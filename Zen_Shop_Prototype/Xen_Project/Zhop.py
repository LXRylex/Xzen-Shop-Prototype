# SEARCH FOR " TOKEN " TO FIND THE uhhh DISCORD BOT thingy put ur own there

import sys
import subprocess
import os
import time
import traceback
import logging
import math
import asyncio
import concurrent.futures
import requests
from urllib.parse import urlparse

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QScrollArea, QMessageBox, QGridLayout,
    QToolButton, QMenu
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer, QSettings

# -----------------------------------------------------------
# 1. Check and install required packages if necessary. otherwise it will throw a brick at you. an error brick.
# -----------------------------------------------------------
def check_and_install_requirements():
    required = ["PyQt5", "requests", "discord.py"]
    missing = []
    for pkg in required:
        try:
            __import__(pkg.replace(".py", ""))
        except ImportError:
            missing.append(pkg)
    if missing:
        for pkg in missing:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

check_and_install_requirements()

import discord  # Import discord after installation

# -----------------------------------------------------------
# 2. Set up logging. for errors
# -----------------------------------------------------------
logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s: %(message)s',
    filemode='w'
)

# -----------------------------------------------------------
# 3. Global exception hook. maybe for fishing? :d
# -----------------------------------------------------------
def handle_exception(exctype, value, tb):
    err = ''.join(traceback.format_exception(exctype, value, tb))
    logging.error(err)
    try:
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        QMessageBox.critical(None, "Error", "An unexpected error occurred:\n" + err)
    except Exception:
        print(err, file=sys.stderr)
    time.sleep(10)
    sys.exit(1)

sys.excepthook = handle_exception

# -----------------------------------------------------------
# 4. THEMEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEES (I'm sorry, I had to do it)
# -----------------------------------------------------------
DEFAULT_THEME = """
QMainWindow, QWidget, QScrollArea, QDialog {
    background-color: #ffffff; color: #000000;
}
QLabel { color: #000000; }
QPushButton {
    background-color: #f0f0f0; color: #000000;
    border: 1px solid #cccccc; padding: 4px; border-radius: 4px;
}
QPushButton:hover { background-color: #e0e0e0; }
QLineEdit {
    background-color: #ffffff; color: #000000;
    border: 1px solid #cccccc; padding: 4px; border-radius: 4px;
}
QToolBar { background-color: #f0f0f0; }
"""

GREY_THEME = """
QMainWindow, QWidget, QScrollArea, QDialog {
    background-color: #2e2e2e; color: #ffffff;
}
QLabel { color: #ffffff; }
QPushButton {
    background-color: #3a3a3a; color: #ffffff;
    border: 1px solid #555555; padding: 4px; border-radius: 4px;
}
QPushButton:hover { background-color: #4a4a4a; }
QLineEdit {
    background-color: #3a3a3a; color: #ffffff;
    border: 1px solid #555555; padding: 4px; border-radius: 4px;
}
QToolBar { background-color: #3a3a3a; }
"""

BLACK_THEME = """
QMainWindow, QWidget, QScrollArea, QDialog {
    background-color: #000000; color: #f0f0f0;
}
QLabel { color: #f0f0f0; }
QPushButton {
    background-color: #330033; color: #f0f0f0;
    border: 1px solid #660066; padding: 4px; border-radius: 4px;
}
QPushButton:hover { background-color: #4B0082; }
QLineEdit {
    background-color: #330033; color: #f0f0f0;
    border: 1px solid #660066; padding: 4px; border-radius: 4px;
}
QToolBar { background-color: #330033; }
"""

# -----------------------------------------------------------
# 5. Discord Bot Settings.
# -----------------------------------------------------------
DISCORD_BOT_TOKEN = ""  # Replace with your new token
DISCORD_CHANNEL_ID = 12121212121212  # Replace with your channel ID (as an integer)

# -----------------------------------------------------------
# 6. Determine config.ini path dynamically.
#     Expected path: <user_home_directory>\Desktop\Zen-Mod\Xen_Project\config.ini
# -----------------------------------------------------------
config_path = os.path.join(os.path.expanduser("~"), "Desktop", "Zen-Mod", "Xen_Project", "config.ini")

# -----------------------------------------------------------
# 7. Asynchronous function to fetch Discord forum posts.
#    For each thread in the forum channel, fetch the starter message and check for attachments:
#    - If the attachment's filename indicates an image, use it as the post's image.
#    - Otherwise, set it as the post's download_url.
# -----------------------------------------------------------
async def fetch_and_close(token, channel_id, limit=100):
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    posts = []
    
    @client.event
    async def on_ready():
        channel = client.get_channel(channel_id)
        if channel is None:
            print("Channel not found!")
        else:
            # For forum channels, iterate over threads.
            if channel.type == discord.ChannelType.forum:
                threads = channel.threads
                if not threads:
                    threads = await channel.fetch_public_threads()
                for thread in threads:
                    try:
                        starter = await thread.fetch_message(thread.id)
                        image_url = ""
                        download_url = ""
                        # Process attachments:
                        if starter.attachments:
                            for att in starter.attachments:
                                fname = att.filename.lower()
                                if fname.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                                    image_url = att.url
                                else:
                                    download_url = att.url
                                    # If you have multiple files, you might want to collect them in a list.
                                    break
                        # If no attachment was found, check embeds.
                        if not image_url and starter.embeds:
                            for embed in starter.embeds:
                                if embed.image and embed.image.url:
                                    image_url = embed.image.url
                                    break
                        posts.append({
                            "title": thread.name,
                            "author": starter.author.name,
                            "image": image_url,
                            "download_url": download_url,
                            "content": starter.content
                        })
                    except Exception as e:
                        print(f"Error fetching starter for thread {thread.id}: {e}")
                    if len(posts) >= limit:
                        break
        await client.close()
    
    try:
        await client.start(token)
    except Exception as e:
        print(f"Exception while starting client: {e}")
    return posts

# -----------------------------------------------------------
# 8. Dummy post generation. "ye needed that just skip here :d"
# -----------------------------------------------------------
def generate_blog_posts(count):
    posts = []
    for i in range(1, count + 1):
        if i == 1:
            posts.append({
                "title": f"Sample Post {i}",
                "author": "Alice",
                "image": r"C:/USers/x_crusherpx0/Downloads/♡ Manwha Player.jpg",
                "download_url": "https://www.example.com/sample1.txt",
                "content": "This is the content of sample post 1."
            })
        else:
            posts.append({
                "title": f"Sample Post {i}",
                "author": f"Author {i}",
                "image": "",
                "download_url": "https://www.example.com/sample1.txt",
                "content": f"This is the content of sample post {i}."
            })
    return posts

def load_blog_posts():
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(lambda: asyncio.run(fetch_and_close(DISCORD_BOT_TOKEN, int(DISCORD_CHANNEL_ID), limit=100)))
            discord_posts = future.result(timeout=30)
        if discord_posts and len(discord_posts) > 0:
            print(f"Fetched {len(discord_posts)} posts from Discord.")
            return discord_posts
    except Exception as e:
        print(f"Error fetching Discord posts: {e}")
    settings = QSettings(config_path, QSettings.IniFormat)
    num_posts_str = settings.value("General/num_posts", "60")
    try:
        num_posts = int(num_posts_str)
    except ValueError:
        num_posts = 60
    print(f"Loaded num_posts from config.ini: {num_posts}")
    return generate_blog_posts(num_posts)

# -----------------------------------------------------------
# 9. Widget class for displaying blog posts...why is this here?
# -----------------------------------------------------------
class BlogPostWidget(QWidget):
    def __init__(self, post, parent=None):
        super().__init__(parent)
        self.post = post
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        # Title
        title_label = QLabel(f"<b>{self.post['title']}</b>")
        layout.addWidget(title_label)
        
        # If a shared file exists (download_url non-empty), display a modern download button immediately under the title.
        download_url = self.post.get('download_url', '')
        if download_url:
            file_name = os.path.basename(urlparse(download_url).path)
            if not file_name:
                file_name = "Download File"
            download_button = QPushButton(file_name)
            # Updated modern button style. somehow.
            download_button.setStyleSheet("""
                QPushButton {
                    background-color: #0078d7;
                    color: white;
                    font-size: 16px;
                    padding: 8px 16px;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #005a9e;
                }
            """)
            download_button.clicked.connect(self.download_content)
            # Place the button in a horizontal layout aligned to the left.
            h_layout = QHBoxLayout()
            h_layout.addWidget(download_button, alignment=Qt.AlignLeft)
            layout.addLayout(h_layout)
        
        # Author
        author_label = QLabel(f"by {self.post['author']}")
        layout.addWidget(author_label)
        
        # Image display.
        image_url = self.post.get('image', '')
        if image_url:
            image_label = QLabel()
            pixmap = QPixmap()
            if image_url.startswith("http"):
                try:
                    response = requests.get(image_url)
                    response.raise_for_status()
                    pixmap.loadFromData(response.content)
                except Exception as e:
                    print(f"Failed to load image from {image_url}: {e}")
            else:
                pixmap.load(image_url)
            if not pixmap.isNull():
                image_label.setPixmap(pixmap.scaledToWidth(200, Qt.SmoothTransformation))
            layout.addWidget(image_label)
        
        # Content
        content_label = QLabel(self.post.get('content', ''))
        content_label.setWordWrap(True)
        layout.addWidget(content_label)
        
        self.setLayout(layout)

    def download_content(self):
        download_url = self.post.get('download_url')
        if not download_url:
            QMessageBox.warning(self, "No URL", "No download URL provided for this post.")
            return
        try:
            response = requests.get(download_url)
            response.raise_for_status()
            downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
            if not os.path.exists(downloads_folder):
                os.makedirs(downloads_folder)
            parsed = urlparse(download_url)
            filename = os.path.basename(parsed.path)
            if not filename:
                safe_title = self.post['title'].replace(" ", "_")
                filename = safe_title + ".bin"
            filepath = os.path.join(downloads_folder, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            QMessageBox.information(self, "Downloaded", f"File downloaded to:\n{filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{e}")
# -----------------------------------------------------------
# 10. MainWindow CLASS...ASS... the fuck-
# -----------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zen Shop Prototype")
        self.setMinimumSize(1100, 630) # minimum size for window because it may freak out
        
        self.posts = load_blog_posts()
        self.filtered_posts = self.posts[:]
        self.current_page = 0
        self.fixed_row_count = 2
        
        self.settings = QSettings(config_path, QSettings.IniFormat)
        self.current_theme = self.settings.value("General/theme", "Black")
        
        self.initUI()
        self.set_theme(self.current_theme)
    def initUI(self):
        toolbar = self.addToolBar("Settings")
        toolbar.setMovable(False)
        # Settings (gear) button.
        settings_button = QToolButton()
        settings_button.setText("⚙")
        settings_button.setFixedSize(30, 30)
        settings_button.setStyleSheet("border: none; font-size: 16px;")
        settings_button.setPopupMode(QToolButton.InstantPopup)
        menu = QMenu()
        action_default = menu.addAction("Default")
        action_grey = menu.addAction("Grey")
        action_black = menu.addAction("Black")
        action_default.triggered.connect(lambda: self.set_theme("Default"))
        action_grey.triggered.connect(lambda: self.set_theme("Grey"))
        action_black.triggered.connect(lambda: self.set_theme("Black"))
        settings_button.setMenu(menu)
        toolbar.addWidget(settings_button)
        # "Update from Dis :O --> porn- discord" button.
        update_button = QPushButton("Update from Discord")
        update_button.clicked.connect(self.update_from_discord)
        toolbar.addWidget(update_button)
        
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search by title or author...")
        self.search_bar.textChanged.connect(self.update_filter)
        search_layout.addWidget(self.search_bar)
        main_layout.addLayout(search_layout)
        self.scroll_area = QScrollArea()
        self.posts_container = QWidget()
        self.posts_layout = QGridLayout()
        self.posts_container.setLayout(self.posts_layout)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.posts_container)
        main_layout.addWidget(self.scroll_area)
        pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.prev_page)
        pagination_layout.addWidget(self.prev_button)
        self.page_label = QLabel()
        pagination_layout.addWidget(self.page_label, alignment=Qt.AlignCenter)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)
        pagination_layout.addWidget(self.next_button)
        main_layout.addLayout(pagination_layout)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.refresh_posts()
        QTimer.singleShot(0, self.refresh_posts)
    def update_from_discord(self):
        def run_fetch():
            return asyncio.run(fetch_and_close(DISCORD_BOT_TOKEN, int(DISCORD_CHANNEL_ID), limit=100))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(run_fetch)
            try:
                discord_posts = future.result(timeout=30)
                if discord_posts and len(discord_posts) > 0:
                    self.posts = discord_posts
                    self.filtered_posts = self.posts[:]
                    self.current_page = 0
                    self.refresh_posts()
                    QMessageBox.information(self, "Update", f"Updated from Discord with {len(discord_posts)} posts.")
                else:
                    QMessageBox.information(self, "Update", "No posts fetched from Discord.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error fetching Discord posts: {e}")
    def set_theme(self, theme_name):
        self.current_theme = theme_name
        self.settings.setValue("General/theme", theme_name)
        app = QApplication.instance()
        if theme_name == "Default":
            app.setStyleSheet(DEFAULT_THEME)
        elif theme_name == "Grey":
            app.setStyleSheet(GREY_THEME)
        elif theme_name == "Black":
            app.setStyleSheet(BLACK_THEME)
        self.refresh_posts()
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
    def update_filter(self):
        query = self.search_bar.text().lower()
        if query:
            self.filtered_posts = [post for post in self.posts
                                   if query in post['title'].lower() or query in post['author'].lower()]
        else:
            self.filtered_posts = self.posts[:]
        self.current_page = 0
        self.refresh_posts()
    def refresh_posts(self):
        self.clear_layout(self.posts_layout)
        available_width = self.scroll_area.viewport().width()
        min_column_width = 350
        columns = max(1, available_width // min_column_width)
        posts_per_page = self.fixed_row_count * columns
        total_pages = math.ceil(len(self.filtered_posts) / posts_per_page) if posts_per_page else 1
        if self.current_page >= total_pages:
            self.current_page = max(0, total_pages - 1)
        start_index = self.current_page * posts_per_page
        end_index = start_index + posts_per_page
        posts_to_display = self.filtered_posts[start_index:end_index]
        for idx, post in enumerate(posts_to_display):
            row = idx // columns
            col = idx % columns
            post_widget = BlogPostWidget(post)
            self.posts_layout.addWidget(post_widget, row, col)
        total_pages = max(1, total_pages)
        self.page_label.setText(f"Page {self.current_page + 1} of {total_pages}")
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled((self.current_page + 1) < total_pages)
    def next_page(self):
        self.current_page += 1
        self.refresh_posts()
    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.refresh_posts()
    def resizeEvent(self, event):
        self.refresh_posts()
        super().resizeEvent(event)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
