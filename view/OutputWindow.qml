import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Python.InteractiveInterpreter
import "OutputWindowComponents" as OutputWindowComponents
import "CommonComponents" as CommonComponents

Window {
    id: root

    title: qsTr("Console")
    width: 640
    height: 480
    visible: false

    ColumnLayout {
        anchors.fill: parent
        ToolBar {
            Layout.fillWidth: true
            RowLayout {
                anchors.fill: parent
                ToolButton {
                    id: showMenuButton
                    display: AbstractButton.IconOnly
                    implicitWidth: 28
                    icon {
                        source: "resource:/svg/filter.svg"
                    }
                    ToolTip {
                        visible: parent.hovered
                        text: qsTr("show output type menu")
                        delay: 1000
                        timeout: 5000
                    }
                    onClicked: () => {
                        messageMenu.popup();
                    }
                }
                ToolButton {
                    id: clearButton
                    display: AbstractButton.IconOnly
                    implicitWidth: 28
                    icon {
                        source: "resource:/svg/clear.svg"
                    }
                    ToolTip {
                        visible: parent.hovered
                        text: qsTr("clear output window")
                        delay: 1000
                        timeout: 5000
                    }
                    onClicked: () => {
                        outputText.clearText();
                    }
                }
                OutputWindowComponents.FindControl {
                    id: findWidget
                    Layout.fillWidth: true
                    onFindTextChanged: (text) => {
                        outputText.findText(text);
                    }
                    onPrevClicked: () => {
                        outputText.findPrev();
                    }
                    onNextClicked: () => {
                        outputText.findNext();
                    }
                }
                ToolButton {
                    id: prevButton
                    display: AbstractButton.IconOnly
                    implicitWidth: 28
                    icon {
                        source: "resource:/svg/dropup.svg"
                    }
                    ToolTip {
                        visible: parent.hovered
                        text: qsTr("previous match")
                        delay: 1000
                        timeout: 5000
                    }
                    onClicked: () => {
                        findWidget.onPrev();
                    }
                }
                ToolButton {
                    id: nextButton
                    display: AbstractButton.IconOnly
                    implicitWidth: 28
                    icon {
                        source: "resource:/svg/dropdown.svg"
                    }
                    ToolTip {
                        visible: parent.hovered
                        text: qsTr("next match")
                        delay: 1000
                        timeout: 5000
                    }
                    onClicked: () => {
                        findWidget.onNext();
                    }
                }
            }
        }
        OutputWindowComponents.OutputTextControl {
            id: outputText
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
        CommonComponents.HistoryRollbackTextField {
            id: consoleInput
            Layout.fillWidth: true
            placeholderText: "input python code to debug..."
            onAccepted: () => {
                const script = this.text.trim();
                root.showNormalMessage(`>>> ${script}`);
                interactiveInterpreter.interpret_script(script);
                this.text = '';
            }
        }
    }
    InteractiveInterpreter {
        id: interactiveInterpreter
    }
    Connections {
        target: outputWindowBridge
        function onShowNormalMessage(msg) {
            showNormalMessage(msg);
        }

        function onShowWarningMessage(msg) {
            showWarningMessage(msg);
        }

        function onShowErrorMessage(msg) {
            showErrorMessage(msg);
        }
    }
    Menu {
        id: messageMenu
        MenuItem {
            action: normalMessageAction
        }
        MenuItem {
            action: warningMessageAction
        }
        MenuItem {
            action: errorMessageAction
        }
    }
    Action {
        id: normalMessageAction
        text: qsTr("Normal")
        checkable: true
        checked: true
        onTriggered: (source) => {
            handleMessageTypeFilter();
        }
    }
    Action {
        id: warningMessageAction
        text: qsTr("Warning")
        checkable: true
        checked: true
        onTriggered: () => {
            handleMessageTypeFilter();
        }
    }
    Action {
        id: errorMessageAction
        text: qsTr("Error")
        checkable: true
        checked: true
        onTriggered: () => {
            handleMessageTypeFilter();
        }
    }

    function showMessage(msg, msgType=OutputWindowComponents.OutputTextControl.MessageType.Normal) {
        outputText.addItem(msg, msgType);
    }

    function showNormalMessage(msg) {
        showMessage(msg, OutputWindowComponents.OutputTextControl.MessageType.Normal);
    }

    function showWarningMessage(msg) {
        showMessage(msg, OutputWindowComponents.OutputTextControl.MessageType.Warning);
    }

    function showErrorMessage(msg) {
        showMessage(msg, OutputWindowComponents.OutputTextControl.MessageType.Error);
    }

    function handleMessageTypeFilter() {
        let msgType = 0;
        if (normalMessageAction.checked) {
            msgType |= OutputWindowComponents.OutputTextControl.MessageType.Normal;
        }
        if (warningMessageAction.checked) {
            msgType |= OutputWindowComponents.OutputTextControl.MessageType.Warning;
        }
        if (errorMessageAction.checked) {
            msgType |= OutputWindowComponents.OutputTextControl.MessageType.Error;
        }
        outputText.setCurrentMessageType(msgType);
    }

}
