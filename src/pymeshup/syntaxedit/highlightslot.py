from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name


class HighlightSlot:
    def __init__(self, widget):
        self._widget = widget

    def widget(self):
        return self._widget

    def execute(self):
        font = self.widget().editorFont()

        markup = highlight(
            self.widget().toPlainText(),
            get_lexer_by_name(
                self.widget().syntax(),
                stripnl=False,
                ensurenl=False,
            ),
            HtmlFormatter(
                lineseparator="<br />",
                prestyles=f"white-space:pre-wrap; font-family: '{font}';",
                noclasses=True,
                nobackground=True,
                style=self.widget().theme(),
            ),
        )

        position = self.widget().cursorPosition()
        # get scroll position
        scroll_position = self.widget().verticalScrollBar().value()

        self.widget().blockSignals(True)
        self.widget().setHtml(markup)
        self.widget().blockSignals(False)

        self.widget().setCursorPosition(position)

        # restore scroll position
        self.widget().verticalScrollBar().setValue(scroll_position)

