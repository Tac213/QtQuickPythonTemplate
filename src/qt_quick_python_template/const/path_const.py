# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import sys
import os
import pathlib

import qt_quick_python_template

ROOT_DIR = (
    getattr(sys, "_MEIPASS")  # PyInstaller
    if getattr(sys, "frozen", False)
    else os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))  # Nuitka
    if hasattr(qt_quick_python_template, "__compiled__")
    else os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))  # Source code
)
ROOT_PATH = (
    pathlib.Path(getattr(sys, "_MEIPASS"))  # PyInstaller
    if getattr(sys, "frozen", False)
    else pathlib.Path(__file__).parent.parent.parent  # Nuitka
    if hasattr(qt_quick_python_template, "__compiled__")
    else pathlib.Path(__file__).parent.parent.parent.parent  # Source code
)

RESOURCE_DIR = os.path.join(ROOT_DIR, "resource")
RESOURCE_PATH = ROOT_PATH / "resource"
APP_ICON_PATH = os.path.join(RESOURCE_DIR, "icon.jpg")

SOURCE_DIR = os.path.join(ROOT_DIR, "src")
SOURCE_PATH = ROOT_PATH / "src"

VIEW_DIR = os.path.join(ROOT_DIR, "view")
VIEW_PATH = ROOT_PATH / "view"

SHADER_DIR = os.path.join(ROOT_DIR, "shader")
SHADER_PATH = ROOT_PATH / "shader"

LOG_DIR = os.path.join(ROOT_DIR, "log")
LOG_PATH = ROOT_PATH / "log"
