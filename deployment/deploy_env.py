# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import sys
import os
import logging

import deploy
import deploy_utils
import resource_compiler

logger = logging.getLogger('deployment')

deployment_args = deploy.get_argument_parser().parse_args(sys.argv[1:])

root_path = os.getcwd()
source_path = os.path.join(root_path, 'source')
deployment_path = os.path.join(root_path, 'deployment')

all_source_modules = list(deploy_utils.iterate_all_modules(source_path))

scripts = [os.path.join(root_path, 'launcher.py')]
pathex = [source_path]
hiddenimports = [os.path.splitext(resource_compiler.PY_RC_FILE_NAME)[0]]
hiddenimports.extend(all_source_modules)
