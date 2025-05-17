from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QComboBox, QTableWidget, QVBoxLayout,
    QHBoxLayout, QGroupBox, QGridLayout, QHeaderView, QDateTimeEdit, QTableWidgetItem, QStackedWidget, QMessageBox  
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap
import sys
import os

# Thêm thư mục gốc vào PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from model.DatabaseManagement import DatabaseManagement

# 7.1.2. QTabWidget tự động chuyển đến widget StudentInformationManagement đã được khởi tạo và thêm vào tab trước đó.
class StudentInformationManagement(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.stacked_widget = stacked_widget
        self.setWindowTitle("Quản lý thông tin sinh viên")
        self.setGeometry(100, 100, 1200, 700)

        self.db_manager = DatabaseManagement()

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
            QTableWidget {
                alternate-background-color: #f6f6f6;
                gridline-color: #CCCCCC;
            }
            QTableWidget::item:selected {
                background-color: #2196F3;
                color: white;
            }
            QHeaderView::section {
                background-color: #e0e0e0;
                padding: 4px;
                font-weight: bold;
                border: 1px solid #CCCCCC;
            }
        """)

        # Layout ngoài cùng chứa toàn bộ nội dung
        outer_layout = QVBoxLayout()

        # Tiêu đề chính
        header_label = QLabel("Quản lý thông tin Sinh viên")
        header_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        header_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: black; margin: 0px; padding: 0px;"
        )
        outer_layout.addWidget(header_label)
        outer_layout.addSpacing(10)

        main_layout = QHBoxLayout()

        # ----------- Phần thông tin học sinh (bên trái) -----------
        student_group = QGroupBox("Thông tin Học sinh")
        student_layout = QGridLayout()

        self.photo_label = QLabel("Hình ảnh học sinh")
        self.photo_label.setFixedSize(200, 200)
        self.photo_label.setStyleSheet("border: 1px solid black; background-color: #F0F0F0; border-radius: 5px;")
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.class_input = QLineEdit()
        self.cccd_input = QLineEdit()
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["nam", "nữ"])
        self.dob_input = QDateTimeEdit(self, calendarPopup=True)
        self.dob_input.setDate(QDate.currentDate())
        self.dob_input.setDisplayFormat("dd/MM/yyyy")

        calendar = self.dob_input.calendarWidget()
        calendar.setStyleSheet("""
            QCalendarWidget QTableView {
                selection-background-color: lightblue;
                selection-color: black;
            }
            QCalendarWidget QTableView::item {
                color: black;
                background-color: white;
            }
            QCalendarWidget QHeaderView::section {
                background-color: #1E90FF;
                color: white;
                font-weight: bold;
                border: 1px solid #CCCCCC;
                padding: 5px;
            }
        """)

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
        student_layout.addWidget(self.photo_label, 0, 0, 1, 2)

        button_layout = QHBoxLayout()
        self.edit_button = QPushButton("Sửa")
        self.edit_button.setStyleSheet("background-color: black; color: white;")
        self.delete_button = QPushButton("Xóa")
        self.delete_button.setStyleSheet("background-color: black; color: white;")
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        student_layout.addLayout(button_layout, 6, 0, 1, 4)
        student_group.setLayout(student_layout)

        # ----------- Phần hệ thống tìm kiếm (bên phải) -----------
        table_group = QGroupBox("Hệ Thống Tìm kiếm")
        table_layout = QVBoxLayout()

        class_filter_layout = QHBoxLayout()
        class_filter_layout.addWidget(QLabel("Chọn lớp:"))
        # 7.1.3. Hệ thống khởi tạo ComboBox để chọn lớp.
        self.class_combo = QComboBox()
        self.class_combo.setMinimumWidth(200)
        class_filter_layout.addWidget(self.class_combo)
        class_filter_layout.addStretch()

        table_search_layout = QHBoxLayout()
        table_search_layout.addWidget(QLabel("Tìm kiếm theo ID:"))
        self.search_input = QLineEdit()
        table_search_layout.addWidget(self.search_input)
        self.search_button = QPushButton("Tìm kiếm")
        table_search_layout.addWidget(self.search_button)

        # 7.1.4. Hệ thống khởi tạo bảng hiển thị danh sách sinh viên với 5 cột và 5 dòng.
        self.table = QTableWidget(5, 5)
        self.table.setHorizontalHeaderLabels(["ID Học sinh", "Họ tên", "CCCD", "Giới tính", "Lớp"])
        header = self.table.horizontalHeader()
        for i in range(self.table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        table_layout.addLayout(class_filter_layout)
        table_layout.addLayout(table_search_layout)
        table_layout.addWidget(self.table)
        table_group.setLayout(table_layout)

        main_layout.addWidget(student_group, 2)
        main_layout.addWidget(table_group, 2)
        outer_layout.addLayout(main_layout)
        self.setLayout(outer_layout)

        # 7.1.5. Khi StudentInformationManagement được hiển thị, phương thức load_classes() của đối tượng StudentInformationManagement được gọi (đã được gọi từ init).
        self.load_classes()
        # 7.1.12. Sau khi load_classes() xong, StudentInformationManagement tiếp tục gọi phương thức view_all_students() để tải danh sách tất cả sinh viên từ cơ sở dữ liệu.
        self.view_all_students()

        self.edit_button.clicked.connect(self.edit_student)
        self.delete_button.clicked.connect(self.delete_student)
        self.search_button.clicked.connect(self.search_student)
        self.table.cellClicked.connect(self.display_student_info)
        self.class_combo.currentIndexChanged.connect(self.load_students_by_class)
        self.search_input.returnPressed.connect(self.search_student)

    def load_classes(self):
        """Load all classes into the combobox"""
        # 7.1.6. Phương thức load_classes() gọi đến phương thức get_all_classes() của đối tượng DatabaseManagement.
        classes = self.db_manager.get_all_classes()  
        # 7.1.9. Phương thức load_classes() xóa tất cả các mục hiện có trong class_combo
        self.class_combo.clear()  
        # 7.1.10. Phương thức load_classes() thêm mục "Tất cả các lớp" với giá trị "all" vào đầu ComboBox
        self.class_combo.addItem("Tất cả các lớp", "all")  
        if classes:
            # 7.1.11. Phương thức load_classes() duyệt qua từng lớp trong kết quả truy vấn và thêm vào ComboBox với tên lớp được hiển thị và ID lớp.
            for class_data in classes:
                class_id = class_data[0]
                class_name = class_data[1]
                self.class_combo.addItem(class_name, class_id)

    def view_all_students(self):
        # 7.1.13. Phương thức view_all_students() gọi đến phương thức get_all_students() của đối tượng DatabaseManagement.
        results = self.db_manager.get_all_students()
        # 7.1.16. Phương thức view_all_students() kiểm tra kết quả trả về, nếu không có dữ liệu sẽ hiển thị thông báo
        if not results:
            # 7.2.1. Hiển thị thông báo 
            QMessageBox.information(self, "Không có dữ liệu", "Không tìm thấy sinh viên nào trong hệ thống.")
            self.table.setRowCount(0) # 7.2.2. Xóa tất cả các dòng trong bảng
            self.reset_fields()  # 7.2.3. Xóa tất cả các trường nhập liệu
            return
        # 7.1.17. Thiết lập số dòng cho bảng table
        self.table.setRowCount(len(results))
        # 7.1.18. Duyệt qua từng dòng kết quả và gán giá trị vào bảng
        for row_idx, row_data in enumerate(results):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        if self.table.rowCount() > 0:
            # 7.1.19. Gọi self.table.selectRow(0) để chọn dòng đầu tiên
            self.table.selectRow(0)
            # 7.1.20. Gọi self.display_student_info(0, 0) để hiển thị thông tin chi tiết của sinh viên đầu tiên
            self.display_student_info(0, 0)
      
    def display_student_info(self, row, column):
            # 7.1.21. Phương thức display_student_info(0, 0) lấy ID sinh viên từ ô đầu tiên của dòng đầu tiên
            student_id = self.table.item(row, 0).text()
            # 7.1.22. Phương thức display_student_info() lấy tên lớp từ cột thứ 5 của dòng đầu tiên
            class_name = self.table.item(row, 4).text()
            print(f"Đang tải thông tin học sinh: ID={student_id}, Lớp={class_name}")
            # 7.1.23. Phương thức display_student_info() gọi đến phương thức get_student_by_id_and_class() của đối tượng DatabaseManagement
            student = self.db_manager.get_student_by_id_and_class(student_id, class_name)
            if student and isinstance(student, tuple):
                # 7.1.26. Hiển thị thông tin sinh viên lên các trường nhập liệu
                self.id_input.setText(str(student[0]))
                self.name_input.setText(str(student[1]))
                self.cccd_input.setText(str(student[2]))
                gender_index = 0 if student[3] == "male" else 1
                self.gender_combo.setCurrentIndex(gender_index)
                self.class_input.setText(str(student[4]) if student[4] else "")
                if student[5]:
                    dob = QDate.fromString(str(student[5]), "yyyy-MM-dd")
                    self.dob_input.setDate(dob)
                photo_path = student[6]
                # 7.1.27. Hiển thị ảnh sinh viên
                self.load_image(photo_path)
            else:
                self.reset_fields()
                print(f"Không tìm thấy thông tin chi tiết cho học sinh ID: {student_id}")

    def load_image(self, photo_path):
        #Khi không có đường dẫn ảnh hoặc đường dẫn rỗng
        if not photo_path:
            self.photo_label.setText("Không có ảnh")
            self.photo_label.setPixmap(QPixmap())
            return
            
        # Ghép đường dẫn tuyệt đối từ đường dẫn ảnh trong DB
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        
        # Convert forward slashes to backslashes for Windows
        if os.name == 'nt':  # Check if running on Windows
            photo_path = photo_path.replace('/', '\\')
            
        image_path = os.path.join(project_root, photo_path)
        
        try:
            # Khi file ảnh không tồn tại
            if not os.path.exists(image_path):
                self.photo_label.setText("Không tìm thấy ảnh")
                print(f"Image not found: {image_path}")
                print(f"Project root: {project_root}")
                print(f"Photo path from DB: {photo_path}")
                return

            # Directly try to load the image
            pixmap = QPixmap(image_path)
            # Khi file ảnh không hợp lệ hoặc không thể đọc được
            if pixmap.isNull():
                self.photo_label.setText("Ảnh không hợp lệ")
                print(f"Invalid image format: {image_path}")
                return

            # Hiển thị ảnh đã được scale phù hợp với kích thước label
            self.photo_label.setPixmap(pixmap.scaled(
                self.photo_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
            self.photo_label.setText("")

        # Khi có lỗi xảy ra trong quá trình tải ảnh
        except Exception as e:
            self.photo_label.setText("Lỗi tải ảnh")
            print(f"Error loading image: {e}")
            print(f"Path: {image_path}")

    # Reset các ô nhập liệu
    def reset_fields(self):
        self.id_input.clear()
        self.name_input.clear()
        self.class_input.clear()
        self.cccd_input.clear()
        self.gender_combo.setCurrentIndex(0)  # Chọn lại giá trị mặc định đầu tiên
        self.dob_input.setDate(QDate.currentDate())  # Đặt lại ngày hiện tại
        self.photo_label.setPixmap(QPixmap())  # xóa hình
        self.photo_label.setText("Hình ảnh học sinh")  # hiện chữ

    def edit_student(self):
        # Kiểm tra dữ liệu ID
        student_id = self.id_input.text().strip()
        if not student_id:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập ID Học sinh để sửa.")
            return

        # Lấy dữ liệu từ giao diện
        name = self.name_input.text().strip()
        student_class = self.class_input.text().strip()
        cccd = self.cccd_input.text().strip()
        gender_text = self.gender_combo.currentText()
        if(gender_text == "nam"):
            gender="male"
        else:
            gender="female"
        dob = self.dob_input.date().toString("yyyy-MM-dd")  # Định dạng ngày sinh

        # Kiểm tra dữ liệu đầu vào
        if not name or not student_class or not cccd:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin cần thiết!")
            return

        # Sử dụng DatabaseManagement để cập nhật thông tin
        rows_affected = self.db_manager.update_student(
            student_id, name, dob, gender, cccd, student_class
        )

        # Kiểm tra kết quả
        if rows_affected == 0:
            QMessageBox.warning(self, "Lỗi", f"Không tìm thấy học sinh với ID {student_id} để sửa.")
        else:
            QMessageBox.information(self, "Thành công", f"Đã sửa thông tin học sinh với ID {student_id} thành công.")  
            
            # Get current selected class in combobox
            current_class_index = self.class_combo.currentIndex()
            
            # Cập nhật lại bảng dựa trên lớp đang chọn
            if current_class_index > 0 and self.class_combo.itemData(current_class_index) != "all":
                self.load_students_by_class()
            else:
                self.view_all_students()
                
            # Load thông tin đã sửa, truyền cả ID và lớp học
            self.load_student_to_inputs(student_id, student_class)

    # nút xóa
    def delete_student(self):
        student_id = self.id_input.text().strip()
        if not student_id:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập ID Học sinh để xóa.")
            return
        
        # Hiển thị hộp thoại xác nhận
        reply = QMessageBox.question(
            self,
            "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa học sinh với ID {student_id} không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Sử dụng DatabaseManagement để xóa học sinh
            rows_affected = self.db_manager.delete_student(student_id)
        
            if rows_affected > 0:
                QMessageBox.information(self, "Thành công", f"Đã xóa học sinh với ID {student_id} thành công.")
                
                # Get current selected class in combobox
                current_class_index = self.class_combo.currentIndex()
                
                # Cập nhật lại bảng dựa trên lớp đang chọn
                if current_class_index > 0 and self.class_combo.itemData(current_class_index) != "all":
                    self.load_students_by_class()
                else:
                    self.view_all_students()
            else:
                QMessageBox.warning(self, "Không tìm thấy", f"Không tìm thấy học sinh với ID {student_id} để xóa.")
            
            self.reset_fields()  # Reset các ô nhập liệu

    # tìm kiếm
    def search_student(self):
        student_id = self.search_input.text().strip()
        if not student_id:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập ID học sinh để tìm kiếm.")
            return

        # Sử dụng DatabaseManagement để tìm kiếm học sinh
        try:
            # Kiểm tra xem đang chọn lớp nào trong combobox
            current_class_index = self.class_combo.currentIndex()
            current_class_id = self.class_combo.itemData(current_class_index)
            
            # Nếu đang chọn "Tất cả các lớp", hiển thị tất cả các lớp của học sinh đó
            if current_class_index == 0 or current_class_id == "all":
                # Lấy tất cả các lớp mà học sinh tham gia
                results = self.db_manager.get_all_instances_by_student_id(student_id)
                
                if results:
                    # Hiển thị tất cả các lớp của học sinh này
                    self.table.setRowCount(len(results))
                    for row_idx, row_data in enumerate(results):
                        for col_idx, col_data in enumerate(row_data):
                            self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
                    
                    # Tự động chọn dòng đầu tiên và hiển thị thông tin
                    self.table.selectRow(0)
                    self.display_student_info(0, 0)
                else:
                    self.table.setRowCount(0)
                    QMessageBox.information(self, "Không tìm thấy", f"Không tìm thấy học sinh với ID {student_id}.")
                    self.reset_fields()
            else:
                # Nếu đang chọn một lớp cụ thể, chỉ tìm học sinh trong lớp đó
                class_name = self.class_combo.currentText()
                student = self.db_manager.get_student_by_id_and_class(student_id, class_name)
                
                if student and isinstance(student, tuple):
                    # Hiển thị một hàng duy nhất
                    self.table.setRowCount(1)
                    # Chỉ hiển thị 5 cột đầu tiên phù hợp với bảng
                    for col_idx in range(5):
                        # Đảm bảo không vượt quá số cột trong kết quả
                        if col_idx < len(student):
                            self.table.setItem(0, col_idx, QTableWidgetItem(str(student[col_idx])))
                    
                    # Tự động chọn học sinh vừa tìm thấy để hiển thị chi tiết
                    self.table.selectRow(0)
                    self.display_student_info(0, 0)
                else:
                    self.table.setRowCount(0)
                    QMessageBox.information(self, "Không tìm thấy", 
                                        f"Không tìm thấy học sinh với ID {student_id} trong lớp {class_name}.")
                    self.reset_fields()
        except Exception as e:
            print(f"Lỗi khi tìm kiếm học sinh: {e}")
            QMessageBox.warning(self, "Lỗi", f"Đã xảy ra lỗi khi tìm kiếm: {str(e)}")
            self.table.setRowCount(0)
            self.reset_fields()

    def load_student_to_inputs(self, student_id, class_name=None):
        try:
            student = None
            
            # If class_name is provided, get student by both ID and class
            if class_name:
                student = self.db_manager.get_student_by_id_and_class(student_id, class_name)
                
            # If no class_name provided or no result found, try with just ID
            if not student:
                student = self.db_manager.get_student_by_id(student_id)
            
            if student and isinstance(student, tuple):
                self.id_input.setText(str(student[0]))     # ID
                self.name_input.setText(str(student[1]))   # Tên
                self.cccd_input.setText(str(student[2]))   # CCCD
                
                # Đặt giới tính
                gender_index = 0 if student[3] == "male" else 1
                self.gender_combo.setCurrentIndex(gender_index)
                
                # If class_name was provided but not found in the result, use the provided class name
                if class_name and (not student[4] or student[4] != class_name):
                    self.class_input.setText(class_name)
                else:
                    self.class_input.setText(str(student[4]) if student[4] else "")  # Lớp
                
                # Đặt ngày sinh
                if student[5]:  # Nếu có ngày sinh
                    dob = QDate.fromString(str(student[5]), "yyyy-MM-dd")
                    self.dob_input.setDate(dob)
                
                # Hiển thị ảnh nếu có
                photo_path = student[6]
                self.load_image(photo_path)
            else:
                self.reset_fields()
                print(f"Không tìm thấy thông tin chi tiết cho học sinh ID: {student_id}")
        except Exception as e:
            print(f"Lỗi khi tải thông tin học sinh: {e}")
            self.reset_fields()

    def load_students_by_class(self):
        """Load students based on selected class"""
        try:
            # Get selected class ID
            selected_index = self.class_combo.currentIndex()
            if selected_index < 0:
                return
                
            class_id = self.class_combo.itemData(selected_index)
            
            if class_id == "all":
                # Load all students if "All Classes" is selected
                self.view_all_students()
            else:
                # Load students for the selected class
                results = self.db_manager.get_students_by_class(class_id)
                
                if results:
                    self.table.setRowCount(len(results))
                    for row_idx, row_data in enumerate(results):
                        for col_idx, col_data in enumerate(row_data):
                            self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
                    
                    # Chọn hàng đầu tiên và hiển thị thông tin
                    self.table.selectRow(0)
                    self.display_student_info(0, 0)
                else:
                    self.table.setRowCount(0)
                    self.reset_fields()  # Đảm bảo xóa thông tin cũ
                    QMessageBox.information(self, "Không có dữ liệu", 
                                        f"Không có học sinh nào trong lớp {self.class_combo.currentText()}")
        except Exception as e:
            print(f"Lỗi khi tải danh sách học sinh theo lớp: {e}")
            QMessageBox.warning(self, "Lỗi", f"Đã xảy ra lỗi khi tải danh sách học sinh theo lớp: {str(e)}")
            self.table.setRowCount(0)
            self.reset_fields()

   

