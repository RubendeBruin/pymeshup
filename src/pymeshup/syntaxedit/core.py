from PySide6 import QtGui
from PySide6.QtGui import QTextCursor
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTextEdit

from pygments.styles import get_style_by_name


from pymeshup.syntaxedit.highlightslot import HighlightSlot


class SyntaxEdit(QTextEdit):
    def __init__(
        self,
        content="",
        parent=None,
        font="Courier New",
        font_size=13,
        syntax="Markdown",
        theme="solarized-light",
        indentation_size=4,
        use_theme_background=True,
        use_smart_indentation=True,
    ):
        super().__init__("", parent)

        self._indentation_size = indentation_size
        self._use_smart_indentation = use_smart_indentation

        self._font = font
        self._font_size = font_size
        self._setFontValues()

        self._syntax = syntax
        self._theme = theme

        self._use_theme_background = use_theme_background

        self._updateBackgroundColor()

        self._highlight_slot = HighlightSlot(self)
        self.textChanged.connect(self._highlight_slot.execute)

        self.setPlainText(content)

    def _updateBackgroundColor(self):
        if self._use_theme_background:
            style = get_style_by_name(self._theme)
            self.setStyleSheet(
                f"QTextEdit {{ background-color: {style.background_color}; }}"
            )
        else:
            self.setStyleSheet("")

    def _setFontValues(self):
        self.setFont(QtGui.QFont(self._font, self._font_size))
        self.setTabStopDistance(
            QtGui.QFontMetricsF(self.font()).horizontalAdvance(" ") * 4
        )

    def setSyntax(self, syntax):
        self._syntax = syntax
        self.textChanged.emit()

    def syntax(self):
        return self._syntax

    def theme(self):
        return self._theme

    def setTheme(self, theme):
        self._theme = theme
        self._updateBackgroundColor()
        self.textChanged.emit()

    def indentationSize(self):
        return self._indentation_size

    def editorFont(self):
        return self.currentFont().family()

    def editorFontSize(self):
        return self.currentFont().pointSize()

    def setEditorFontSize(self, size):
        self._font_size = size
        self._setFontValues()

    def cursorPosition(self):
        return self.textCursor().position()

    def setCursorPosition(self, position):
        cursor = self.textCursor()
        cursor.setPosition(position)
        self.setTextCursor(cursor)

    def setContents(self, contents):
        self.setPlainText(contents)


    def keyPressEvent(self, event):
        if self._use_smart_indentation and event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
            current_line_text = cursor.selectedText()

            # indentation may be tabs or spaces, get the leading whitespace
            indent = ""
            for char in current_line_text:
                if char == " " or char == "\t":
                    indent += char
                else:
                    break

            # if the previous line ended with a colon, indent the new line by one level
            if current_line_text.strip().endswith(":"):
                if '\t' in indent:
                    indent += '\t'
                else:
                    indent += " " * self._indentation_size

            super().keyPressEvent(event)
            self.insertPlainText(indent)
        else:
            super().keyPressEvent(event)
