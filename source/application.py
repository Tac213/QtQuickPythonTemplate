# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import sys
import argparse

from PySide6 import QtCore, QtGui, QtQml

from const import app_const, path_const


def get_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    return parser


def main(args) -> None:
    """
    entry function
    Returns:
        None
    """
    QtGui.QGuiApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    QtGui.QGuiApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    app = QtGui.QGuiApplication()
    app.setApplicationName(app_const.APP_NAME)
    app.setApplicationDisplayName(app_const.APP_NAME)
    app.setDesktopFileName(app_const.APP_NAME)
    app.setOrganizationName(app_const.ORGANIZATION_NAME)

    QtCore.QDir.setSearchPaths(app_const.RESOURCE_PREFIX, [path_const.RESOURCE_DIR])
    QtCore.QDir.setSearchPaths(app_const.VIEW_PREFIX, [path_const.VIEW_DIR])

    engine = QtQml.QQmlApplicationEngine('view:/MainWindow.qml')
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
