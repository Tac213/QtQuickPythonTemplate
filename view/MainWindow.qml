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
            title: qsTr("&File")
            MenuItem {
                text: qsTr("&Exit")
                onTriggered: Qt.quit()
            }
        }
        Menu {
            title: qsTr("&Developer")
            MenuItem {
                text: qsTr("&Toggle Console")
                onTriggered: toggleConsoleWindow()
            }
        }
    }

    Item {
        focus: true
        Keys.onPressed: (event) => {
            if (event.key === Qt.Key_QuoteLeft) {
                toggleConsoleWindow();
            }
        }

    }

    OutputWindow {
        id: consoleWindow
    }

    function toggleConsoleWindow() {
        consoleWindow.visible = !consoleWindow.visible;
    }
}
