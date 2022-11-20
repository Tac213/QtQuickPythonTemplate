# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

from PySide6 import QtCore, QtQml

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = 'Python.OutputWindowBridge'
QML_IMPORT_MAJOR_VERSION = 1
QML_IMPORT_MINOR_VERSION = 0


@QtQml.QmlElement
class OutputWindowBridge(QtCore.QObject):

    show_normal_message = QtCore.Signal(str, name='showNormalMessage')
    show_warning_message = QtCore.Signal(str, name='showWarningMessage')
    show_error_message = QtCore.Signal(str, name='showErrorMessage')
