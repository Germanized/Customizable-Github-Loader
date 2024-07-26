import sys
import os
import requests
import zipfile
from io import BytesIO
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
                             QStackedWidget, QTextEdit, QScrollArea, QFrame, QHBoxLayout, QSizePolicy, QMessageBox, QGraphicsOpacityEffect)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QPainter, QColor, QBrush, QIcon, QFontDatabase, QFont
import pygame
import webbrowser


class RoundedWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        color = QColor(28, 28, 28)
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 15, 15)


class SplashScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        screen_geometry = QApplication.desktop().screenGeometry()
        screen_center = screen_geometry.center()
        self.setGeometry(screen_center.x() - 400, screen_center.y() - 300, 800, 600)

        self.central_widget = RoundedWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)
        self.central_widget.setLayout(layout)

        self.expand_animation = QPropertyAnimation(self, b"geometry")
        self.expand_animation.setDuration(2000)
        self.expand_animation.setStartValue(QRect(screen_center.x(), screen_center.y(), 10, 10))
        self.expand_animation.setEndValue(QRect(screen_center.x() - 400, screen_center.y() - 300, 800, 600))
        self.expand_animation.setEasingCurve(QEasingCurve.OutQuad)
        self.expand_animation.finished.connect(self.show_text)
        self.expand_animation.start()

    def show_text(self):
        self.welcome_label = QLabel("Welcome to Germanized's Loader", self)
        self.welcome_label.setAlignment(Qt.AlignCenter)

        # Load custom font
        font_id = QFontDatabase.addApplicationFont("Mont.otf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.welcome_label.setFont(QFont(font_family))
        self.welcome_label.setStyleSheet("color: white; font-size: 24px;")
        self.central_widget.layout().addWidget(self.welcome_label)

        # Opacity effect
        self.opacity_effect = QGraphicsOpacityEffect(self.welcome_label)
        self.welcome_label.setGraphicsEffect(self.opacity_effect)

        self.opacity_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(3000)
        self.opacity_animation.setStartValue(0)
        self.opacity_animation.setEndValue(1)
        self.opacity_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.opacity_animation.finished.connect(self.fade_out_text)
        self.opacity_animation.start()

    def fade_out_text(self):
        self.opacity_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(3000)
        self.opacity_animation.setStartValue(1)
        self.opacity_animation.setEndValue(0)
        self.opacity_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.opacity_animation.finished.connect(self.cleanup_and_shrink)
        self.opacity_animation.start()

    def cleanup_and_shrink(self):
        self.welcome_label.deleteLater()
        screen_geometry = QApplication.desktop().screenGeometry()
        screen_center = screen_geometry.center()
        self.expand_animation.setStartValue(QRect(screen_center.x() - 400, screen_center.y() - 300, 800, 600))
        self.expand_animation.setEndValue(QRect(screen_center.x(), screen_center.y(), 10, 10))
        self.expand_animation.setEasingCurve(QEasingCurve.InQuad)
        self.expand_animation.finished.connect(self.open_main_window)
        self.expand_animation.start()

    def open_main_window(self):
        if not hasattr(self, 'main_window') or not self.main_window.isVisible():
            self.main_window = LoaderApp()
            self.main_window.show()
        self.close()


class DraggableWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.moving = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moving = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.moving:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moving = False


class LoaderApp(DraggableWidget):
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        super().__init__()
        self.initUI()
        self.play_music()
        self.expand_window()  # Start the expand animation

    def initUI(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        screen_center = screen_geometry.center()
        self.setGeometry(screen_center.x() - 500, screen_center.y() - 350, 1000, 700)
        self.setStyleSheet("background-color: #1c1c1c; border-radius: 15px;")

        central_widget = RoundedWidget()
        central_layout = QVBoxLayout(central_widget)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        # Load custom font
        font_id = QFontDatabase.addApplicationFont("Mont.otf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.setFont(QFont(font_family))

        self.title = QLabel("Germanized Loader", self)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont(font_family))
        self.title.setStyleSheet("color: white; font-size: 24px;")
        central_layout.addWidget(self.title)

        content_layout = QHBoxLayout()
        central_layout.addLayout(content_layout)

        nav_frame = QFrame(self)
        nav_layout = QVBoxLayout(nav_frame)
        nav_frame.setStyleSheet("background-color: #282828; border-radius: 15px;")
        nav_frame.setFixedWidth(150)
        content_layout.addWidget(nav_frame)

        self.repos_button = QPushButton("Repositories")
        self.repos_button.setStyleSheet(self.button_style())
        self.repos_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.repositories_widget))
        nav_layout.addWidget(self.repos_button)

        self.readme_button = QPushButton("Readme")
        self.readme_button.setStyleSheet(self.button_style())
        self.readme_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.readme_widget))
        nav_layout.addWidget(self.readme_button)

        self.more_button = QPushButton("More")
        self.more_button.setStyleSheet(self.button_style())
        self.more_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.more_widget))
        nav_layout.addWidget(self.more_button)

        nav_layout.addStretch(1)

        self.mute_button = QPushButton()
        self.mute_button.setIcon(QIcon("mute_icon.png"))
        self.mute_button.setStyleSheet("border: none; background-color: #333; border-radius: 15px; padding: 5px;")
        self.mute_button.setFixedSize(40, 40)
        self.mute_button.clicked.connect(self.toggle_mute)
        self.muted = False
        nav_layout.addWidget(self.mute_button)

        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(self.stacked_widget)

        self.repositories_widget = QScrollArea()
        self.repositories_widget.setWidgetResizable(True)
        self.repositories_container = QWidget()
        self.repositories_layout = QVBoxLayout(self.repositories_container)
        self.repositories_widget.setWidget(self.repositories_container)
        self.stacked_widget.addWidget(self.repositories_widget)
        self.fetch_repositories()

        self.readme_widget = QScrollArea()
        self.readme_text = QTextEdit()
        self.readme_text.setReadOnly(True)
        self.readme_widget.setWidget(self.readme_text)
        self.readme_widget.setWidgetResizable(True)
        self.stacked_widget.addWidget(self.readme_widget)
        self.fetch_readme()

        self.more_widget = QWidget()
        more_layout = QVBoxLayout(self.more_widget)
        self.more_label = QLabel("More content can be added here")
        self.more_label.setAlignment(Qt.AlignCenter)
        more_layout.addWidget(self.more_label)
        self.stacked_widget.addWidget(self.more_widget)

    def button_style(self):
        return """
        QPushButton {
            background-color: #333;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 10px;
            font-family: 'Mont';
        }
        QPushButton:hover {
            background-color: #555;
        }
        QPushButton:pressed {
            background-color: #111;
        }
        """

    def fetch_repositories(self):
        url = "https://github.com/Germanized?tab=repositories"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors
            soup = BeautifulSoup(response.text, 'html.parser')
            repo_items = soup.find_all('div', class_='d-inline-block mb-1')

            for item in repo_items:
                repo_name = item.find('a').text.strip()
                repo_description = item.find('p', class_='col-9 text-gray my-1 pr-4').text.strip() if item.find('p', class_='col-9 text-gray my-1 pr-4') else 'No description'
                repo_button = QPushButton(f"{repo_name}: {repo_description}")
                repo_button.setStyleSheet(self.button_style())
                repo_button.clicked.connect(lambda checked, name=repo_name: self.download_repo(name))
                self.repositories_layout.addWidget(repo_button)

        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch repositories: {e}")

    def download_repo(self, repo_name):
        try:
            url = f"https://github.com/Germanized/{repo_name}/archive/refs/heads/main.zip"
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors

            with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
                extract_path = os.path.join(os.getcwd(), repo_name)
                os.makedirs(extract_path, exist_ok=True)
                zip_file.extractall(extract_path)

            QMessageBox.information(self, "Success", f"Repository '{repo_name}' downloaded successfully.")

        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to download repository '{repo_name}': {e}")

    def fetch_readme(self):
        readme_url = "https://github.com/Germanized/Germanized/blob/main/README.md"
        try:
            response = requests.get(readme_url)
            response.raise_for_status()  # Check for HTTP errors

            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.find('article', {'class': 'markdown-body entry-content container-lg'}).get_text()
            self.readme_text.setPlainText(content)

        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch README: {e}")

    def play_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load("background_music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # Loop the music

    def toggle_mute(self):
        if self.muted:
            pygame.mixer.music.unpause()
            self.mute_button.setIcon(QIcon("mute_icon.png"))
            self.muted = False
        else:
            pygame.mixer.music.pause()
            self.mute_button.setIcon(QIcon("unmute_icon.png"))
            self.muted = True

    def expand_window(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        screen_center = screen_geometry.center()
        self.expand_animation = QPropertyAnimation(self, b"geometry")
        self.expand_animation.setDuration(2000)
        self.expand_animation.setStartValue(QRect(screen_center.x(), screen_center.y(), 10, 10))
        self.expand_animation.setEndValue(QRect(screen_center.x() - 500, screen_center.y() - 350, 1000, 700))
        self.expand_animation.setEasingCurve(QEasingCurve.OutQuad)
        self.expand_animation.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec_())
