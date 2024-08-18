import os
import time
import requests
from PyQt5.QtCore import QThread, pyqtSignal


class DownloadWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    remaining_time = pyqtSignal(int)
    error = pyqtSignal(str)
    paused = pyqtSignal()
    resumed = pyqtSignal()

    def __init__(self, url, download_path):
        super().__init__()
        self.url = url
        self.download_path = download_path
        self._pause = False
        self._stop = False

    def run(self):
        try:
            file_name = self.url.split('/')[-1].split('?')[0]
            file_path = os.path.join(self.download_path, file_name)

            if os.path.exists(file_path):
                existing_file_size = os.path.getsize(file_path)
            else:
                existing_file_size = 0

            headers = {'Range': f'bytes={existing_file_size}-'}
            response = requests.get(self.url, headers=headers, stream=True)

            if response.status_code in (200, 206):
                content_type = response.headers.get('Content-Type', '').split(';')[0]
                file_extension = self.get_file_extension(content_type)

                if not '.' in file_name:
                    file_name = f"{file_name}.{file_extension}"

                category_folder = self.categorize_file(file_extension)
                final_path = os.path.join(self.download_path, category_folder)
                os.makedirs(final_path, exist_ok=True)
                file_path = os.path.join(final_path, file_name)

                total_length = int(response.headers.get('Content-Length', 0)) + existing_file_size

                with open(file_path, 'ab') as file:
                    downloaded = existing_file_size
                    start_time = time.time()
                    for chunk in response.iter_content(chunk_size=1024):
                        if self._stop:
                            return
                        if self._pause:
                            self.paused.emit()
                            while self._pause:
                                QThread.sleep(1)
                            self.resumed.emit()
                        if chunk:
                            file.write(chunk)
                            downloaded += len(chunk)
                            percent = (downloaded / total_length) * 100
                            self.progress.emit(int(percent))

                            elapsed_time = time.time() - start_time
                            if elapsed_time > 0:
                                speed = downloaded / elapsed_time
                                remaining_data = total_length - downloaded
                                if speed > 0:
                                    remaining_time_estimate = int(remaining_data / speed)
                                    self.remaining_time.emit(remaining_time_estimate)
                if not self._stop:
                    self.finished.emit(f"{file_name} Downloaded")
            else:
                self.error.emit(f"Error downloading the file. Status: {response.status_code}")
        except Exception as e:
            self.error.emit(f"Exception: {str(e)}")

    def get_file_extension(self, content_type):
        content_type_map = {
            'application/zip': 'zip',
            'application/pdf': 'pdf',
            'image/jpeg': 'jpg',
            'image/png': 'png',
            'text/html': 'html',
            'video/mp4': 'mp4',
            'audio/mpeg': 'mp3',
        }
        return content_type_map.get(content_type, 'bin')

    def categorize_file(self, file_extension):
        video_ext = {'mp4', 'mkv', 'avi'}
        audio_ext = {'mp3', 'wav', 'aac'}
        document_ext = {'pdf', 'doc', 'docx', 'txt'}
        image_ext = {'jpg', 'jpeg', 'png', 'gif'}

        if file_extension in video_ext:
            return "Videos"
        elif file_extension in audio_ext:
            return "Music"
        elif file_extension in document_ext:
            return "Documents"
        elif file_extension in image_ext:
            return "Pictures"
        else:
            return "Others"

    def pause(self):
        self._pause = True

    def resume(self):
        self._pause = False

    def stop(self):
        self._stop = True
