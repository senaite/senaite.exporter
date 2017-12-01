# -*- coding: utf-8 -*-
#
# Copyright 2017-2017 SENAITE

from zope.interface import Interface  # noqa


class ISenaiteExporter(Interface):
    """Marker interface that defines a Zope 3 browser layer.
    A layer specific for this add-on product.
    This interface is referred in browserlayer.xml.
    All views and viewlets register against this layer will appear on
    your Plone site only when the add-on installer has been run.
    """
