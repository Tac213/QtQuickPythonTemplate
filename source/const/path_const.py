# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import sys
import os
import pathlib

ROOT_DIR = getattr(sys, '_MEIPASS') if getattr(sys, 'frozen', False) else os.path.normpath(
    os.path.join(os.path.dirname(__file__), '..', '..'))
ROOT_PATH = pathlib.Path(getattr(sys, '_MEIPASS')) if getattr(sys, 'frozen', False) else pathlib.Path(__file__).parent.parent.parent

RESOURCE_DIR = os.path.join(ROOT_DIR, 'resource')
RESOURCE_PATH = ROOT_PATH / 'resource'
APP_ICON_PATH = os.path.join(RESOURCE_DIR, 'icon.jpg')

SOURCE_DIR = os.path.join(ROOT_DIR, 'source')
SOURCE_PATH = ROOT_PATH / 'source'

VIEW_DIR = os.path.join(ROOT_DIR, 'view')
VIEW_PATH = ROOT_PATH / 'view'

LOG_DIR = os.path.join(ROOT_DIR, 'log')
LOG_PATH = ROOT_PATH / 'log'
