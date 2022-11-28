# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import sys
from PySide6 import QtCore
import bridge


def handler(mode: QtCore.QtMsgType, context: QtCore.QMessageLogContext, message: str) -> None:
    # available fields of context: category, file, function, line
    formatted_message = QtCore.qFormatLogMessage(mode, context, message)
    if bridge.output_window_bridge_object:
        if mode in (QtCore.QtMsgType.QtDebugMsg, QtCore.QtMsgType.QtInfoMsg):
            bridge.output_window_bridge_object.show_normal_message.emit(formatted_message)
        elif mode == QtCore.QtMsgType.QtWarningMsg:
            bridge.output_window_bridge_object.show_warning_message.emit(formatted_message)
        elif mode in (QtCore.QtMsgType.QtCriticalMsg, QtCore.QtMsgType.QtFatalMsg):
            bridge.output_window_bridge_object.show_error_message.emit(formatted_message)
    if mode in (QtCore.QtMsgType.QtDebugMsg, QtCore.QtMsgType.QtInfoMsg):
        sys.__stdout__.write(f'{formatted_message}\n')
    else:
        sys.__stderr__.write(f'{formatted_message}\n')
