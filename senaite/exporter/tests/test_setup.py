# -*- coding: utf-8 -*-
#
# Copyright 2017-2017 SENAITE

from senaite.exporter.tests.base import SimpleTestCase


class TestSetup(SimpleTestCase):
    """ Test Setup
    """

    def test_is_bika_lims_installed(self):
        qi = self.portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled("bika.lims"))

    def test_is_senaite_exporter_installed(self):
        qi = self.portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled("senaite.exporter"))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSetup))
    return suite
