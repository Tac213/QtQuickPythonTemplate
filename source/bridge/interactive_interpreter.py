# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import code

from PySide6 import QtCore, QtQml

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = 'Python.InteractiveInterpreter'
QML_IMPORT_MAJOR_VERSION = 1
QML_IMPORT_MINOR_VERSION = 0


@QtQml.QmlElement
class InteractiveInterpreter(QtCore.QObject):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._interpreter = code.InteractiveInterpreter()

    @QtCore.Slot(str)
    def interpret_script(self, script: str) -> None:
        self._interpreter.runsource(script)
