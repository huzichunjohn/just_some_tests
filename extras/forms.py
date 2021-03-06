from __future__ import unicode_literals
import re
from collections import OrderedDict

from django import forms
from django.core.validators import URLValidator
from django.contrib.contenttypes.models import ContentType

from .models import (
    CF_TYPE_BOOLEAN, CF_TYPE_DATE, CF_TYPE_INTEGER, CF_TYPE_SELECT, CF_TYPE_URL, CustomField, CustomFieldValue,
)

class BootstrapMixin(forms.BaseForm):

    def __init__(self, *args, **kwargs):
        super(BootstrapMixin, self).__init__(*args, **kwargs)

        exempt_widgets = [forms.CheckboxInput, forms.ClearableFileInput, forms.FileInput, forms.RadioSelect]

        for field_name, field in self.fields.items():
            if field.widget.__class__ not in exempt_widgets:
                css = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = ' '.join([css, 'form-control']).strip()
            if field.required:
                field.widget.attrs['required'] = 'required'
            if 'placeholder' not in field.widget.attrs:
                field.widget.attrs['placeholder'] = field.label

class BulkEditForm(forms.Form):

    def __init__(self, model, *args, **kwargs):
        super(BulkEditForm, self).__init__(*args, **kwargs)
        self.model = model
        # Copy any nullable fields defined in Meta
        if hasattr(self.Meta, 'nullable_fields'):
            self.nullable_fields = [field for field in self.Meta.nullable_fields]
        else:
            self.nullable_fields = []

class LaxURLField(forms.URLField):
    """
    Custom URLField which allows any valid URL scheme
    """

    class AnyURLScheme(object):
        # A fake URL list which "contains" all scheme names abiding by the syntax defined in RFC 3986 section 3.1
        def __contains__(self, item):
            if not item or not re.match('^[a-z][0-9a-z+\-.]*$', item.lower()):
                return False
            return True

    default_validators = [URLValidator(schemes=AnyURLScheme())]

def get_custom_fields_for_model(content_type, filterable_only=False, bulk_edit=False):
    """
    Retrieve all CustomFields applicable to the given ContentType
    """
    field_dict = OrderedDict()
    kwargs = {'obj_type': content_type}
    if filterable_only:
        kwargs['is_filterable'] = True
    custom_fields = CustomField.objects.filter(**kwargs)

    for cf in custom_fields:
        field_name = 'cf_{}'.format(str(cf.name))

        # Integer
        if cf.type == CF_TYPE_INTEGER:
            field = forms.IntegerField(required=cf.required, initial=cf.default)

        # Boolean
        elif cf.type == CF_TYPE_BOOLEAN:
            choices = (
                (None, '---------'),
                (1, 'True'),
                (0, 'False'),
            )
            if cf.default.lower() in ['true', 'yes', '1']:
                initial = 1
            elif cf.default.lower() in ['false', 'no', '0']:
                initial = 0
            else:
                initial = None
            field = forms.NullBooleanField(required=cf.required, initial=initial,
                                           widget=forms.Select(choices=choices))

        # Date
        elif cf.type == CF_TYPE_DATE:
            field = forms.DateField(required=cf.required, initial=cf.default, help_text="Date format: YYYY-MM-DD")

        # Select
        elif cf.type == CF_TYPE_SELECT:
            choices = [(cfc.pk, cfc) for cfc in cf.choices.all()]
            if not cf.required or bulk_edit or filterable_only:
                choices = [(None, '---------')] + choices
            field = forms.TypedChoiceField(choices=choices, coerce=int, required=cf.required)

        # URL
        elif cf.type == CF_TYPE_URL:
            field = LaxURLField(required=cf.required, initial=cf.default)

        # Text
        else:
            field = forms.CharField(max_length=255, required=cf.required, initial=cf.default)

        field.model = cf
        field.label = cf.label if cf.label else cf.name.replace('_', ' ').capitalize()
        if cf.description:
            field.help_text = cf.description

        field_dict[field_name] = field

    return field_dict


class CustomFieldForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        self.custom_fields = []
        self.obj_type = ContentType.objects.get_for_model(self._meta.model)

        super(CustomFieldForm, self).__init__(*args, **kwargs)

        # Add all applicable CustomFields to the form
        custom_fields = []
        for name, field in get_custom_fields_for_model(self.obj_type).items():
            self.fields[name] = field
            custom_fields.append(name)
        self.custom_fields = custom_fields

        # If editing an existing object, initialize values for all custom fields
        if self.instance.pk:
            existing_values = CustomFieldValue.objects.filter(obj_type=self.obj_type, obj_id=self.instance.pk)\
                .select_related('field')
            for cfv in existing_values:
                self.initial['cf_{}'.format(str(cfv.field.name))] = cfv.serialized_value

    def _save_custom_fields(self):

        for field_name in self.custom_fields:
            try:
                cfv = CustomFieldValue.objects.select_related('field').get(field=self.fields[field_name].model,
                                                                           obj_type=self.obj_type,
                                                                           obj_id=self.instance.pk)
            except CustomFieldValue.DoesNotExist:
                # Skip this field if none exists already and its value is empty
                if self.cleaned_data[field_name] in [None, '']:
                    continue
                cfv = CustomFieldValue(
                    field=self.fields[field_name].model,
                    obj_type=self.obj_type,
                    obj_id=self.instance.pk
                )
            cfv.value = self.cleaned_data[field_name]
            cfv.save()

    def save(self, commit=True):
        obj = super(CustomFieldForm, self).save(commit)

        # Handle custom fields the same way we do M2M fields
        if commit:
            self._save_custom_fields()
        else:
            self.save_custom_fields = self._save_custom_fields

        return obj


class CustomFieldBulkEditForm(BulkEditForm):

    def __init__(self, *args, **kwargs):
        super(CustomFieldBulkEditForm, self).__init__(*args, **kwargs)

        self.custom_fields = []
        self.obj_type = ContentType.objects.get_for_model(self.model)

        # Add all applicable CustomFields to the form
        custom_fields = get_custom_fields_for_model(self.obj_type, bulk_edit=True).items()
        for name, field in custom_fields:
            # Annotate non-required custom fields as nullable
            if not field.required:
                self.nullable_fields.append(name)
            field.required = False
            self.fields[name] = field
            # Annotate this as a custom field
            self.custom_fields.append(name)


class CustomFieldFilterForm(forms.Form):

    def __init__(self, *args, **kwargs):

        self.obj_type = ContentType.objects.get_for_model(self.model)

        super(CustomFieldFilterForm, self).__init__(*args, **kwargs)

        # Add all applicable CustomFields to the form
        custom_fields = get_custom_fields_for_model(self.obj_type, filterable_only=True).items()
        for name, field in custom_fields:
            field.required = False
            self.fields[name] = field
