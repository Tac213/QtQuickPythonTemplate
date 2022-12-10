# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import sys
import os
import subprocess

from PySide6 import QtQuick

import deploy_utils

EXCLUDE_DIR_NAMES = (
    '.git',
    '.svn',
    '__pycache__',
)
VALID_SHADER_SRC_EXTS = (
    '.vert',  # vertex shader
    '.frag',  # fragment shader
    '.comp',  # compute shader
)
QSB_EXT = '.qsb'


def get_qt_install_dir():
    if sys.platform == 'win32':
        return 'C:\\Qt'
    return os.path.expanduser('~/Qt')


def find_qsb_executable():
    qt_install_dir = get_qt_install_dir()
    path_seg = ['QtDesignStudio', 'qt6_design_studio_reduced_version', 'bin', 'qsb']
    if sys.platform != 'darwin':
        path_seg.insert(0, 'Tools')
    if sys.platform == 'win32':
        path_seg[-1] += '.exe'
    qsb_executable = os.path.join(qt_install_dir, *path_seg)
    if not os.path.exists(qsb_executable):
        return ''
    return qsb_executable


def get_shading_language_args() -> list:
    shading_language_args = []
    graphics_api = QtQuick.QQuickView.graphicsApi()
    if graphics_api == QtQuick.QSGRendererInterface.GraphicsApi.Direct3D11:
        shading_language_args.extend(('--hlsl', '50'))
    elif graphics_api == QtQuick.QSGRendererInterface.GraphicsApi.Metal:
        shading_language_args.extend(('--msl', '12'))
    elif graphics_api == QtQuick.QSGRendererInterface.GraphicsApi.OpenGL:
        shading_language_args.extend(('--glsl', '310es,430'))
    return shading_language_args


def main() -> int:
    from const import path_const  # pylint: disable=import-outside-toplevel
    import deploy_env  # pylint: disable=import-outside-toplevel
    qsb_executable = find_qsb_executable()
    if not qsb_executable:
        deploy_env.logger.error(
            'Cannot find qsb executable, failed to bake shaders. If you have a qsb executable, modify find_qsb executable function in %s.',
            __file__)
        return -1
    shading_language_args = get_shading_language_args()
    stdout = deploy_utils.LogPipe(deploy_env.logger.info)
    stderr = deploy_utils.LogPipe(deploy_env.logger.error)
    for root, _, file_names in os.walk(path_const.SHADER_DIR):
        if os.path.basename(root) in EXCLUDE_DIR_NAMES:
            continue
        for file_name in file_names:
            if not file_name.endswith(VALID_SHADER_SRC_EXTS):
                continue
            file_path = os.path.join(root, file_name)
            output_file_path = file_path + QSB_EXT
            command_args = [
                qsb_executable,
                file_path,
                '--output',
                output_file_path,
            ]
            command_args.extend(shading_language_args)
            deploy_env.logger.info('Running command "%s" in "%s"', ' '.join(command_args), deploy_env.root_path)
            with subprocess.Popen(
                    command_args,
                    stdout=stdout,
                    stderr=stderr,
                    cwd=deploy_env.root_path,
            ) as p:
                p.wait()
            if p.returncode:
                stdout.close()
                stderr.close()
                return p.returncode
    stdout.close()
    stderr.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
