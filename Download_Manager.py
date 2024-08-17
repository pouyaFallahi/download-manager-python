import os
import sys
from Download_Manager_Worker import DownloadWorker
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QTextEdit,
                             QListWidget, QFileDialog, QProgressBar)


class DownloadManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Download Manager")
        self.setGeometry(100, 100, 600, 400)

        self.url_list = []
        self.workers = []
        self.default_download_path = os.path.join(os.path.expanduser('~'), 'Downloads')

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter download URL")
        self.layout.addWidget(self.url_input)

        self.add_button = QPushButton("Add URL", self)
        self.add_button.clicked.connect(self.add_url)
        self.layout.addWidget(self.add_button)

        self.url_list_widget = QListWidget(self)
        self.layout.addWidget(self.url_list_widget)

        self.download_button = QPushButton("Start Download", self)
        self.download_button.clicked.connect(self.start_download)
        self.layout.addWidget(self.download_button)

        self.change_path_button = QPushButton("Change Download Path", self)
        self.change_path_button.clicked.connect(self.change_download_path)
        self.layout.addWidget(self.change_path_button)

        self.pause_button = QPushButton("Pause", self)
        self.pause_button.clicked.connect(self.pause_download)
        self.layout.addWidget(self.pause_button)

        self.resume_button = QPushButton("Resume", self)
        self.resume_button.clicked.connect(self.resume_download)
        self.layout.addWidget(self.resume_button)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.cancel_download)
        self.layout.addWidget(self.cancel_button)

        self.progress_output = QTextEdit(self)
        self.progress_output.setReadOnly(True)
        self.layout.addWidget(self.progress_output)

        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)

        # Initialize buttons state
        self.pause_button.setEnabled(False)
        self.resume_button.setEnabled(False)
        self.cancel_button.setEnabled(False)

    def add_url(self):
        url = self.url_input.text()
        if url:
            self.url_list.append(url)
            self.url_list_widget.addItem(url)
            self.url_input.clear()

    def start_download(self):
        self.progress_output.clear()
        self.url_list_widget.setEnabled(False)
        self.download_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.resume_button.setEnabled(True)
        self.cancel_button.setEnabled(True)

        self.workers = []  # Reset the list of workers
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(100)

        for url in self.url_list:
            worker = DownloadWorker(url, self.default_download_path)
            worker.progress.connect(self.update_progress)
            worker.finished.connect(self.on_finished)
            worker.error.connect(self.on_error)
            worker.paused.connect(self.on_paused)
            worker.resumed.connect(self.on_resumed)
            self.workers.append(worker)
            worker.start()

    def change_download_path(self):
        new_path = QFileDialog.getExistingDirectory(self, "Select Download Directory", self.default_download_path)
        if new_path:
            self.default_download_path = new_path

    def pause_download(self):
        for worker in self.workers:
            worker.pause()

    def resume_download(self):
        for worker in self.workers:
            worker.resume()

    def cancel_download(self):
        for worker in self.workers:
            worker.stop()

        self.url_list_widget.setEnabled(True)
        self.download_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.resume_button.setEnabled(False)
        self.cancel_button.setEnabled(False)

    def update_progress(self, percent):
        self.progress_bar.setValue(percent)

    def on_paused(self):
        self.progress_output.append("Download paused.")

    def on_resumed(self):
        self.progress_output.append("Download resumed.")

    def on_finished(self, message):
        self.progress_output.append(message)
        self.check_all_finished()

    def on_error(self, error_message):
        self.progress_output.append(f"Error: {error_message}")
        self.check_all_finished()

    def check_all_finished(self):
        if all(not worker.isRunning() for worker in self.workers):
            self.url_list_widget.setEnabled(True)
            self.download_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.resume_button.setEnabled(False)
            self.cancel_button.setEnabled(False)

    def closeEvent(self, event):
        for worker in self.workers:
            worker.quit()
            worker.wait()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DownloadManager()
    window.show()
    sys.exit(app.exec_())
