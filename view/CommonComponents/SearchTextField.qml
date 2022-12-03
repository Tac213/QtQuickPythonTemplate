import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RowLayout {
    id: root
    property alias searchButtonVisible: searchButton.visible
    property alias text: textField.text
    signal textEdited(text: string)
    signal editingFinished(text: string)
    signal accepted(text: string)

    TextField {
        id: textField
        Layout.fillWidth: true
        placeholderText: qsTr("search...")
        onTextEdited: () => {
            root.textEdited(this.text);
        }
        onEditingFinished: () => {
            root.editingFinished(this.text);
        }
        onAccepted: () => {
            root.accepted(this.text);
        }
    }
    ToolButton {
        id: searchButton
        display: AbstractButton.IconOnly
        implicitWidth: 28
        icon {
            source: "qrc:/resource/svg/search.svg"
        }
        ToolTip {
            visible: parent.hovered
            text: qsTr("search")
            delay: 1000
            timeout: 5000
        }
    }
}
