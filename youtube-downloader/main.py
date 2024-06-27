import sys
import os
from PyQt6 import QtWidgets as wg, QtGui, QtCore
from PyQt6.QtCore import QUrl, QThread, pyqtSignal, QEventLoop
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from pytube import YouTube
from function import *
from settings import Settings


class DownloadThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, yt, video_quality, audio_quality, output_path, keep_temp_files):
        super().__init__()
        self.yt = yt
        self.video_quality = video_quality
        self.audio_quality = audio_quality
        self.output_path = output_path
        self.keep_temp_files = keep_temp_files

    def run(self):
        try:
            downloadVideo(self.yt, self.video_quality, self.audio_quality, self.output_path, self.progress.emit, self.keep_temp_files)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))
            
class MainWindow(wg.QWidget):
    def __init__(self):
        super().__init__()
        self.DLWindow = None
        self.settings = Settings()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("YouTube Video Downloader")
        self.setFixedSize(500, 110)

        self.searchButton = wg.QPushButton("Search")
        self.searchButton.setFixedHeight(30)
        self.quitButton = wg.QPushButton("Quit")
        self.quitButton.setFixedWidth(70)

        self.line = wg.QLineEdit()
        self.line.setPlaceholderText("YouTube URL")
        self.line.setFixedSize(350, 30)

        self.text = wg.QLabel()
        paletteText = self.text.palette()
        paletteText.setColor(self.text.foregroundRole(), QtGui.QColor(200, 0, 0))
        self.text.setPalette(paletteText)
        self.settingsButton = wg.QPushButton("Settings")
        self.settingsButton.clicked.connect(self.openSettings)
        self.settingsButton.setFixedWidth(70)

        self.searchButton.clicked.connect(self.searchButtonClicked)
        self.quitButton.clicked.connect(self.close)

        self.outerLayout = wg.QVBoxLayout()
        self.searchLayout = wg.QHBoxLayout()
        self.quitLayout = wg.QHBoxLayout()

        self.searchLayout.addWidget(self.line)
        self.searchLayout.addWidget(self.searchButton)
        
        self.quitLayout.addWidget(self.quitButton)
        self.quitLayout.addWidget(self.settingsButton)
        self.quitLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.outerLayout.addLayout(self.searchLayout)
        self.outerLayout.addWidget(self.text)
        self.outerLayout.addLayout(self.quitLayout)

        self.setLayout(self.outerLayout)
        self.show()
                
    def openSettings(self):
            dialog = SettingsDialog(self.settings, self)
            dialog.exec()
            
    def searchButtonClicked(self):
        url = self.line.text()
        if isLinkValid(url):
            self.text.setText("")
            try:
                yt = YouTube(url)
                if yt.age_restricted:
                    self.text.setText("The video is age restricted, we can't download it!")
                    return
                self.DLWindow = DownloadWindow(yt, self.settings, self)
                self.DLWindow.exec()
            except Exception as e:
                self.text.setText(f"Error: {str(e)}")
        else:
            self.text.setText("The link you entered is invalid!")

class DownloadWindow(wg.QDialog):
    def __init__(self, yt: YouTube, settings: Settings, parent=None):
        super().__init__()
        self.yt = yt
        self.settings = settings
        self.thumbnail_path = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Download {self.yt.title}")
        
        outerLayout = wg.QVBoxLayout()
        videoLayout = wg.QHBoxLayout()
        videoInfoLayout = wg.QVBoxLayout()
        qualityLayout = wg.QHBoxLayout()
        
        self.thumbnail = wg.QLabel()
        title = wg.QLabel(self.yt.title)
        description = wg.QLabel((self.yt.description[:80] + "..") if self.yt.description else '')
        author = wg.QLabel(self.yt.author)
        duration = wg.QLabel(f"Duration: {seconds_to_time_string(self.yt.length)}")
        views = wg.QLabel(f"{format_view_count(self.yt.views)} views")
        
        self.downloadButton = wg.QPushButton("Download")
        self.downloadButton.setFixedSize(100, 40)
        
        self.videoQuality = wg.QComboBox()
        self.audioQuality = wg.QComboBox()
        self.videoQuality.addItems(getVideoQuality(self.yt))
        self.audioQuality.addItems(getAudioQuality(self.yt))
        self.videoQuality.setFixedWidth(150)
        self.audioQuality.setFixedWidth(150)
        
        self.videoQuality.currentIndexChanged.connect(self.qualityChanged)
        self.audioQuality.currentIndexChanged.connect(self.qualityChanged)
        self.downloadButton.pressed.connect(self.downloadButtonPressed)
        
        self.fileSize = wg.QLabel()
        self.updateFileSize()

        self.path = f"thumbnails/{self.yt.title}.png"
        
        if not os.path.isfile(self.path):
            self.manager = QNetworkAccessManager()
            self.manager.finished.connect(self.replyFinished)
            self.downloadThumbnail()
        
        self.thumbnail.setPixmap(QtGui.QPixmap(self.path).scaledToHeight(150))
        title.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Weight.Bold))
        title.setFixedWidth(500)
        title.setWordWrap(True)
        
        default_video_quality = self.settings.get('default_video_quality')
        default_audio_quality = self.settings.get('default_audio_quality')
        
        video_quality_index = self.videoQuality.findText(default_video_quality)
        audio_quality_index = self.audioQuality.findText(default_audio_quality)
        
        if video_quality_index != -1:
            self.videoQuality.setCurrentIndex(video_quality_index)
        if audio_quality_index != -1:
            self.audioQuality.setCurrentIndex(audio_quality_index)

        
        videoInfoLayout.addWidget(title)
        videoInfoLayout.addWidget(author)
        videoInfoLayout.addWidget(description)
        videoInfoLayout.addWidget(duration)
        videoInfoLayout.addWidget(views)
        videoInfoLayout.addWidget(self.fileSize)
        videoInfoLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        
        qualityLayout.addWidget(self.videoQuality)
        qualityLayout.addWidget(self.audioQuality)
        qualityLayout.addWidget(self.downloadButton, 100, QtCore.Qt.AlignmentFlag.AlignRight)
        qualityLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        videoLayout.addWidget(self.thumbnail)
        videoLayout.addLayout(videoInfoLayout)
        
        outerLayout.addLayout(videoLayout)
        outerLayout.addLayout(qualityLayout)
        
        self.setLayout(outerLayout)
        self.updateFileSize()
        self.adjustSize()


    def downloadThumbnail(self):
        self.thumbnail_path = f"thumbnails/{sanitize_filename(self.yt.title)}.jpg"
        os.makedirs("thumbnails", exist_ok=True)
        
        if not os.path.isfile(self.thumbnail_path):
            self.manager = QNetworkAccessManager()
            self.manager.finished.connect(self.replyFinished)
            self.manager.get(QNetworkRequest(QUrl(self.yt.thumbnail_url)))
        else:
            self.thumbnail.setPixmap(QtGui.QPixmap(self.thumbnail_path).scaledToHeight(150))

    def replyFinished(self, reply):
        data = reply.readAll()
        with open(self.thumbnail_path, "wb") as file:
            file.write(data)
        self.thumbnail.setPixmap(QtGui.QPixmap(self.thumbnail_path).scaledToHeight(150))
        self.loop.quit()

    def qualityChanged(self):
        self.updateFileSize()

    def updateFileSize(self):
        videoSize = self.yt.streams.filter(res=self.videoQuality.currentText()).first().filesize
        audioSize = self.yt.streams.filter(abr=self.audioQuality.currentText()).first().filesize
        self.fileSize.setText(f"File size: {convert_bytes(audioSize + videoSize)}")

    def downloadButtonPressed(self):
        output_path = wg.QFileDialog.getExistingDirectory(self, "Select Output Directory", self.settings.get('default_output_path'))
        if output_path:
            self.settings.set('default_output_path', output_path)
            keep_temp_files = self.settings.get('keep_temp_files')
            self.downloadThread = DownloadThread(self.yt, self.videoQuality.currentText(), self.audioQuality.currentText(), output_path, keep_temp_files)
            self.downloadThread.progress.connect(self.updateProgress)
            self.downloadThread.finished.connect(self.downloadFinished)
            self.downloadThread.error.connect(self.downloadError)

            self.progressDialog = wg.QProgressDialog("Downloading...", "Cancel", 0, 100, self)
            self.progressDialog.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
            self.progressDialog.setAutoReset(False)
            self.progressDialog.setAutoClose(False)
            self.progressDialog.canceled.connect(self.cancelDownload)
            self.progressDialog.show()

            # Start the download thread
            self.downloadThread.start()

            # Create an event loop to wait for the download to finish
            loop = QEventLoop()
            self.downloadThread.finished.connect(loop.quit)
            self.downloadThread.error.connect(loop.quit)
            loop.exec()

    def updateProgress(self, value):
        self.progressDialog.setValue(value)

    def downloadFinished(self):
        self.progressDialog.close()
        wg.QMessageBox.information(self, "Download Complete", "The video has been downloaded successfully!")
        if not self.settings.get('keep_temp_files') and self.thumbnail_path:
            try:
                os.remove(self.thumbnail_path)
                print(f"Thumbnail deleted: {self.thumbnail_path}")
            except Exception as e:
                print(f"Failed to delete thumbnail: {self.thumbnail_path}. Error: {str(e)}")
        self.close()
            
    def downloadError(self, error_message):
        self.progressDialog.close()
        wg.QMessageBox.critical(self, "Download Error", f"An error occurred during download: {error_message}")
        self.close()

    def cancelDownload(self):
        self.downloadThread.terminate()
        self.downloadThread.wait()
        self.close()
        
class SettingsDialog(wg.QDialog):
    def __init__(self, settings: Settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Settings")
        self.setMinimumWidth(400)
        layout = wg.QVBoxLayout()

        # Default output path
        path_layout = wg.QHBoxLayout()
        path_layout.addWidget(wg.QLabel("Default output path:"))
        self.path_edit = wg.QLineEdit(self.settings.get('default_output_path'))
        path_layout.addWidget(self.path_edit)
        browse_button = wg.QPushButton("Browse")
        browse_button.clicked.connect(self.browsePath)
        path_layout.addWidget(browse_button)
        layout.addLayout(path_layout)

        # Default video quality
        layout.addWidget(wg.QLabel("Default video quality:"))
        self.video_quality = wg.QComboBox()
        self.video_quality.addItems(['144p', '240p', '360p', '480p', '720p', '1080p'])
        self.video_quality.setCurrentText(self.settings.get('default_video_quality'))
        layout.addWidget(self.video_quality)

        # Default audio quality
        layout.addWidget(wg.QLabel("Default audio quality:"))
        self.audio_quality = wg.QComboBox()
        self.audio_quality.addItems(['48kbps', '128kbps', '160kbps', '192kbps'])
        self.audio_quality.setCurrentText(self.settings.get('default_audio_quality'))
        layout.addWidget(self.audio_quality)

        # Keep temporary files
        self.keep_temp = wg.QCheckBox("Keep temporary files")
        self.keep_temp.setChecked(self.settings.get('keep_temp_files'))
        layout.addWidget(self.keep_temp)

        # Auto rename existing files
        self.auto_rename = wg.QCheckBox("Auto rename existing files")
        self.auto_rename.setChecked(self.settings.get('auto_rename_existing'))
        layout.addWidget(self.auto_rename)

        # Buttons
        button_layout = wg.QHBoxLayout()
        save_button = wg.QPushButton("Save")
        save_button.clicked.connect(self.saveSettings)
        button_layout.addWidget(save_button)
        cancel_button = wg.QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def browsePath(self):
        path = wg.QFileDialog.getExistingDirectory(self, "Select Default Output Directory", self.path_edit.text())
        if path:
            self.path_edit.setText(path)

    def saveSettings(self):
        self.settings.set('default_output_path', self.path_edit.text())
        self.settings.set('default_video_quality', self.video_quality.currentText())
        self.settings.set('default_audio_quality', self.audio_quality.currentText())
        self.settings.set('keep_temp_files', self.keep_temp.isChecked())
        self.settings.set('auto_rename_existing', self.auto_rename.isChecked())
        self.accept()


if __name__ == "__main__":
    app = wg.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())