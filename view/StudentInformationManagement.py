from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QComboBox, QTableWidget, QVBoxLayout,
    QHBoxLayout, QGroupBox, QGridLayout, QHeaderView, QDateTimeEdit, QTableWidgetItem, QStackedWidget, QFileDialog
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap
import sys
import os

# Thêm thư mục gốc vào PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from model.DatabaseManagement import DatabaseManagement

class StudentInformationManagement(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.stacked_widget = stacked_widget
        # Thiết lập tiêu đề và kích thước cửa sổ
        self.setWindowTitle("Quản lý thông tin Học sinh")
        self.setGeometry(100, 100, 1200, 700)

        self.db_manager = DatabaseManagement()  # Initialize the database manager

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
        header_label = QLabel("Quản lý thông tin Học sinh")
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
        student_group = QGroupBox("Thông tin Học sinh")  # Nhóm chứa thông tin học sinh
        student_layout = QGridLayout()  # Layout dạng lưới

        # Nhãn để hiển thị hình ảnh 
        self.photo_label = QLabel("Hình ảnh học sinh")
        self.photo_label.setFixedSize(200, 200)
        self.photo_label.setStyleSheet("border: 1px solid black; background-color: #F0F0F0; border-radius: 5px;")
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Các ô nhập liệu thông tin
        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.class_input = QLineEdit()
        self.cccd_input = QLineEdit()
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["nam", "nữ"])  # Thêm tùy chọn "Nam" và "Nữ
        self.dob_input = QDateTimeEdit(self, calendarPopup=True)
        self.dob_input.setDate(QDate.currentDate())  # Ngày mặc định
        self.dob_input.setDisplayFormat("dd/MM/yyyy")  # Định dạng hiển thị

        calendar = self.dob_input.calendarWidget()
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

        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.address_input = QLineEdit()

        # Thêm các thành phần nhập liệu vào lưới
        student_layout.addWidget(QLabel("ID Học sinh:"), 1, 0)
        student_layout.addWidget(self.id_input, 1, 1)
        student_layout.addWidget(QLabel("Tên Học sinh:"), 1, 2)
        student_layout.addWidget(self.name_input, 1, 3)
        student_layout.addWidget(QLabel("Lớp học:"), 2, 0)
        student_layout.addWidget(self.class_input, 2, 1)
        student_layout.addWidget(QLabel("CCCD:"), 2, 2)
        student_layout.addWidget(self.cccd_input, 2, 3)
        student_layout.addWidget(QLabel("Giới tính:"), 3, 0)
        student_layout.addWidget(self.gender_combo, 3, 1)
        student_layout.addWidget(QLabel("Ngày sinh:"), 3, 2)
        student_layout.addWidget(self.dob_input, 3, 3)
        student_layout.addWidget(QLabel("Email:"), 4, 0)
        student_layout.addWidget(self.email_input, 4, 1)
        student_layout.addWidget(QLabel("SĐT:"), 4, 2)
        student_layout.addWidget(self.phone_input, 4, 3)
        student_layout.addWidget(QLabel("Địa chỉ:"), 5, 0)
        student_layout.addWidget(self.address_input, 5, 1)

        # Thêm nhãn và nút vào layout
        student_layout.addWidget(self.photo_label, 0, 0, 1, 2)  # Tạo khoảng trống cho ảnh

        # Các nút chức năng (Sửa, Xóa)
        button_layout = QHBoxLayout()
        self.edit_button = QPushButton("Sửa")
        self.edit_button.setStyleSheet("background-color: black; color: white;")
        self.delete_button = QPushButton("Xóa")
        self.delete_button.setStyleSheet("background-color: black; color: white;")
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        student_layout.addLayout(button_layout, 6, 0, 1, 4)  # Thêm hàng nút vào layout lưới
        student_group.setLayout(student_layout)  # Đặt layout cho nhóm

        # ----------- Phần hệ thống tìm kiếm (bên phải) -----------
        table_group = QGroupBox("Hệ Thống Tìm kiếm")  # Nhóm chứa bảng và chức năng tìm kiếm
        table_layout = QVBoxLayout()  # Layout dạng dọc

        # Thanh tìm kiếm
        self.search_combo = QComboBox()
        self.search_combo.addItems(["ID Học sinh"])  # Thêm tiêu chí tìm kiếm
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Tìm kiếm")
        self.view_all_button = QPushButton("Xem tất cả")
        self.table = QTableWidget(5, 5)  # Bảng chứa kết quả tìm kiếm
        self.table.setHorizontalHeaderLabels(["ID Học sinh", "Họ tên", "CCCD", "Giới tính", "Lớp"])  # Đặt tên các cột

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

        # Kết nối các sự kiện
        self.edit_button.clicked.connect(self.edit_student)
        self.delete_button.clicked.connect(self.delete_student)
        self.search_button.clicked.connect(self.search_student)
        self.view_all_button.clicked.connect(self.view_all_students)
        self.table.cellClicked.connect(self.display_student_info)  # Kết nối sự kiện click vào bảng

        # Hiển thị tất cả học sinh khi khởi động
        self.view_all_students()

    def reset_fields(self):
        """Reset all input fields"""
        self.id_input.clear()
        self.name_input.clear()
        self.class_input.clear()
        self.cccd_input.clear()
        self.gender_combo.setCurrentIndex(0)  # Chọn lại giá trị mặc định đầu tiên
        self.dob_input.setDate(QDate.currentDate())  # Đặt lại ngày hiện tại
        self.email_input.clear()
        self.phone_input.clear()
        self.address_input.clear()
        self.photo_label.setPixmap(QPixmap())  # xóa hình
        self.photo_label.setText("Hình ảnh học sinh")  # hiện chữ

    def display_student_info(self, row, column):
        """Display student information when clicking on a table row"""
        # Lấy ID học sinh từ cột đầu tiên của dòng được chọn
        student_id = self.table.item(row, 0).text()
        
        # Sử dụng DatabaseManagement để lấy thông tin chi tiết
        results = self.db_manager.get_student_details(student_id)
        
        if results:
            student = results[0]  # Lấy thông tin học sinh đầu tiên
            
            # Hiển thị thông tin học sinh lên các trường nhập liệu
            self.id_input.setText(str(student[0]))  # ID
            self.name_input.setText(str(student[1]))  # Tên
            self.class_input.setText(str(student[2]))  # Lớp
            self.cccd_input.setText(str(student[3]))  # CCCD
            
            # Đặt giới tính
            gender_index = 0 if student[4] == "nam" else 1
            self.gender_combo.setCurrentIndex(gender_index)
            
            # Đặt ngày sinh
            if student[5]:  # Nếu có ngày sinh
                dob = QDate.fromString(str(student[5]), "yyyy-MM-dd")
                self.dob_input.setDate(dob)
            
            # Thông tin liên hệ
            self.email_input.setText(str(student[6]) if student[6] else "")
            self.phone_input.setText(str(student[7]) if student[7] else "")
            self.address_input.setText(str(student[8]) if student[8] else "")
            
            # Hiển thị ảnh nếu có
            photo_path = student[9]
            if photo_path:
                # Đường dẫn đầy đủ đến thư mục ảnh
                project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                image_folder = os.path.join(project_root, photo_path)
                
                # Tìm ảnh đầu tiên trong thư mục
                try:
                    for file in os.listdir(image_folder):
                        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                            image_path = os.path.join(image_folder, file)
                            self.photo_label.setPixmap(QPixmap(image_path).scaled(
                                self.photo_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
                            self.photo_label.setText("")  # Xóa text khi có ảnh
                            break
                    else:
                        self.photo_label.setText("Không có ảnh")
                except Exception as e:
                    print(f"Lỗi khi tải ảnh: {e}")
                    self.photo_label.setText("Lỗi tải ảnh")
            else:
                self.photo_label.setText("Không có ảnh")
                self.photo_label.setPixmap(QPixmap())  # Xóa ảnh nếu có

    def edit_student(self):
        # Kiểm tra dữ liệu ID
        student_id = self.id_input.text().strip()
        if not student_id:
            print("ID Học sinh không được để trống!")
            return

        # Lấy dữ liệu từ giao diện
        name = self.name_input.text().strip()
        student_class = self.class_input.text().strip()
        cccd = self.cccd_input.text().strip()
        gender = self.gender_combo.currentText()
        dob = self.dob_input.date().toString("yyyy-MM-dd")  # Định dạng ngày sinh
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        address = self.address_input.text().strip()

        # Kiểm tra dữ liệu đầu vào
        if not name or not student_class or not cccd:
            print("Vui lòng nhập đầy đủ thông tin cần thiết!")
            return

        # Sử dụng DatabaseManagement để cập nhật thông tin
        rows_affected = self.db_manager.update_student(
            student_id, name, dob, gender, cccd, email, address, phone, student_class
        )

        # Kiểm tra kết quả
        if rows_affected == 0:
            print(f"Không tìm thấy Học sinh với ID {student_id} để sửa.")
        else:
            print(f"Sửa thông tin Học sinh với ID {student_id} thành công!")
            # Cập nhật lại bảng
            self.view_all_students()
        
        self.reset_fields()

    # nút xóa
    def delete_student(self):
        student_id = self.id_input.text().strip()
        if not student_id:
            print("Cần nhập ID Học sinh để xóa!")
            return

        # Sử dụng DatabaseManagement để xóa học sinh
        rows_affected = self.db_manager.delete_student(student_id)
        
        if rows_affected > 0:
            print(f"Xóa thông tin Học sinh với ID {student_id} thành công!")
            # Cập nhật lại bảng
            self.view_all_students()
        else:
            print(f"Không tìm thấy Học sinh với ID {student_id} để xóa.")
            
        self.reset_fields()  # Reset các ô nhập liệu

    # tìm kiếm
    def search_student(self):
        keyword = self.search_input.text()
        if not keyword:
            print("Cần nhập từ khóa để tìm kiếm!")
            return

        # Sử dụng DatabaseManagement để tìm kiếm học sinh
        results = self.db_manager.get_student_by_id(keyword)

        # Cập nhật bảng
        if results:
            self.table.setRowCount(len(results))
            for row_idx, row_data in enumerate(results):
                for col_idx, col_data in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        else:
            self.table.setRowCount(0)
            print("Không tìm thấy học sinh với ID này.")

    def view_all_students(self):
        # Sử dụng DatabaseManagement để lấy tất cả học sinh
        results = self.db_manager.get_all_students()

        if not results:
            print("Không có học sinh nào trong hệ thống.")
            self.reset_fields()
            return

        self.table.setRowCount(len(results))
        for row_idx, row_data in enumerate(results):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = StudentInformationManagement(" ")
    main_window.show()
    sys.exit(app.exec())