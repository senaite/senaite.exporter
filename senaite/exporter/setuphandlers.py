# -*- coding: utf-8 -*-
#
# Copyright 2017-2017 SENAITE


from senaite.exporter import logger


def setup_handler(context):
    """
    SENAITE EXPORTER setup handler
    """

    if context.readDataFile('senaite.exporter.txt') is None:
        return

    logger.info("SENAITE EXPORTER setup handler [BEGIN]")

    logger.info("SENAITE EXPORTER setup handler [DONE]")
