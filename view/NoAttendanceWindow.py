from BaseTableWindow import BaseTableWindow
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QHeaderView
)
from PyQt6.QtCore import Qt
import sys
import os

# Thêm thư mục gốc vào PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from model.DatabaseManagement import DatabaseManagement


class NoAttendanceWindow(BaseTableWindow):
    def __init__(self):
        super().__init__("Học sinh không điểm danh")

        # Khởi tạo DatabaseManagement
        self.db_manager = DatabaseManagement()

        # Lấy dữ liệu từ DatabaseManagement
        data = self.db_manager.get_no_attendance_data()

        # Điền dữ liệu vào bảng
        self.table.setRowCount(len(data))
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))