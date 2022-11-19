# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import sys
import os


def check_python_path():
    workspace_folder = os.path.dirname(__file__)
    source_folder = os.path.join(workspace_folder, 'source')
    if source_folder in sys.path:
        return
    sys.path.insert(source_folder)


def main():
    import application  # pylint: disable=import-outside-toplevel

    args = application.get_argument_parser().parse_args(sys.argv[1:])
    application.main(args)


if __name__ == '__main__':
    check_python_path()
    main()
