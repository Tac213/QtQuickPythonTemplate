import QtQuick
import QtQuick.Controls

TextField {
    id: root
    property var history: [""]
    property int historyIndex: 0
    property int stackSize: 100
    Keys.onPressed: event => {
        if (event.key === Qt.Key_Up) {
            if (this.history.length === 0) {
                this.history[0] = this.text;
            }
            this.historyIndex += 1;
            this.historyIndex = Math.min(this.history.length - 1, this.historyIndex);
            this.text = this.history[this.historyIndex];
        } else if (event.key === Qt.Key_Down) {
            this.historyIndex -= 1;
            this.historyIndex = Math.max(0, this.historyIndex);
            this.text = this.history[this.historyIndex];
        }
    }
    onAccepted: () => {
        const value = this.text.trim();
        if (!value) {
            return;
        }
        if (this.history.length === 1 || this.history.length > 1 && this.history[1] !== value) {
            this.history.splice(1, 0, value);
            if (this.history.length > this.stackSize) {
                this.history.pop();
            }
        }
        this.historyIndex = 0;
    }
}
