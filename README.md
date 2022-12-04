# QtQuickPythonTemplate

A Template repository for QtQuick Python.

## Prerequisites

-   Git 2.32 (or more recent)
-   Python 3.11.0 (or more recent)

## Setup Development Environment

Recommended IDE: [Visual Studio Code](https://code.visualstudio.com/)

To setup Development Environment, run the following commands:

```bash
# git clone this repository
cd QtQuickPythonTemplate
# create venv
python3 -m venv .venv
# activate venv
source .venv/bin/activate
# for Windows Command Prompt, run the following command to activate venv
# .venv\Scripts\activate.bat
# for Windows Powershell, run the following command to activate venv
# .venv\Scripts\Activate.ps1
# for Winows Git Bash, run the following command to activate venv
# source .venv/Scripts/activate
pip3 install -r requirements.txt
# deactivate venv
deactivate
# open current folder using VSCode
code .
```

After opening the folder, install the following extensions:

-   [ms-python.python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
-   [ms-python.vscode-pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
-   [seanwu.vscode-qt-for-python](https://marketplace.visualstudio.com/items?itemName=seanwu.vscode-qt-for-python)
-   [esbenp.prettier-vscode](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)

These extensions have been written in `.vscode/extensions.json`, you can also click `Yes` when VSCode ask you whether to install the recommended extensions, which makes it easier to install all the above extensions.

The next step is to select the interpreter under `.venv` folder as the development interpreter. Simply press `Ctrl + Shift + P`, then enter `Python: Select Interpreter` command.

Finally, press `F5`. The application should be launched in debug mode.

## Usage

1. Clone or download this repository
2. Rename the root folder
3. Change the `APP_NAME` and `ORGANIZATION_NAME` variable in `source/const/app_const.py`
4. Change the icon in `resouce/icon.jpg`, change it to a `.ico` format icon will be better(for deployment)
5. Upgrade dependencies: PySide6, pylint, yapf, pyinstaller

## Deployment

The major 3 operate systems: Windows, MacOS, Linux(Ubuntu / Debian), is supported.

To deploy the application, simply press `Ctrl + P` in VSCode, then enter `task Deploy(Release)`. If the task is performed successfully, the application will be deployed under: `${workspaceFolder}/deployment/dist`.

See spec files under `${workspaceFolder}/deployment/spec` for more information.
