import QtQuick
import QtQuick.Controls

ScrollView {
    id: root
    enum MessageType {
        Normal = 1,
        Warning,
        Error = 4
    }

    property var outputTexts: []
    property var currentMessageType: OutputTextControl.MessageType.Normal | OutputTextControl.MessageType.Warning | OutputTextControl.MessageType.Error
    property var searchRE: null
    property var matchIndexStack: []
    property int currentSearchIndex: -1

    TextArea {
        id: textArea

        implicitWidth: parent.width
        textFormat: TextEdit.RichText
        wrapMode: Text.Wrap
        readOnly: true

        onLinkActivated: link => {
            root.handleLinkActivated(link);
        }
    }

    function clearText() {
        textArea.clear();
        this.outputTexts.length = 0;
    }

    function setCurrentMessageType(msgType) {
        if (this.currentMessageType === msgType) {
            return;
        }
        textArea.clear();
        for (const [mType, text] of this.outputTexts) {
            if (mType & msgType) {
                textArea.append(text);
            }
        }
        this.currentMessageType = msgType;
    }

    function escapeHtml(unsafe) {
        return unsafe.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
    }

    function addItem(item, msgType = OutputTextControl.MessageType.Normal) {
        let colorName = 'grey';
        if (msgType === OutputTextControl.MessageType.Normal) {
            colorName = '#000000';
        } else if (msgType === OutputTextControl.MessageType.Warning) {
            colorName = '#ed7d31';
        } else if (msgType === OutputTextControl.MessageType.Error) {
            colorName = '#ff0000';
        }
        let text = escapeHtml(item);
        text = _processText(text);
        text = `<span style="color:${colorName};white-space:pre;">${text}</span>`;
        this._addText(text, msgType);
    }

    function addHtml(htmlText, msgType = OutputTextControl.MessageType.Normal) {
        this._addText(htmlText, msgType);
    }

    function handleLinkActivated(link) {
        let url = decodeURI(link).replace(/<br\/>/g, '\n');
        if (url.startsWith('#wrap:'))
        // TODO
        {
        } else {
            url = url.substring(1);  // remove '#'
            const idx = url.lastIndexOf('.');
            if (idx === -1 || idx >= url.length) {
                return;
            }
            // const [fileName, lineNumber] = [url.substring(0, idx), Number(url.substring(idx + 1, url.length))];
        }
    }

    function _addText(text, msgType = OutputTextControl.MessageType.Normal) {
        if (!text) {
            return;
        }
        this.outputTexts.push([msgType, text]);
        if (msgType & this.currentMessageType) {
            textArea.append(text);
        }
    }

    function _processText(text, color = '#1a77e6') {
        const traceRE = /(File &quot;(.+?)&quot;, line (\d{1,5}), in (.+?))$/g;
        return text.replace(traceRE, (match, line, fileName, lineNumber) => {
                const link = encodeURI(`${fileName.replace(/\\/g, '/')}.${lineNumber}`);
                return line.replace(fileName, `<a href=\"#${link}\" style="color:${color};white-space:pre;">${fileName}</a>`);
            }).replace(/\n/g, '<br/>');
    }

    function findText(text) {
        if (text.length <= 1) {
            this.searchRE = null;
            this.matchIndexStack.length = 0;
            this.currentSearchIndex = -1;
            this.disableAllHighlight();
            return;
        }
        this.highlightText(text);
        this.searchRE = new RegExp(text, 'gim');
        this.matchIndexStack.length = 0;
        this.currentSearchIndex = -1;
        this.find();
    }

    function find(backward = false) {
        if (!this.searchRE) {
            return;
        }
        if (this.matchIndexStack.length === 0) {
            let match;
            while (match = this.searchRE.exec(textArea.getText(0, textArea.length))) {
                textArea.cursorPosition = match.index;
                textArea.moveCursorSelection(this.searchRE.lastIndex, TextEdit.SelectCharacters);
                this.matchIndexStack.push([match.index, this.searchRE.lastIndex]);
            }
        }
        if (this.matchIndexStack.length === 0) {
            return;
        }
        if (backward) {
            this.currentSearchIndex -= 1;
            if (this.currentSearchIndex < 0) {
                this.currentSearchIndex = this.matchIndexStack.length - 1;
            }
        } else {
            this.currentSearchIndex += 1;
            if (this.currentSearchIndex >= this.matchIndexStack.length) {
                this.currentSearchIndex = 0;
            }
        }
        textArea.cursorPosition = this.matchIndexStack[this.currentSearchIndex][0];
        textArea.moveCursorSelection(this.matchIndexStack[this.currentSearchIndex][1], TextEdit.SelectCharacters);
    }

    function findPrev() {
        this.find(true);
    }

    function findNext() {
        this.find();
    }

    function highlightText(text) {
        this.disableAllHighlight();
        if (text.length <= 1) {
            return;
        }
        const findRE = new RegExp(text, 'gim');
        const currentText = textArea.getFormattedText(0, textArea.length);
        const newText = currentText.replace(findRE, findText => {
                return `<span style='background-color:#ffff00'>${findText}</span>`;
            });
        textArea.text = newText;
    }

    function disableAllHighlight() {
        const findRE = /background-color:#ffff00;/gm;
        const currentText = textArea.getFormattedText(0, textArea.length);
        const newText = currentText.replace(findRE, findText => {
                return '';
            });
        textArea.text = newText;
    }
}
