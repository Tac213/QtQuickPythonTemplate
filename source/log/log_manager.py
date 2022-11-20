# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import logging
import enum
import typing
import time
import os

from . import logger as logger_module
from . import output_window_handler
from . import mock_stdout  # pylint: disable=unused-import


@enum.unique
class LogLevel(enum.Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class LogManager(object):
    created_logger_names = set()
    level = LogLevel.DEBUG
    tag = ''

    @classmethod
    def get_logger(cls,
                   logger_name: str,
                   log_to_output_window: bool = True,
                   save_file: bool = False,
                   dirname: typing.Optional[str] = None) -> logger_module.Logger:
        if logger_name in cls.created_logger_names:
            return logging.getLogger(logger_name)

        logger = logging.getLogger(logger_name)
        logger.setLevel(cls.level.value)
        logger.addHandler(cls._create_handler(save_file, dirname))
        if log_to_output_window:
            logger.addHandler(cls._create_handler())
        cls.created_logger_names.add(logger_name)

        return logger

    @classmethod
    def _create_handler(cls, save_file=False, dirname=None):
        con = ' - '
        # 可以用的key参考logging源码Formatter类的注释
        format_list = ['%(asctime)s', cls.tag, '%(levelname)s', '%(message)s']
        if save_file:
            if dirname:
                filename = os.path.join(dirname, f'{cls.tag}_{time.strftime("%Y%m%d_%H%M%S")}.log')
            else:
                filename = f'{cls.tag}_{time.strftime("%Y%m%d_%H%M%S")}.log'
            handler = logging.FileHandler(filename, encoding='utf-8')
        else:
            # handler = logging.StreamHandler(sys.stdout)
            handler = output_window_handler.OutputWindowHandler()

        handler.setLevel(cls.level.value)
        formatter = logging.Formatter(con.join(format_list))
        handler.setFormatter(formatter)
        return handler

    @classmethod
    def set_level(cls, level: LogLevel):
        cls.level = level
        for logger_name in cls.created_logger_names:
            logging.getLogger(logger_name).setLevel(level.value)

    @classmethod
    def set_tag(cls, tag: str) -> None:
        cls.tag = tag
        for logger_name in cls.created_logger_names:
            logger = logging.getLogger(logger_name)
            logger.addHandler(cls._create_handler())
