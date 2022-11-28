# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import argparse

from PySide6 import QtCore, QtGui, QtQml

import bridge
import genv
from const import app_const, path_const
from log import qt_message_handler


def get_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    return parser


def main(args) -> int:
    """
    entry function
    Args:
        args: Argument parsed by get_argument_parser()
    Returns:
        int, returncode of current process
    """
    QtCore.qInstallMessageHandler(qt_message_handler.handler)
    QtGui.QGuiApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    QtGui.QGuiApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    app = QtGui.QGuiApplication()
    app.setApplicationName(app_const.APP_NAME)
    app.setApplicationDisplayName(app_const.APP_NAME)
    app.setDesktopFileName(app_const.APP_NAME)
    app.setOrganizationName(app_const.ORGANIZATION_NAME)

    QtCore.QDir.setSearchPaths(app_const.RESOURCE_PREFIX, [path_const.RESOURCE_DIR])
    QtCore.QDir.setSearchPaths(app_const.VIEW_PREFIX, [path_const.VIEW_DIR])
    app.setWindowIcon(QtGui.QIcon(app_const.APP_ICON))

    bridge.register_bridges()
    bridge.initialize_bridge_objects()
    genv.initialize()
    engine = QtQml.QQmlApplicationEngine()
    engine.rootContext().setContextProperties(bridge.get_bridge_objects())
    engine.load('view:/MainWindow.qml')
    if not engine.rootObjects():
        return -1

    returncode = app.exec()
    bridge.finalize_bridge_objects()
    genv.finalize()

    return returncode
