from __future__ import unicode_literals
from collections import OrderedDict
from datetime import date

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

CUSTOMFIELD_MODELS = (
    'book',
)

CF_TYPE_TEXT = 100
CF_TYPE_INTEGER = 200
CF_TYPE_BOOLEAN = 300
CF_TYPE_DATE = 400
CF_TYPE_URL = 500
CF_TYPE_SELECT = 600
CUSTOMFIELD_TYPE_CHOICES = (
    (CF_TYPE_TEXT, 'Text'),
    (CF_TYPE_INTEGER, 'Integer'),
    (CF_TYPE_BOOLEAN, 'Boolean (true/false)'),
    (CF_TYPE_DATE, 'Date'),
    (CF_TYPE_URL, 'URL'),
    (CF_TYPE_SELECT, 'Selection'),
)

#
# Custom fields
#

class CustomFieldModel(object):

    def cf(self):
        """
        Name-based CustomFieldValue accessor for use in templates
        """
        if not hasattr(self, 'get_custom_fields'):
            return dict()
        return {field.name: value for field, value in self.get_custom_fields().items()}

    def get_custom_fields(self):
        """
        Return a dictionary of custom fields for a single object in the form {<field>: value}.
        """

        # Find all custom fields applicable to this type of object
        content_type = ContentType.objects.get_for_model(self)
        fields = CustomField.objects.filter(obj_type=content_type)

        # If the object exists, populate its custom fields with values
        if hasattr(self, 'pk'):
            values = CustomFieldValue.objects.filter(obj_type=content_type, obj_id=self.pk).select_related('field')
            values_dict = {cfv.field_id: cfv.value for cfv in values}
            return OrderedDict([(field, values_dict.get(field.pk)) for field in fields])
        else:
            return OrderedDict([(field, None) for field in fields])


@python_2_unicode_compatible
class CustomField(models.Model):
    obj_type = models.ManyToManyField(ContentType, related_name='custom_fields', verbose_name='Object(s)',
                                      limit_choices_to={'model__in': CUSTOMFIELD_MODELS},
                                      help_text="The object(s) to which this field applies.")
    type = models.PositiveSmallIntegerField(choices=CUSTOMFIELD_TYPE_CHOICES, default=CF_TYPE_TEXT)
    name = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=50, blank=True, help_text="Name of the field as displayed to users (if not "
                                                                  "provided, the field's name will be used)")
    description = models.CharField(max_length=100, blank=True)
    required = models.BooleanField(default=False, help_text="Determines whether this field is required when creating "
                                                            "new objects or editing an existing object.")
    is_filterable = models.BooleanField(default=True, help_text="This field can be used to filter objects.")
    default = models.CharField(max_length=100, blank=True, help_text="Default value for the field. Use \"true\" or "
                                                                     "\"false\" for booleans. N/A for selection "
                                                                     "fields.")
    weight = models.PositiveSmallIntegerField(default=100, help_text="Fields with higher weights appear lower in a "
                                                                     "form")

    class Meta:
        ordering = ['weight', 'name']

    def __str__(self):
        return self.label or self.name.replace('_', ' ').capitalize()

    def serialize_value(self, value):
        """
        Serialize the given value to a string suitable for storage as a CustomFieldValue
        """
        if value is None:
            return ''
        if self.type == CF_TYPE_BOOLEAN:
            return str(int(bool(value)))
        if self.type == CF_TYPE_DATE:
            # Could be date/datetime object or string
            try:
                return value.strftime('%Y-%m-%d')
            except AttributeError:
                return value
        if self.type == CF_TYPE_SELECT:
            # Could be ModelChoiceField or TypedChoiceField
            return str(value.id) if hasattr(value, 'id') else str(value)
        return value

    def deserialize_value(self, serialized_value):
        """
        Convert a string into the object it represents depending on the type of field
        """
        if serialized_value is '':
            return None
        if self.type == CF_TYPE_INTEGER:
            return int(serialized_value)
        if self.type == CF_TYPE_BOOLEAN:
            return bool(int(serialized_value))
        if self.type == CF_TYPE_DATE:
            # Read date as YYYY-MM-DD
            return date(*[int(n) for n in serialized_value.split('-')])
        if self.type == CF_TYPE_SELECT:
            return self.choices.get(pk=int(serialized_value))
        return serialized_value


@python_2_unicode_compatible
class CustomFieldValue(models.Model):
    field = models.ForeignKey('CustomField', related_name='values', on_delete=models.CASCADE)
    obj_type = models.ForeignKey(ContentType, related_name='+', on_delete=models.PROTECT)
    obj_id = models.PositiveIntegerField()
    obj = GenericForeignKey('obj_type', 'obj_id')
    serialized_value = models.CharField(max_length=255)

    class Meta:
        ordering = ['obj_type', 'obj_id']
        unique_together = ['field', 'obj_type', 'obj_id']

    def __str__(self):
        return '{} {}'.format(self.obj, self.field)

    @property
    def value(self):
        return self.field.deserialize_value(self.serialized_value)

    @value.setter
    def value(self, value):
        self.serialized_value = self.field.serialize_value(value)

    def save(self, *args, **kwargs):
        # Delete this object if it no longer has a value to store
        if self.pk and self.value is None:
            self.delete()
        else:
            super(CustomFieldValue, self).save(*args, **kwargs)


@python_2_unicode_compatible
class CustomFieldChoice(models.Model):
    field = models.ForeignKey('CustomField', related_name='choices', limit_choices_to={'type': CF_TYPE_SELECT},
                              on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    weight = models.PositiveSmallIntegerField(default=100, help_text="Higher weights appear lower in the list")

    class Meta:
        ordering = ['field', 'weight', 'value']
        unique_together = ['field', 'value']

    def __str__(self):
        return self.value

    def clean(self):
        if self.field.type != CF_TYPE_SELECT:
            raise ValidationError("Custom field choices can only be assigned to selection fields.")

    def delete(self, using=None, keep_parents=False):
        # When deleting a CustomFieldChoice, delete all CustomFieldValues which point to it
        pk = self.pk
        super(CustomFieldChoice, self).delete(using, keep_parents)
        CustomFieldValue.objects.filter(field__type=CF_TYPE_SELECT, serialized_value=str(pk)).delete()
