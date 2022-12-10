# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import sys
import os
import subprocess

import deploy_utils
import shader_baker

QRC_FILE_NAME = 'resource_view.qrc'
PY_RC_FILE_NAME = 'resource_view_rc.py'
QT_QUICK_CONTROLS_CONF_FILE_NAME = 'qtquickcontrols2.conf'
EXCLUDE_DIR_NAMES = (
    '.git',
    '.svn',
    '__pycache__',
)
EXCLUDE_EXTS = (
    '.py',
    '.pyc',
    '.qrc',
    '.qml~',
)


def generate_qrc_file() -> int:
    from const import app_const, path_const  # pylint: disable=import-outside-toplevel
    import deploy_env  # pylint: disable=import-outside-toplevel
    qt_quick_controls_conf_file_relpath = ''
    content = '<!DOCTYPE RCC><RCC version="1.0">\n'

    if os.path.exists(path_const.RESOURCE_DIR):
        content += f'<qresource prefix="{app_const.RESOURCE_PREFIX}">\n'
        for root, _, file_names in os.walk(path_const.RESOURCE_DIR):
            if os.path.basename(root) in EXCLUDE_DIR_NAMES:
                continue
            for file_name in file_names:
                if file_name.endswith(EXCLUDE_EXTS):
                    continue
                file_path = os.path.join(root, file_name)
                file_relpath = os.path.relpath(file_path, deploy_env.root_path).replace(os.path.sep, '/')
                if file_name == QT_QUICK_CONTROLS_CONF_FILE_NAME:
                    qt_quick_controls_conf_file_relpath = file_relpath
                    continue
                alias = os.path.relpath(file_path, path_const.RESOURCE_DIR).replace(os.path.sep, '/')
                content += f'    <file alias="{alias}">{file_relpath}</file>\n'
        content += '</qresource>\n'

    if os.path.exists(path_const.VIEW_DIR):
        content += f'<qresource prefix="{app_const.VIEW_PREFIX}">\n'
        for root, _, file_names in os.walk(path_const.VIEW_DIR):
            if os.path.basename(root) in EXCLUDE_DIR_NAMES:
                continue
            for file_name in file_names:
                if file_name.endswith(EXCLUDE_EXTS):
                    continue
                file_path = os.path.join(root, file_name)
                file_relpath = os.path.relpath(file_path, deploy_env.root_path).replace(os.path.sep, '/')
                if file_name == QT_QUICK_CONTROLS_CONF_FILE_NAME:
                    qt_quick_controls_conf_file_relpath = file_relpath
                    continue
                alias = os.path.relpath(file_path, path_const.VIEW_DIR).replace(os.path.sep, '/')
                content += f'    <file alias="{alias}">{file_relpath}</file>\n'
        content += '</qresource>\n'

    if os.path.exists(path_const.SHADER_DIR):
        deploy_env.logger.info('Found shader directory, try to bake shaders.')
        returncode = shader_baker.main()
        if returncode:
            deploy_env.logger.error('Failed to bake shader. See logs above.')
            return returncode
        content += f'<qresource prefix="{app_const.SHADER_PREFIX}">\n'
        for root, _, file_names in os.walk(path_const.SHADER_DIR):
            if os.path.basename(root) in EXCLUDE_DIR_NAMES:
                continue
            for file_name in file_names:
                if not file_name.endswith(shader_baker.QSB_EXT):
                    continue
                file_path = os.path.join(root, file_name)
                file_relpath = os.path.relpath(file_path, deploy_env.root_path).replace(os.path.sep, '/')
                alias = os.path.relpath(file_path, path_const.SHADER_DIR).replace(os.path.sep, '/')
                content += f'    <file alias="{alias}">{file_relpath}</file>\n'
        content += '</qresource>\n'

    if qt_quick_controls_conf_file_relpath:
        content += '<qresource prefix="/">\n'
        content += f'    <file alias="{QT_QUICK_CONTROLS_CONF_FILE_NAME}">{qt_quick_controls_conf_file_relpath}</file>\n'
        content += '</qresource>\n'

    content += '</RCC>\n'

    qrc_file_path = os.path.join(deploy_env.root_path, QRC_FILE_NAME)
    with open(qrc_file_path, 'w+', encoding='utf-8') as fp:
        fp.write(content)

    return 0


def compile_qrc_file() -> int:
    import deploy_env  # pylint: disable=import-outside-toplevel
    pyside6_rcc_executable = os.path.join(os.path.dirname(sys.executable), 'pyside6-rcc')
    command = f'{pyside6_rcc_executable} {QRC_FILE_NAME} > {PY_RC_FILE_NAME}'
    deploy_env.logger.info('Running command "%s" in "%s"', command, deploy_env.root_path)
    stdout = deploy_utils.LogPipe(deploy_env.logger.info)
    stderr = deploy_utils.LogPipe(deploy_env.logger.error)
    with subprocess.Popen(
            command,
            stdout=stdout,
            stderr=stderr,
            shell=True,
            cwd=deploy_env.root_path,
    ) as p:
        p.wait()
        stdout.close()
        stderr.close()
    return p.returncode


def main() -> int:
    import deploy_env  # pylint: disable=import-outside-toplevel
    deploy_env.logger.info('Generating %s', QRC_FILE_NAME)
    returncode = generate_qrc_file()
    if returncode:
        return returncode
    deploy_env.logger.info('Generating %s', PY_RC_FILE_NAME)
    return compile_qrc_file()


if __name__ == '__main__':
    sys.exit(main())
