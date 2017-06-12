# -*- coding: utf-8 -*-
import six

def csv_format(data):
    csv = []
    for value in data:
        if value in [None, False]:
            csv.append('')
            continue

        if not isinstance(value, six.string_types):
            value = '{}'.format(value)

        if ',' in value:
            csv.append('"{}"'.format(value))
        else:
            csv.append('{}'.format(value))
    return ','.join(csv)
