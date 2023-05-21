# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import sys
import os
import argparse
import shutil

import PyInstaller.__main__

from qt_quick_python_tools import resource_compiler
from qt_quick_python_tools import deploy_env
from qt_quick_python_tools.spec import nuitka_spec


def get_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool", "-t", type=str, choices=["pyinstaller", "nuitka"], default="pyinstaller")
    parser.add_argument("--variant", "-v", type=str, choices=["debug", "release"], default="release")
    parser.add_argument("--distpath", "-d", type=str, default=os.path.join(os.path.dirname(__file__), "..", "..", "deployment", "dist"))
    parser.add_argument("--workpath", "-b", type=str, default=os.path.join(os.path.dirname(__file__), "..", "..", "deployment", "build"))
    return parser


def main(args):
    root_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if os.path.normpath(os.getcwd()) != root_path:
        deploy_env.logger.error("Deployment should be performed in working directory: %s", root_path)
        sys.exit(-1)
    deploy_env.logger.info("Start deployment.")
    deploy_env.logger.info("tool: %s", args.tool)
    deploy_env.logger.info("variant: %s", args.variant)
    deploy_env.logger.info("distpath: %s", args.distpath)
    deploy_env.logger.info("workpath: %s", args.workpath)
    returncode = resource_compiler.main()
    if returncode:
        deploy_env.logger.error("Failed to compile resource. See logs above.")
        sys.exit(returncode)
    if os.path.exists(args.workpath):
        deploy_env.logger.info("Workpath '%s' exists, pending to remove it.", args.workpath)
        shutil.rmtree(args.workpath)
    if args.tool == "pyinstaller":
        PyInstaller.__main__.run(
            [
                os.path.join(os.path.dirname(__file__), "spec", f"{sys.platform}.spec"),
                "--distpath",
                args.distpath,
                "--workpath",
                args.workpath,
                "--noconfirm",
            ]
        )
    else:
        sys.exit(nuitka_spec.deploy_with_nuitka())


if __name__ == "__main__":
    main(deploy_env.deployment_args)
