import os
import sys
from PyQt5 import QtGui, QtCore
from Download_Manager_Worker import DownloadWorker
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QTextEdit,
                             QListWidget, QFileDialog, QProgressBar)
from Download_Manager_ui import Ui_Dialog

class DownloadManager(QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.url_list = []
        self.workers = []
        self.default_download_path = os.path.join(os.path.expanduser('~'), 'Downloads')

        self.initUI()

    def initUI(self):
        self.add_button.clicked.connect(self.add_url)
        self.download_button.clicked.connect(self.start_download)
        self.change_path_button.clicked.connect(self.change_download_path)
        self.pause_button.clicked.connect(self.pause_download)
        self.resume_button.clicked.connect(self.resume_download)
        self.cancel_button.clicked.connect(self.cancel_download)

        self.pause_button.setEnabled(False)
        self.pause_button.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.resume_button.setEnabled(False)
        self.resume_button.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.cancel_button.setEnabled(False)
        self.cancel_button.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))

        self.remove_1.clicked.connect(self.remove_selected_url)
        self.remove_all.clicked.connect(self.remove_all_urls)

    def add_url(self):
        url = self.url_input.text()
        if url:
            self.url_list.append(url)
            self.url_list_widget.addItem(url)
            self.url_input.clear()

    def remove_selected_url(self):
        selected_items = self.url_list_widget.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            self.url_list.remove(item.text())
            self.url_list_widget.takeItem(self.url_list_widget.row(item))

    def remove_all_urls(self):
        self.url_list_widget.clear()
        self.url_list.clear()

    def start_download(self):
        self.progress_output.clear()
        self.url_list_widget.setEnabled(False)
        self.url_list_widget.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.download_button.setEnabled(False)
        self.download_button.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.pause_button.setEnabled(True)
        self.pause_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.resume_button.setEnabled(False)
        self.resume_button.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.cancel_button.setEnabled(True)
        self.cancel_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.change_path_button.setEnabled(False)
        self.change_path_button.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.remove_1.setEnabled(False)
        self.remove_1.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.remove_all.setEnabled(False)
        self.remove_all.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))

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
            worker.cancelled.connect(self.on_cancelled)
            worker.remaining_time.connect(self.update_remaining_time)
            worker.file_size.connect(self.display_file_size)
            self.workers.append(worker)
            worker.start()

    def change_download_path(self):
        new_path = QFileDialog.getExistingDirectory(self, "Select Download Directory", self.default_download_path)
        if new_path:
            self.default_download_path = new_path

    def pause_download(self):
        self.pause_button.setEnabled(False)
        self.pause_button.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.resume_button.setEnabled(True)
        self.resume_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        for worker in self.workers:
            worker.pause()

    def resume_download(self):
        self.pause_button.setEnabled(True)
        self.pause_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.resume_button.setEnabled(False)
        self.resume_button.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        for worker in self.workers:
            worker.resume()

    def cancel_download(self):
        self.pause_button.setEnabled(False)
        self.pause_button.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.resume_button.setEnabled(False)
        self.resume_button.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.change_path_button.setEnabled(True)
        self.change_path_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.remove_1.setEnabled(True)
        self.remove_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.remove_all.setEnabled(True)
        self.remove_all.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        for worker in self.workers:

            worker.stop()

        self.url_list_widget.setEnabled(True)
        self.url_list_widget.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.download_button.setEnabled(True)
        self.download_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pause_button.setEnabled(False)
        self.pause_button.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.resume_button.setEnabled(False)
        self.resume_button.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.cancel_button.setEnabled(False)
        self.cancel_button.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))

    def update_progress(self, percent):
        self.progress_bar.setValue(percent)

    def on_paused(self):
        self.progress_output.append("Download paused.")

    def on_resumed(self):
        self.progress_output.append("Download resumed.")

    def on_cancelled(self):
        self.progress_output.append("Download cancelled.")

    def on_finished(self, message):
        self.progress_output.append(message)
        self.change_path_button.setEnabled(True)
        self.change_path_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.check_all_finished()
        self.remove_all_urls()
        self.url_list_widget.setEnabled(True)
        self.url_list_widget.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.download_button.setEnabled(True)
        self.download_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.file_size_display.setText("")
        self.remove_1.setEnabled(True)
        self.remove_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.remove_all.setEnabled(True)
        self.remove_all.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def on_error(self, error_message):
        self.progress_output.append(f"Error: {error_message}")
        self.check_all_finished()

    def check_all_finished(self):
        if all(not worker.isRunning() for worker in self.workers):
            self.url_list_widget.setEnabled(True)
            self.url_list_widget.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
            self.download_button.setEnabled(True)
            self.download_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.pause_button.setEnabled(False)
            self.pause_button.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
            self.resume_button.setEnabled(False)
            self.resume_button.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
            self.cancel_button.setEnabled(False)
            self.cancel_button.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))

    def closeEvent(self, event):
        for worker in self.workers:
            worker.quit()
            worker.wait()
        event.accept()

    def update_remaining_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        time_str= f'{minutes:02}:{seconds:02}'

        self.remaining_time.setText(time_str)

    def display_file_size(self, size):
        size_in_mb = size / (1024 * 1024)
        self.file_size_display.setText(f"{size_in_mb:.2f} MB")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DownloadManager()
    window.show()
    sys.exit(app.exec_())
