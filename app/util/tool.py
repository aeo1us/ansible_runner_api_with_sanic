#!/usr/bin/env python
# coding: utf-8

# A restful HTTP API for ansible
# Base on ansible-runner and sanic
# Github <https://github.com/lfbear/ansible-api>
# Author: lfbear

import os
import logging

__all__ = ['Tool']


class Tool(object):
    LOGGER = None

    @staticmethod
    def init_logger(path):
        log_format = "%(asctime)s | %(levelname)s - %(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"
        log_formatter = logging.Formatter(fmt=log_format, datefmt=date_format)
        if isinstance(path, str) and os.path.exists(os.path.dirname(path)):
            err_handler = logging.handlers.TimedRotatingFileHandler(path + '/err.log', when='midnight')
            err_handler.setFormatter(log_formatter)
            err_handler.setLevel(logging.WARNING)
            log_handler = logging.handlers.TimedRotatingFileHandler(path + '/out.log', when='midnight')
            log_handler.setFormatter(log_formatter)
            Tool.LOGGER.addHandler(log_handler)
            Tool.LOGGER.addHandler(err_handler)
            Tool.LOGGER.setLevel(logging.DEBUG)
            Tool.LOGGER.propagate = False  # disable console output
        else:
            logging.basicConfig(level=logging.DEBUG,
                                format=log_format, datefmt=date_format)

        Tool.LOGGER = logging.getLogger('ansible-run-api')
