import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "CommonComponents" as CommonComponents
import "script/js-console.js" as Util

Window {
    id: root

    title: qsTr("JavaScript Console")
    width: 640
    height: 480
    visible: false
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 9
        RowLayout {
            Layout.fillWidth: true
            CommonComponents.HistoryRollbackTextField {
                id: input
                Layout.fillWidth: true
                focus: true
                placeholderText: "input JavaScript code to debug..."
                onAccepted: {
                    // call our evaluation function on root
                    const script = this.text.trim();
                    root.jsCall(script);
                    this.text = '';
                }
            }
            Button {
                text: qsTr("Send")
                onClicked: {
                    // call our evaluation function on root
                    root.jsCall(input.text);
                    input.text = '';
                }
            }
        }
        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Rectangle {
                anchors.fill: parent
                color: '#333'
                border.color: Qt.darker(color)
                opacity: 0.2
                radius: 2
            }
            ScrollView {
                id: scrollView
                anchors.fill: parent
                anchors.margins: 9
                ListView {
                    id: resultView
                    model: ListModel {
                        id: outputModel
                    }
                    delegate: ColumnLayout {
                        id: delegate
                        required property var model
                        width: ListView.view.width
                        Label {
                            Layout.fillWidth: true
                            color: 'green'
                            text: "> " + delegate.model.expression
                        }
                        Label {
                            Layout.fillWidth: true
                            color: delegate.model.error === "" ? 'blue' : 'red'
                            text: delegate.model.error === "" ? "" + delegate.model.result : delegate.model.error
                        }
                        Rectangle {
                            height: 1
                            Layout.fillWidth: true
                            color: '#333'
                            opacity: 0.2
                        }
                    }
                }
            }
        }
    }

    function jsCall(exp) {
        const data = Util.call(exp);
        // insert the result at the beginning of the list
        outputModel.insert(0, data);
    }
}
