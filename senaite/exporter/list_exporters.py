# -*- coding: utf-8 -*-
#
# Copyright 2017-2017 SENAITE

import datetime
import json

import plone
from senaite.exporter.utils import build_header
from senaite.exporter.utils import build_line
from senaite.exporter.utils import generate_csv
from senaite.exporter.utils import get_strings
from senaite.exporter.utils import get_view
from senaite.exporter.utils import generate_xml
from senaite.exporter import logger

from bika.lims.browser import BrowserView


class ListExporter(BrowserView):
    """
    Exports the current list (all the possible items to list or only the
    visible ones) to different formats, such as CSV or XML.
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.view_instance = None
        self.items_list = None
        self.result_file = None
        self.export_format = None
        self.file_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    def __call__(self):
        plone.protect.CheckAuthenticator(self.request.form)

        submitted = self.request.form.get('export-list-submission', None)
        if not submitted:
            return None

        self.export_format = get_strings(
            self.request.form.get('exporter-selection', None))
        if not self.export_format:
            return None

        # Getting view instance
        self.view_instance = self.get_view_instance()
        # Getting all items as list of lists
        self.items_list = get_strings(self.export_to_list())

        # Setting header
        setheader = self.request.RESPONSE.setHeader

        # Generating files
        # CSV
        if self.export_format in ['csv_whole_list', 'csv_current_list']:
            self.file_name += '.csv'
            self.result_file = generate_csv(self.items_list)
            # Setting headers for result
            setheader('Content-Type', 'text/comma-separated-values')

        # XML
        if self.export_format in ['xml_whole_list', 'xml_current_list']:
            self.file_name += '.xml'
            self.result_file = generate_xml(self.items_list)
            # Setting headers for result
            setheader('Content-Type', 'application/xml')

        if self.result_file is None:
            logger.info(
                "Generated file from format {} is None."
                .format(self.export_format))
            return

        setheader('Content-Length', len(self.result_file))
        # Stream file to browser
        setheader(
            'Content-Disposition',
            'attachment; filename=%s'
            % self.file_name)
        # Send file
        self.request.RESPONSE.write(self.result_file)

    def get_view_instance(self,):
        """
        Gets current class view dynamically.

        :return: instanced class object
        """
        view_name = get_strings(self.request.form.get('view-name'))
        return get_view(self.context, self.request, view_name)

    def export_to_list(self):
        """
        Export listed items to a python list of lists where the first list
        is the header and the later lists are each line.

        :return: A list of lists as the list of items
        """
        # Basic info that will be needed
        lines = []
        columns_map = self.view_instance.columns
        review_states = self.view_instance.review_states
        form_id = self.view_instance.form_id
        review_state = get_strings(
            self.request.get(form_id + '_review_state', 'default'))

        avoid_void_cols = self.export_format in [
            'xml_whole_list',
            'xml_current_list']

        # Getting columns for review_state
        columns_order = []
        for dic in review_states:
            if dic.get('id', None) == review_state:
                columns_order = dic.get('columns', [])
                break
        visible_columns = self.view_instance.get_toggle_cols()

        # Columns without title will not be included in the final file when
        # exporting to formats such as XML.
        if avoid_void_cols:
            visible_columns_tmp = []
            for col in visible_columns:
                col_def = columns_map.get(col, {})
                title = col_def.get('title', '')
                if title:
                    visible_columns_tmp.append(col)
            visible_columns = visible_columns_tmp

        # Getting items
        items = self.get_items()

        # building the list of lists
        for item in items:
            lines.append(build_line(item, columns_order, visible_columns))
        header = build_header(columns_map, columns_order, visible_columns)
        return [header] + lines

    def get_items(self):
        """
        This function uses a instance of the current view object to get the
        same listed items.

        :return: A list of lists with all the listed values.
        """
        # Setting filters and processes before getting final items
        self._apply_specific_conditions()
        # Call list process
        self.view_instance._process_request()

        # Getting all items
        return self.view_instance.folderitems()

    def _apply_specific_conditions(self):
        """
        Apply specific condition to the request request.
        Modifications for request filter patterns should be placed here!
        """
        form_id = self.view_instance.form_id
        export_selection = self.request.form.get('exporter-selection', None)

        # Filter bar data
        filter_bar = self.request.get('filter-bar-backup', '')
        filter_bar_decoded = {}
        if filter_bar is not None and filter_bar:
            try:
                decoded = json.loads(filter_bar)
            except ValueError:
                decoded = filter_bar
            filter_bar_decoded = get_strings(decoded)

        self.view_instance.save_filter_bar_values(filter_bar_decoded)
        self.view_instance.printwfenabled = \
            self.context.bika_setup.getPrintingWorkflowEnabled()

        # Setting page size
        # TODO: Is there another way to set page-seize as infinite?
        pagesize = 999999
        if export_selection not in ['csv_whole_list', 'xml_whole_list']:
            pagesize = self.request.form.get(form_id + '_pagesize', '')
            if pagesize:
                pagesize = int(json.loads(pagesize))
        self.view_instance.request.set(form_id + '_pagesize', pagesize)

        # Setting review state filter
        state = self.request.form.get('state-filter-backup', '')
        if state:
            self.view_instance.request.form[form_id + '_review_state'] =\
                get_strings(json.loads(state))

        # Setting Plone filter
        plone_filter = self.request.form.get('filter-backup', '')
        if plone_filter:
            try:
                decoded = json.loads(plone_filter)
            except ValueError:
                decoded = plone_filter
            self.view_instance.request.set(
                form_id + '_filter',
                get_strings(decoded))
