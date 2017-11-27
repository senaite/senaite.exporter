# -*- coding: utf-8 -*-
#
# Copyright 2017 SENAITE

import logging

from zope.i18nmessageid import MessageFactory

logger = logging.getLogger("senaite.exporter")
_ = MessageFactory('senaite.exporter')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    logger.info("*** Initializing SENAITE EXPORTER ***")
