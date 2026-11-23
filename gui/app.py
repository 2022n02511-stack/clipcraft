import sys

from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QTextEdit,
    QListWidget, QListWidgetItem, QSplitter, QMessageBox
)

from core.dbus_server import process_text
from storage.history import save, get_recent, clear


class FormatWorker(QThread):
    finished = Signal(str)
    failed = Signal(str)

    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        try:
            result = process_text(self.text)
            self.finished.emit(result or "")
        except Exception as error:
            self.failed.emit(str(error))


class ClipCraftWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ClipCraft")
        self.resize(1000, 650)

        self.clipboard = QApplication.clipboard()
        self.original_text = None
        self.formatted_text = None
        self.worker = None

        self.build_ui()
        self.load_clipboard()
        self.load_history()

    def build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(14)

        header = QHBoxLayout()

        title = QLabel("ClipCraft")
        title.setStyleSheet("font-size: 26px; font-weight: bold;")

        subtitle = QLabel("Your clipboard, intelligently formatted.")
        subtitle.setStyleSheet("color: gray; font-size: 13px;")

        title_layout = QVBoxLayout()
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        header.addLayout(title_layout)
        header.addStretch()

        self.status = QLabel("Ready")
        self.status.setStyleSheet("color: gray;")
        header.addWidget(self.status)

        main_layout.addLayout(header)

        splitter = QSplitter(Qt.Horizontal)

        editor_panel = QWidget()
        editor_layout = QVBoxLayout(editor_panel)

        editor_layout.addWidget(QLabel("Clipboard content"))

        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Copy text or paste it here...")
        editor_layout.addWidget(self.editor)

        buttons = QHBoxLayout()

        self.refresh_button = QPushButton("Read Clipboard")
        self.refresh_button.clicked.connect(self.load_clipboard)

        self.format_button = QPushButton("Format Clipboard")
        self.format_button.setMinimumHeight(38)
        self.format_button.clicked.connect(self.format_clipboard)

        self.undo_button = QPushButton("Undo")
        self.undo_button.clicked.connect(self.undo)
        self.undo_button.setEnabled(False)

        buttons.addWidget(self.refresh_button)
        buttons.addWidget(self.format_button)
        buttons.addWidget(self.undo_button)

        editor_layout.addLayout(buttons)

        history_panel = QWidget()
        history_layout = QVBoxLayout(history_panel)

        history_header = QHBoxLayout()
        history_header.addWidget(QLabel("Clipboard History"))
        history_header.addStretch()

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_history)
        history_header.addWidget(self.clear_button)

        history_layout.addLayout(history_header)

        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.restore_history)
        history_layout.addWidget(self.history_list)

        restore_button = QPushButton("Restore Selected")
        restore_button.clicked.connect(self.restore_selected)
        history_layout.addWidget(restore_button)

        splitter.addWidget(editor_panel)
        splitter.addWidget(history_panel)
        splitter.setSizes([680, 280])

        main_layout.addWidget(splitter)

        footer = QLabel(
            "Manual mode: your clipboard changes only when you choose to format it."
        )
        footer.setStyleSheet("color: gray; font-size: 11px;")
        main_layout.addWidget(footer)

        self.setStyleSheet("""
            QMainWindow {
                background: palette(window);
            }
            QPushButton {
                padding: 8px 12px;
                border-radius: 6px;
            }
            QTextEdit, QListWidget {
                border: 1px solid palette(mid);
                border-radius: 7px;
                padding: 8px;
            }
        """)

    def load_clipboard(self):
        text = self.clipboard.text()
        self.editor.setPlainText(text)
        self.status.setText("Clipboard loaded")

    def format_clipboard(self):
        if self.worker is not None and self.worker.isRunning():
            return

        original = self.editor.toPlainText()

        if not original.strip():
            self.status.setText("Nothing to format")
            return

        self.original_text = original
        self.format_button.setEnabled(False)
        self.refresh_button.setEnabled(False)
        self.status.setText("Formatting...")

        self.worker = FormatWorker(original)
        self.worker.finished.connect(self.format_finished)
        self.worker.failed.connect(self.format_failed)
        self.worker.start()

    def format_finished(self, formatted):
        original = self.original_text

        if not formatted:
            self.status.setText("Formatting returned empty text")
            self.format_button.setEnabled(True)
            self.refresh_button.setEnabled(True)
            return

        self.formatted_text = formatted

        if formatted != original:
            self.clipboard.setText(formatted)
            self.undo_button.setEnabled(True)

        save(original, formatted)

        self.editor.setPlainText(formatted)
        self.load_history()

        self.status.setText("Clipboard updated" if formatted != original
                            else "No changes needed")

        self.format_button.setEnabled(True)
        self.refresh_button.setEnabled(True)
        self.worker = None

    def format_failed(self, error):
        self.status.setText("Formatting failed")
        self.format_button.setEnabled(True)
        self.refresh_button.setEnabled(True)
        self.worker = None

        QMessageBox.critical(self, "ClipCraft Error", error)

    def undo(self):
        if self.original_text is None:
            return

        self.clipboard.setText(self.original_text)
        self.editor.setPlainText(self.original_text)

        self.original_text = None
        self.formatted_text = None

        self.undo_button.setEnabled(False)
        self.status.setText("Formatting undone")

    def load_history(self):
        self.history_list.clear()

        for original, formatted in get_recent(100):
            preview = original.replace("\n", " ").strip()

            if len(preview) > 65:
                preview = preview[:65] + "..."

            item = QListWidgetItem(preview or "(Empty)")
            item.setData(Qt.UserRole, (original, formatted))
            self.history_list.addItem(item)

    def restore_selected(self):
        item = self.history_list.currentItem()

        if item is not None:
            self.restore_history(item)

    def restore_history(self, item):
        original, formatted = item.data(Qt.UserRole)

        self.clipboard.setText(formatted)
        self.editor.setPlainText(formatted)

        self.original_text = original if original != formatted else None
        self.formatted_text = formatted

        self.undo_button.setEnabled(self.original_text is not None)
        self.status.setText("History item restored")

    def clear_history(self):
        answer = QMessageBox.question(
            self,
            "Clear History",
            "Delete all clipboard history?",
            QMessageBox.Yes | QMessageBox.No
        )

        if answer == QMessageBox.Yes:
            clear()
            self.load_history()
            self.status.setText("History cleared")


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("ClipCraft")

    window = ClipCraftWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
