# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import os
import pathlib

ROOT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
ROOT_PATH = pathlib.Path(__file__).parent.parent.parent

RESOURCE_DIR = os.path.join(ROOT_DIR, 'resource')
RESOURCE_PATH = ROOT_PATH / 'resource'

SOURCE_DIR = os.path.join(ROOT_DIR, 'source')
SOURCE_PATH = ROOT_PATH / 'source'

VIEW_DIR = os.path.join(ROOT_DIR, 'view')
VIEW_PATH = ROOT_PATH / 'view'

LOG_DIR = os.path.join(ROOT_DIR, 'log')
LOG_PATH = ROOT_PATH / 'log'
