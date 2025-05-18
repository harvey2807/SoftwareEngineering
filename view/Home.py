import sys

from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QTabWidget, QPushButton, QLabel, QFrame, QHBoxLayout, QVBoxLayout, QStackedWidget
)
from PyQt6.QtCore import Qt, QTimer, QTime, QDate, QSize

from StudentInformationManagement import StudentInformationManagement
from SystemStatistics import SystemStatistics

# 7.0.1. Đang ở trang Home này
class Home(QWidget):
    def __init__(self,stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setWindowTitle('Face Recognition System')
        self.setGeometry(0, 0, 1200, 700)
        self.setStyleSheet("color: black;")
        self.init_ui()

    def init_ui(self):
        # Một QVBoxLayout (self.main_layout) được tạo và gán cho main_widget.
        self.central_widget = QWidget(self)
        self.central_widget.setFixedSize(1200, 700)
        self.central_widget.setStyleSheet("background-color: lightblue;")

        self.panel = QFrame(self.central_widget)
        self.panel.setGeometry(15, 15, 1150, 650)
        self.panel.setStyleSheet("""
                           background-color: white;
                           border-radius: 10px;
                       """)

        self.header_panel = QFrame(self.panel)
        self.header_panel.setGeometry(0, 0, 1150, 50)
        self.header_panel.setStyleSheet("""
                            background-color: white;
                            border-top-right-radius: 10px;
                            border-top-left-radius: 10px;
                            border-bottom: 1px solid black;
                        """)

        self.clock_icon = QLabel()
        self.clock_icon.setPixmap(QPixmap('../Image/clock-icon.png').scaled(35, 30))
        self.clock_icon.setStyleSheet("border: none;")

        self.time_date_panel = QFrame(self.header_panel)
        self.time_date_panel.setGeometry(50, 5, 150, 40)
        self.time_date_layout = QVBoxLayout(self.time_date_panel)
        self.time_date_layout.setContentsMargins(0, 0, 0, 0)
        self.time_date_panel.setStyleSheet("border: none;")

        self.time_label = QLabel()
        self.time_label.setStyleSheet("font-size: 12px; font-weight: bold; border: none;")
        self.time_date_layout.addWidget(self.time_label)

        self.date_label = QLabel()
        self.date_label.setStyleSheet("font-size: 12px; font-weight: bold; border: none;")
        self.time_date_layout.addWidget(self.date_label)

        self.title_label = QLabel("Hệ thống nhận diện khuôn mặt")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_panel = QFrame(self.header_panel)
        self.title_panel.setGeometry(400, 5, 550, 40)
        self.title_panel.setStyleSheet("border: none;")

        self.title_layout = QHBoxLayout(self.title_panel)
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_layout.addWidget(self.title_label)

        self.header_layout = QHBoxLayout(self.header_panel)
        self.header_layout.setContentsMargins(10, 5, 10, 5)
        self.header_layout.setSpacing(10)
        self.header_layout.addWidget(self.clock_icon)
        self.header_layout.addWidget(self.time_date_panel)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.title_panel)
        self.header_layout.addStretch()

        #Tạo main_widget và gán layout
        self.main_widget = QWidget(self.panel)
        self.main_widget.setStyleSheet("background-color: white;")
        self.main_widget.setGeometry(0, 50, 1150, 600)
        self.main_layout = QVBoxLayout(self.main_widget)

        # Tạo một QTabWidget (self.tab) và thiết lập style cho nó với CSS để hiển thị tab đang chọn với nền trắng và đường viền màu xanh (#0078D7).
        self.tab = QTabWidget(self.main_widget)
        self.tab.setStyleSheet("""
            QTabBar::tab:selected { 
                background: white; 
                border-bottom: 1px solid #0078D7;
                padding: 5px;
            }
        """)

        # Khởi tạo một đối tượng StudentInformationManagement.
        self.StudentInformationManagement = StudentInformationManagement(self)
        # Khởi tạo một đối tượng SystemStatistics.
        self.SystemStatistics = SystemStatistics(self)

        # QTabWidget thêm StudentInformationManagement làm tab mới với tên "Quản lí sinh viên" thông qua phương thức addTab.
        self.tab.addTab(self.StudentInformationManagement, 'Quản lí sinh viên')
        self.tab.addTab(self.SystemStatistics, 'Thống kê')

    # 6.1.0 Chọn tab "Thống kê" từ  QTabWidget
        # QTabWidget được thêm vào main_layout thông qua phương thức addWidget.
        self.main_layout.addWidget(self.tab)

        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        self.update_time()

    def update_time(self):
        self.time_label.setText(QTime.currentTime().toString("hh:mm:ss"))
        self.date_label.setText(QDate.currentDate().toString("dd/MM/yyyy"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    from PyQt6.QtWidgets import QStackedWidget
    stacked = QStackedWidget()
    home = Home(stacked)
    home.show()
    sys.exit(app.exec())

      