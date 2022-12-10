# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import sys
import os
import argparse
import logging
import subprocess

EXCLUDE_DIR_NAMES = (
    '.git',
    '.svn',
    '__pycache__',
)
QML_EXT = '.qml'


def check_python_path():
    workspace_folder = os.path.dirname(os.path.dirname(__file__))
    source_folder = os.path.join(workspace_folder, 'source')
    if source_folder in sys.path:
        return
    sys.path.insert(0, source_folder)


def get_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', '-a', help='Whether to format all qml files', action='store_true', default=False)
    parser.add_argument('--dont-delete-backup-file', help='Dont delete qml~ backup file', action='store_true', default=False)
    parser.add_argument('files', type=str, help='Files to be processed by qmlformat', nargs='*')
    return parser


def format_files(file_paths, dont_delete_backup_file) -> int:
    from const import path_const  # pylint: disable=import-outside-toplevel
    pyside6_qmlformat_executable = os.path.join(os.path.dirname(sys.executable), 'pyside6-qmlformat')
    for file_path in file_paths:
        command_args = [
            pyside6_qmlformat_executable,
            file_path,
            '--inplace',
        ]
        logging.info('Running command "%s" in "%s"', ' '.join(command_args), path_const.ROOT_DIR)
        with subprocess.Popen(command_args, cwd=path_const.ROOT_DIR) as p:
            p.wait()
        if p.returncode:
            return p.returncode
        if dont_delete_backup_file:
            continue
        backup_file_path = f'{file_path}~'
        if os.path.exists(backup_file_path):
            logging.info('Pending to remove qmlformat backup file: %s.', backup_file_path)
            os.remove(backup_file_path)
    return 0


def main(args) -> int:
    logging.basicConfig(level=logging.INFO)
    if args.all:
        from const import path_const  # pylint: disable=import-outside-toplevel
        file_paths = []
        for root, _, file_names in os.walk(path_const.VIEW_DIR):
            if os.path.basename(root) in EXCLUDE_DIR_NAMES:
                continue
            for file_name in file_names:
                if not file_name.endswith(QML_EXT):
                    continue
                file_path = os.path.join(root, file_name)
                file_paths.append(file_path)
        return format_files(file_paths, args.dont_delete_backup_file)
    return format_files(filter(lambda file_name: file_name.endswith(QML_EXT), args.files), args.dont_delete_backup_file)


if __name__ == '__main__':
    check_python_path()
    sys.exit(main(get_argument_parser().parse_args(sys.argv[1:])))
