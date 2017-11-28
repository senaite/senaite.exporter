# -*- coding: utf-8 -*-
#
# Copyright 2017-2017 SENAITE

import json

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements

from bika.lims.interfaces import ITopLeftListingHook


class ListsExporter(object):
    """
    Creates a view with the available list exporters. It gives values to the
    form elements that will be sued by the exporter.
    """
    implements(ITopLeftListingHook)
    template = ViewPageTemplateFile("templates/lists_exporters.pt")

    def __init__(self, listing_table):
        self.request = None
        self.pagesize = None
        self.listing_table = listing_table
        self.bika_listing = listing_table.bika_listing
        self.context = listing_table.context

    def __call__(self, request):
        self.request = request
        self.pagesize = self.bika_listing.pagesize

        return self.template()

    def get_pagesize(self):
        """
        Retrieves the current page size used to display the list.

        :return: json string with page size
        """
        return json.dumps(self.pagesize)

    def get_class_view_id(self):
        """
        Retrieves the class view module name that renders the list.

        :return: json string module name
        """
        # If I use 'self.bika_listing.implemented.__name__' here, I get
        # 'Products.Five.metaclass.AnalysisRequestsView' instead of
        # 'bika.lims.browser.analysisrequest.analysisrequests
        # .AnalysisRequestsView'. I don't understand why this happens.
        implemented_name = self.bika_listing.implemented.__name__
        return json.dumps(implemented_name)
