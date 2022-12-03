# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import sys
import logging
import enum
import typing
import time
import os

from . import logger as logger_module
from . import output_window_handler
from . import mock_stdout


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
    file_handler = None

    @classmethod
    def get_logger(cls,
                   logger_name: str,
                   log_to_output_window: bool = True,
                   save_file: bool = True,
                   dirname: typing.Optional[str] = None) -> logger_module.Logger:
        if not cls.file_handler and dirname:
            cls.file_handler = cls._create_handler(True, dirname)
        if logger_name in cls.created_logger_names:
            return logging.getLogger(logger_name)

        logger = logging.getLogger(logger_name)
        logger.setLevel(cls.level.value)
        if save_file:
            if not dirname:
                logger.addHandler(cls.file_handler)
            else:
                logger.addHandler(cls._create_handler(save_file, dirname))
        if log_to_output_window:
            logger.addHandler(cls._create_handler())
        cls.created_logger_names.add(logger_name)

        return logger

    @classmethod
    def _create_handler(cls, save_file=False, dirname=None):
        con = ' - '
        # comment of logging.Formatter lists all available keys
        format_list = ['%(asctime)s', '%(name)s', '%(levelname)s', '%(message)s']
        if save_file:
            if dirname:
                filename = os.path.join(dirname, f'{cls.tag}_{time.strftime("%Y%m%d_%H%M%S")}.log')
            else:
                return cls.file_handler
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

    @classmethod
    def setup_std_logger(cls) -> None:
        sys.stdout = mock_stdout.MockStdout(mock_stdout.ChannelType.STDOUT, sys.__stdout__, cls.file_handler)
        sys.stderr = mock_stdout.MockStdout(mock_stdout.ChannelType.STDERR, sys.__stderr__, cls.file_handler)
