from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QProgressBar, QLabel
)
from PySide6.QtCore import Qt, QTimer, QCoreApplication
from PySide6.QtGui import QFont
import sys
import subprocess
import os


class SplashScreen(QWidget):
    """
    Splash screen that loads for a few seconds, then runs:
    1) updater.py
    2) app.py
    using PowerShell.
    """

    def __init__(self):
        super().__init__()

        self.updater_script = "updater.py"
        self.main_app_script = "app.py"

        self.setWindowTitle("GW IDE Loading")
        self.setGeometry(300, 300, 500, 200)

        # Remove frame & center
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.center_window()

        self.init_ui()
        self.show()

        # Duration (4 seconds)
        self.loading_duration_ms = 4000

        # Launch timer
        self.launch_timer = QTimer(self)
        self.launch_timer.timeout.connect(self.run_updater)
        self.launch_timer.start(self.loading_duration_ms)

        # Progress animation
        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_timer.start(40)

        self.progress_increment = 100 / (self.loading_duration_ms / 40)
        self.current_progress = 0

    def init_ui(self):
        """UI setup."""
        self.setStyleSheet("""
            QWidget {
                background-color: #2C2D2D;
                border-radius: 15px;
            }
            QLabel#title_label {
                color: #61afef;
                font-size: 24pt;
                font-weight: bold;
            }
            QProgressBar {
                border: 1px solid #56b6c2;
                border-radius: 7px;
                text-align: center;
                background-color: #3e4451;
            }
            QProgressBar::chunk {
                background-color: #56b6c2;
                border-radius: 7px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        title_label = QLabel("GW IDE v1.0.1.5 BETA")
        title_label.setObjectName("title_label")
        title_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(title_label)

        self.status_label = QLabel("Initializing core modules...")
        self.status_label.setFont(QFont("Segoe UI", 10))
        self.status_label.setStyleSheet("color: #abb2bf;")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def center_window(self):
        qr = self.frameGeometry()
        cp = QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def update_progress(self):
        if self.current_progress < 100:
            self.current_progress += self.progress_increment
            self.progress_bar.setValue(min(100, int(self.current_progress)))

            if self.current_progress < 30:
                self.status_label.setText("Initializing core modules...")
            elif self.current_progress < 60:
                self.status_label.setText("Loading plugins and settings...")
            elif self.current_progress < 90:
                self.status_label.setText("Compiling UI...")
            else:
                self.status_label.setText("Launching updater...")
        else:
            self.progress_bar.setValue(100)

    # --------------------------------------------------
    # ------------  POWERSHELL LAUNCH LOGIC ------------
    # --------------------------------------------------

    def run_powershell_script(self, script_name):
        """Launches a .py script using PowerShell and absolute paths."""

        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        script_path = os.path.join(base_dir, script_name)
        script_path = f'"{script_path}"'

        ps_command = [
            "powershell",
            "-ExecutionPolicy", "Bypass",
            "-NoProfile",
            "-Command",
            f'& "{sys.executable}" {script_path}'
        ]

        subprocess.Popen(ps_command, shell=True)
        print("RUNNING:", ps_command)

    def run_updater(self):
        """Run updater, then main app."""
        self.launch_timer.stop()
        self.progress_timer.stop()

        print("Launching app.py...")
        self.run_powershell_script(self.main_app_script)

        # Close splash screen
        QCoreApplication.instance().quit()


# --------------------------------------------------
# -------------------   MAIN   ---------------------
# --------------------------------------------------

if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = SplashScreen()
    sys.exit(app.exec())
