# -*- coding: utf-8 -*-
#
# Copyright 2017-2017 SENAITE

import StringIO
import csv


def get_strings(data):
    """
    Convert unicode values to strings even if they belong to lists or dicts.

    :param data: an object.
    :return: The object with all unicode values converted to string.
    """
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')

    # if this is a list of values, return list of string values
    if isinstance(data, list):
        return [get_strings(item) for item in data]

    # if this is a dictionary, return dictionary of string keys and values
    if isinstance(data, dict):
        return {
            get_strings(key): get_strings(value)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data


def build_line(item, columns_order, visible_columns):
    """
    This function builds a list with the given columns order and only
    inserting into the list, the columns defined in visible_columns.

    :param item: A dictionary with a bika_listing line data
    :param columns_order: A list with all the possible columns ordered.
    :param visible_columns: The columns that will be inserted in the
    generated list.

    :return: A list with the values from "item" ordered by "columns_order"
    only if they are in "visible_columns".
    """
    line = []
    for col in columns_order:
        if col in visible_columns:
            line.append(item.get(col, None))
    return line


def build_header(columns_def, columns_order, visible_columns):
    """
    Build a header line as a list from bika_listing.columns definition.

    :param columns_def: A dictionary containing information about each
    columns, such as the column title.
    :param columns_order: A list with the columns order.
    :param visible_columns: A list with the columns that will be visible.

    :return: A list with the 'title' attribute of each column.
    """
    header = []
    for col in columns_order:
        col_def = None
        if col in visible_columns:
            col_def = columns_def.get(col, None)
        if col_def is not None:
            header.append(col_def.get('title', ''))
    return header


def generate_csv(data):
    """
    Generates a CSV file from 'data'.
    :param data: A list of lists where the first line is the header
    data and the following ones are each data line.

    :return: A StringIO object.
    """
    output = StringIO.StringIO()
    csv_writer = csv.writer(output, dialect=csv.excel)
    csv_writer.writerows(data)
    result = output.getvalue()
    output.close()
    return result

