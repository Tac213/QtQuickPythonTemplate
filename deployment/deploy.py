# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import sys
import os
import argparse
import shutil

import PyInstaller.__main__

import resource_compiler
import deploy_env


def check_python_path():
    workspace_folder = os.path.dirname(os.path.dirname(__file__))
    source_folder = os.path.join(workspace_folder, 'source')
    if source_folder in sys.path:
        return
    sys.path.insert(0, source_folder)


def get_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('--variant', '-v', type=str, choices=['debug', 'release'], default='release')
    parser.add_argument('--distpath', '-d', type=str, default=os.path.join(os.path.dirname(__file__), 'dist'))
    parser.add_argument('--workpath', '-b', type=str, default=os.path.join(os.path.dirname(__file__), 'build'))
    return parser


def main(args):
    root_path = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
    if os.path.normpath(os.getcwd()) != root_path:
        deploy_env.logger.error('Deployment should be performed in working directory: %s', root_path)
        sys.exit(-1)
    deploy_env.logger.info('Start deployment.')
    deploy_env.logger.info('variant: %s', args.variant)
    deploy_env.logger.info('distpath: %s', args.distpath)
    deploy_env.logger.info('workpath: %s', args.workpath)
    returncode = resource_compiler.main()
    if returncode:
        deploy_env.logger.error('Failed to compile resource. See logs above.')
        sys.exit(returncode)
    if os.path.exists(args.workpath):
        deploy_env.logger.info('Workpath \'%s\' exists, pending to remove it.', args.workpath)
        shutil.rmtree(args.workpath)
    PyInstaller.__main__.run([
        os.path.join(os.path.dirname(__file__), 'spec', f'{sys.platform}.spec'),
        '--distpath',
        args.distpath,
        '--workpath',
        args.workpath,
        '--noconfirm',
    ])


if __name__ == '__main__':
    check_python_path()
    main(deploy_env.deployment_args)
