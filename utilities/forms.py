# -*- coding: utf-8 -*-
import csv
from django import forms

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

#
# Form fields
#

class CSVDataField(forms.CharField):
    """
    A CharField (rendered as a Textarea) which accepts CSV-formatted data. It returns a list of dictionaries mapping
    column headers to values. Each dictionary represents an individual record.
    """
    widget = forms.Textarea

    def __init__(self, fields, required_fields=None, *args, **kwargs):

        self.fields = fields
        self.required_fields = required_fields if required_fields else []

        super(CSVDataField, self).__init__(*args, **kwargs)

        self.strip = False
        if not self.label:
            self.label = 'CSV Data'
        if not self.initial:
            self.initial = ','.join(required_fields) + '\n'
        if not self.help_text:
            self.help_text = 'Enter the list of column headers followed by one line per record to be imported, using ' \
                             'commas to separate values. Multi-line data and values containing commas may be wrapped ' \
                             'in double quotes.'

    def to_python(self, value):

        # Python 2's csv module has problems with Unicode
        if not isinstance(value, str):
            value = value.encode('utf-8')

        records = []
        reader = csv.reader(value.splitlines())

        # Consume and valdiate the first line of CSV data as column headers
        headers = reader.next()
        for f in self.required_fields:
            if f not in headers:
                raise forms.ValidationError('Required column header "{}" not found.'.format(f))
        for f in headers:
            if f not in self.fields:
                raise forms.ValidationError('Unexpected column header "{}" found.'.format(f))

        # Parse CSV data
        for i, row in enumerate(reader, start=1):
            if row:
                if len(row) != len(headers):
                    raise forms.ValidationError(
                        "Row {}: Expected {} columns but found {}".format(i, len(headers), len(row))
                    )
                row = [col.strip() for col in row]
                record = dict(zip(headers, row))
                records.append(record)

        return records

class CSVChoiceField(forms.ChoiceField):
    """
    Invert the provided set of choices to take the human-friendly label as input, and return the database value.
    """

    def __init__(self, choices, *args, **kwargs):
        super(CSVChoiceField, self).__init__(choices, *args, **kwargs)
        self.choices = [(label, label) for value, label in choices]
        self.choice_values = {label: value for value, label in choices}

    def clean(self, value):
        value = super(CSVChoiceField, self).clean(value)
        if not value:
            return None
        if value not in self.choice_values:
            raise forms.ValidationError("Invalid choice: {}".format(value))
        return self.choice_values[value]
