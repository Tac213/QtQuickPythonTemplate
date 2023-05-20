# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import sys
from qt_quick_python_template import application


def main():
    args = application.get_argument_parser().parse_args(sys.argv[1:])
    sys.exit(application.main(args))


if __name__ == "__main__":
    main()
