import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../CommonComponents" as CommonComponents

Frame {
    id: root
    property alias text: textField.text
    signal nextClicked
    signal prevClicked
    signal closeClicked
    signal findTextChanged(string text)

    RowLayout {
        anchors.fill: parent
        spacing: 0
        CommonComponents.SearchTextField {
            id: textField
            Layout.fillWidth: true
            searchButtonVisible: false
            onTextEdited: text => {
                root.findTextChanged(text);
            }
            onAccepted: text => {
                root.nextClicked();
            }
        }
    }

    function onNext() {
        this.nextClicked();
    }

    function onPrev() {
        this.prevClicked();
    }
}
