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


if __name__ == '__main__':
    import sys
    from pathlib import Path

    import pygments
    from PySide6.QtWidgets import (
        QApplication,
        QComboBox,
        QHBoxLayout,
        QMainWindow,
        QVBoxLayout,
        QWidget,
        QSpinBox,
    )


    app = QApplication(sys.argv)


    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            contents = Path(__file__).read_text()

            self.editor = SyntaxEdit(contents, syntax="Python", use_smart_indentation=True)
            self.editor.textChanged.connect(self.editor_changed)

            style_language = QHBoxLayout()
            style_language.setContentsMargins(0, 0, 0, 0)

            self.lexers = QComboBox()
            self.lexers.setEditable(False)
            self.lexers.addItems([i[0] for i in pygments.lexers.get_all_lexers()])
            self.lexers.setCurrentText(self.editor.syntax())
            self.lexers.currentIndexChanged.connect(self.language_changed)

            self.styles = QComboBox()
            self.styles.setEditable(False)
            self.styles.addItems(pygments.styles.get_all_styles())
            self.styles.setCurrentText(self.editor.theme())
            self.styles.currentIndexChanged.connect(self.style_changed)

            self.size = QSpinBox()
            self.size.setMinimum(10)
            self.size.setMaximum(30)
            self.size.setValue(self.editor.editorFontSize())
            self.size.valueChanged.connect(self.editor.setEditorFontSize)

            style_language.addWidget(self.lexers)
            style_language.addWidget(self.styles)
            style_language.addWidget(self.size)

            style_languagewidget = QWidget()
            style_languagewidget.setLayout(style_language)

            layout = QVBoxLayout()
            layout.addWidget(self.editor)
            layout.addWidget(style_languagewidget)

            widget = QWidget()
            widget.setLayout(layout)

            self.setCentralWidget(widget)

        def language_changed(self):
            self.editor.setSyntax(self.lexers.currentText())
            print("Language changed")

        def style_changed(self):
            self.editor.setTheme(self.styles.currentText())
            print("Style changed")

        def editor_changed(self):
            print("editor changed")
            print(self.editor.toPlainText())


    window = MainWindow()
    window.show()
    app.exec()