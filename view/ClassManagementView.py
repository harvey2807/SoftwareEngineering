from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QComboBox, QTableWidget, QVBoxLayout, QFileDialog,
    QHBoxLayout, QGroupBox, QGridLayout, QHeaderView, QDateTimeEdit, QTableWidgetItem, QMessageBox, QDialog,
    QStackedWidget

)
from PyQt6.QtCore import Qt, QDate
import MySQLdb as mdb
from datetime import timedelta
import pandas as pd
import Global


class ClassManagementView(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.stacked_widget = stacked_widget
        # Thiết lập tiêu đề và kích thước cửa sổ
        self.setWindowTitle("Quản lý thông tin Học sinh")
        self.setGeometry(100, 100, 1200, 700)
        # Định nghĩa CSS để tạo giao diện
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                color: black;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit, QComboBox, QTableWidget, QDateTimeEdit {
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 6px;
            }
            QPushButton {
                border: 1px solid black;
                border-radius: 4px;
                padding: 8px;
                color white;           
            }
            QPushButton:hover {
                background-color: black;
                color: white;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid gray;
                margin-top: 10px;
                padding: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                padding: 4px;
            }
        """)

        # Layout ngoài cùng chứa toàn bộ nội dung
        outer_layout = QVBoxLayout()

        # Tiêu đề chính
        header_label = QLabel("Quản lý thông tin lớp học")
        header_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Căn giữa tiêu đề
        header_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: black; margin: 0px; padding: 0px;"
        )
        outer_layout.addWidget(header_label)  # Thêm tiêu đề vào layout ngoài

        # Spacer nhỏ để tạo khoảng cách giữa tiêu đề và nội dung
        outer_layout.addSpacing(10)

        # Layout chính (chứa hai phần: thông tin học sinh và hệ thống tìm kiếm)
        main_layout = QHBoxLayout()

        # ----------- Phần thông tin học sinh (bên trái) -----------
        student_group = QGroupBox("Thông tin buổi học")
        student_layout = QGridLayout()

        # Các ô nhập liệu thông tin
        self.id_input = QLineEdit()
        self.startTime = QLineEdit()
        self.end_time = QLineEdit()
        self.datetime = QDateTimeEdit(self, calendarPopup=True)
        self.datetime.setDate(QDate.currentDate())  # Ngày mặc định
        self.datetime.setDisplayFormat("dd/MM/yyyy")  # Định dạng hiển thị
        calendar = self.datetime.calendarWidget()
        calendar.setStyleSheet("""
            QCalendarWidget QTableView {
                selection-background-color: lightblue; /* Màu nền khi chọn */
                selection-color: black; /* Màu chữ khi chọn */
            }

            QCalendarWidget QTableView::item {
                color: black; /* Màu chữ mặc định của các ngày */
                background-color: white; /* Màu nền mặc định của các ngày */
            }

            QCalendarWidget QHeaderView::section {
                background-color: #1E90FF; /* Màu nền của hàng thứ */
                color: white; /* Màu chữ của hàng thứ */
                font-weight: bold;
                border: 1px solid #CCCCCC;
                padding: 5px;
            }
        """)
        self.sessionName = QLineEdit()
        self.classname = QComboBox()
        class_names = self.loadData()
        self.classname.addItems(class_names)

        # Thêm các thành phần nhập liệu vào lưới
        student_layout.addWidget(QLabel("ID Buổi học:"), 1, 0)
        student_layout.addWidget(self.id_input, 1, 1)
        student_layout.addWidget(QLabel("Tên Buổi học:"), 2, 0)
        student_layout.addWidget(self.sessionName, 2, 1)
        student_layout.addWidget(QLabel("Giờ bắt đầu:"), 3, 0)
        student_layout.addWidget(self.startTime, 3, 1)
        student_layout.addWidget(QLabel("Giờ kết thúc:"), 4, 0)
        student_layout.addWidget(self.end_time, 4, 1)
        student_layout.addWidget(QLabel("Ngày :"), 5, 0)
        student_layout.addWidget(self.datetime, 5, 1)
        student_layout.addWidget(QLabel("Lớp :"), 6, 0)
        student_layout.addWidget(self.classname, 6, 1)

        # Các nút chức năng (Lưu, Sửa, Xóa)
        button_layout = QHBoxLayout()

        # 6.1.1: Khởi tạo nút "Thêm lớp học"
        self.addclass_button = QPushButton("Thêm lớp học")
        self.addclass_button.setStyleSheet("background-color: black; color: white;")

        # 6.5.1 Khởi tạo nút &quot;Import lớp học&quot;
        self.import_button = QPushButton("Import")
        self.import_button.setStyleSheet("background-color: black; color: white;")

        self.addclass_button = QPushButton("Thêm lớp học")
        self.addclass_button.setStyleSheet("background-color: black; color: white;")

        # 6.6.1: Hệ thống khởi tạo nút "Lưu buổi học"
        self.save_button = QPushButton("Lưu")
        self.save_button.setStyleSheet("background-color: black; color: white;")

        # 6.4.1 Khởi tạo nút "Sửa"
        self.edit_button = QPushButton("Sửa")
        self.edit_button.setStyleSheet("background-color: black; color: white;")

        # 6.3.1 Khởi tạo nút "Xóa"
        self.delete_button = QPushButton("Xóa")
        self.delete_button.setStyleSheet("background-color: black; color: white;")

        # Thay thế QHBoxLayout bằng QGridLayout
        button_layout = QGridLayout()

        # Thêm các nút vào layout lưới, chia thành 2 dòng, mỗi dòng 3 ô
        buttons = [
            self.import_button, self.addclass_button, self.save_button,
            self.edit_button, self.delete_button
        ]

        for index, button in enumerate(buttons):
            row = index // 3  # Dòng hiện tại
            col = index % 3  # Cột hiện tại
            button_layout.addWidget(button, row, col)

        # Thêm layout nút vào layout chính
        student_layout.addLayout(button_layout, 7, 0, 2, 3)  # Chiếm 2 dòng, 3 cột
        student_group.setLayout(student_layout)

        # ----------- Phần hệ thống tìm kiếm (bên phải) -----------
        table_group = QGroupBox("Hệ Thống Tìm kiếm")  # Nhóm chứa bảng và chức năng tìm kiếm
        table_layout = QVBoxLayout()  # Layout dạng dọc

        # Thanh tìm kiếm
        self.search_combo = QComboBox()
        self.search_combo.addItems(["Tên lớp học"])  # Thêm tiêu chí tìm kiếm
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Tìm kiếm")
        self.view_all_button = QPushButton("Xem tất cả")
        self.table = QTableWidget(5, 5)  # Bảng chứa kết quả tìm kiếm
        self.table.setHorizontalHeaderLabels(
            ["ID", "Tên buổi học", "Lớp", "Ngày", "Giờ bắt đầu", "Giờ kết thúc"])  # Đặt tên các cột

        # Điều chỉnh kích thước các cột trong bảng
        header = self.table.horizontalHeader()
        for i in range(self.table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        # Layout chứa thanh tìm kiếm
        table_search_layout = QHBoxLayout()
        table_search_layout.addWidget(QLabel("Tìm kiếm theo:"))
        table_search_layout.addWidget(self.search_combo)
        table_search_layout.addWidget(self.search_input)
        table_search_layout.addWidget(self.search_button)
        table_search_layout.addWidget(self.view_all_button)

        # Thêm thanh tìm kiếm và bảng vào layout
        table_layout.addLayout(table_search_layout)
        table_layout.addWidget(self.table)
        table_group.setLayout(table_layout)  # Đặt layout cho nhóm

        # ----------- Thêm các phần vào layout chính -----------
        main_layout.addWidget(student_group, 2)  # Phần bên trái (thông tin học sinh)
        main_layout.addWidget(table_group, 2)  # Phần bên phải (hệ thống tìm kiếm)

        # Thêm layout chính vào outer_layout
        outer_layout.addLayout(main_layout)

        # Đặt outer_layout làm layout chính của cửa sổ
        self.setLayout(outer_layout)

        # 6.5.2 Tạo sự kiện click cho nút &quot;Import lớp học&quot;
        self.import_button.clicked.connect(self.importFile)

        # 6.1.2 Tạo sự kiện Click nút &quot;Thêm lớp học&quot;
        self.addclass_button.clicked.connect(self.add_class_popup)

        # 6.6.2 Hệ thống gán sự kiện cho nút &quot;Lưu buổi học&quot;
        self.save_button.clicked.connect(self.save_session)

        # 6.4.2 Hệ thống gán sự kiện cho nút “Sửa buổi học”
        self.edit_button.clicked.connect(self.edit_session)

        # 6.3.2 Hệ thống gắn sự kiện cho nút “Xóa buổi học”
        self.delete_button.clicked.connect(self.delete_session)

        # 6.2.1 Hệ thống khởi tạo và gắn sự kiện cho nút &quot;Tìm kiếm&quot;
        self.search_button.clicked.connect(self.search_session)
        self.view_all_button.clicked.connect(self.view_all_session)

