import QtQuick
import QtQuick.Window
import QtQuick.Controls

ApplicationWindow {
    id: root

    title: qsTr("QtQuickPythonTemplate")
    width: 800
    height: 600
    visible: true

    menuBar: MenuBar {
        Menu {
            title: qsTr("File")
            MenuItem {
                text: qsTr("Exit")
                onTriggered: Qt.quit()
            }
        }
    }
}
