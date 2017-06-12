# -*- coding: utf-8 -*-
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import render
from django.forms import Form
from django.db import transaction
from django.core.exceptions import ValidationError
from utilities.forms import BootstrapMixin, CSVDataField

class BulkImportView(View):
    """
    Import objects in bulk (CSV format).

    model_form: The form used to create each imported object
    table: The django-tables2 Table used to render the list of imported objects
    template_name: The name of the template
    default_return_url: The name of the URL to use for the cancel button
    """
    model_form = None
    table = None
    default_return_url = None
    template_name = 'utilities/obj_import.html'

    def _import_form(self, *args, **kwargs):

        fields = self.model_form().fields.keys()
        required_fields = [name for name, field in self.model_form().fields.items() if field.required]

        class ImportForm(BootstrapMixin, Form):
            csv = CSVDataField(fields=fields, required_fields=required_fields)

        return ImportForm(*args, **kwargs)

    def _save_obj(self, obj_form):
        """
        Provide a hook to modify the object immediately before saving it (e.g. to encrypt secret data).
        """
        return obj_form.save()

    def get(self, request):

        return render(request, self.template_name, {
            'form': self._import_form(),
            'fields': self.model_form().fields,
            'obj_type': self.model_form._meta.model._meta.verbose_name,
            'return_url': self.default_return_url,
        })

    def post(self, request):

        new_objs = []
        form = self._import_form(request.POST)

        if form.is_valid():

            try:
                # Iterate through CSV data and bind each row to a new model form instance.
                with transaction.atomic():
                    for row, data in enumerate(form.cleaned_data['csv'], start=1):
                        obj_form = self.model_form(data)
                        if obj_form.is_valid():
                            obj = self._save_obj(obj_form)
                            new_objs.append(obj)
                        else:
                            for field, err in obj_form.errors.items():
                                form.add_error('csv', "Row {} {}: {}".format(row, field, err[0]))
                            raise ValidationError("")

                # Compile a table containing the imported objects
                obj_table = self.table(new_objs)
                msg = 'Imported {} {}'.format(len(new_objs), new_objs[0]._meta.verbose_name_plural)
                messages.success(request, msg)

                return render(request, "import_success.html", {
                    'table': obj_table,
                    'return_url': self.default_return_url,
                })

            except ValidationError:
                pass

        return render(request, self.template_name, {
            'form': form,
            'fields': self.model_form().fields,
            'obj_type': self.model_form._meta.model._meta.verbose_name,
            'return_url': self.default_return_url,
        })
