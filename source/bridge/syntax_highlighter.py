# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com
# translated from: https://github.com/stephenquan/QtSyntaxHighlighterApp
# stackoverflow: https://stackoverflow.com/questions/14791360/qt5-syntax-highlighting-in-qml
# unfortunately, this file cannot work like C++, as QQuickTextDocument should be used from C++ directly
# see official documentation of QQuickTextDocument: https://doc.qt.io/qtforpython/PySide6/QtQuick/QQuickTextDocument.html
# instantiation of QQuickTextDocument in Python will cause a crash

import typing
from PySide6 import QtCore, QtQml, QtGui, QtQuick

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = 'Python.SyntaxHighlighter'
QML_IMPORT_MAJOR_VERSION = 1
QML_IMPORT_MINOR_VERSION = 0


@QtQml.QmlElement
class SyntaxHighlighter(QtGui.QSyntaxHighlighter):

    text_document_changed = QtCore.Signal(name='textDocumentChanged')
    py_highlight_block = QtCore.Signal(name='pyHighlightBlock')

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._text_document = None  # type: typing.Optional[QtQuick.QQuickTextDocument]

    def get_text_document(self) -> QtQuick.QQuickTextDocument:
        return self._text_document

    def set_text_document(self, text_document: QtQuick.QQuickTextDocument) -> None:
        if self._text_document is text_document:
            return
        self._text_document = text_document
        self.set_document(text_document.text_document())
        self.text_document_changed.emit()

    text_document = QtCore.Property(object, get_text_document, set_text_document, notify=text_document_changed)

    def highlight_block(self, text: str) -> None:
        super().highlight_block(text)
        self.py_highlight_block.emit()
