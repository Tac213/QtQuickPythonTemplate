# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import os

from qt_quick_python_template.const import path_const, app_const
from qt_quick_python_template.log import logger as logger_module
from qt_quick_python_template.log import log_manager

logger = None  # type: logger_module.Logger


def initialize() -> None:
    _init_logger()


def _init_logger() -> None:
    global logger
    if not os.path.isdir(path_const.LOG_DIR):
        os.mkdir(path_const.LOG_DIR)
    log_manager.LogManager.set_tag(app_const.APP_NAME)
    logger = log_manager.LogManager.get_logger(app_const.APP_NAME, save_file=True, dirname=path_const.LOG_DIR)
    log_manager.LogManager.setup_std_logger()


def finalize() -> None:
    pass
