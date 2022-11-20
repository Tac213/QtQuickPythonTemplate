# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

from PySide6 import QtCore


class MetaSingleton(type):

    def __init__(cls, name, bases, class_dict, **kwargs):
        super().__init__(name, bases, class_dict, **kwargs)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__call__(*args, **kwargs)
        return cls.instance


class QMetaSingleton(MetaSingleton, type(QtCore.QObject)):
    pass


class Singleton(object, metaclass=MetaSingleton):
    pass


class QSingleton(QtCore.QObject, metaclass=QMetaSingleton):
    pass
