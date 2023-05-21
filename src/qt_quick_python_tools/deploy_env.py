# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import sys
import os
import logging

from qt_quick_python_tools import deploy
from qt_quick_python_tools import deploy_utils
from qt_quick_python_tools import resource_compiler

logger = logging.getLogger("deployment")

deployment_args = deploy.get_argument_parser().parse_args(sys.argv[1:])

root_path = os.getcwd()
source_path = os.path.join(root_path, "src", "qt_quick_python_template")
deployment_path = os.path.join(root_path, "src", "qt_quick_python_tools")

all_source_modules = list(deploy_utils.iterate_all_modules(source_path))

entry_script = os.path.join(source_path, "__main__.py")
scripts = [entry_script]
pathex = [source_path]
hiddenimports = [os.path.splitext(resource_compiler.PY_RC_FILE_NAME)[0]]
hiddenimports.extend(all_source_modules)
