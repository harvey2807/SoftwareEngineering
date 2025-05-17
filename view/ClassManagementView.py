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

    def reset_fields(self):
        self.id_input.clear()
        self.sessionName.clear()
        self.classname.setCurrentIndex(0)  # Chọn lại giá trị mặc định đầu tiên
        self.datetime.setDate(QDate.currentDate())  # Đặt lại ngày hiện tại
        self.end_time.clear()
        self.startTime.clear()

    # 4.2.5 Use Case: Import lớp học
    def importFile(self):

        # 6.5.3 Người dùng click nút &quot;Import lớp học&quot;

        # 6.5.4 Hệ thống mở hộp thoại cho phép người dùng chọn file Excel
        file, _ = QFileDialog.getOpenFileName(self, "Chọn file Excel để import", "", "Excel Files (*.xls *.xlsx)")

        # 6.5.5 Nếu không có file được chọn, dừng quá trình
        if not file:
            return

        # 6.5.6 Nếu có file, hệ thống đọc dữ liệu từ file Excel sử dụng pandas
        try:
            # Đọc dữ liệu từ file Excel sử dụng pandas
            df = pd.read_excel(file, engine='openpyxl')  # Đọc tệp .xlsx

            db = mdb.connect(
                host='localhost',
                user='root',
                passwd='',
                db="facerecognitionsystem")
            cursor = db.cursor()

            # 6.5.7 Duyệt file
            for index, row in df.iterrows():
                try:
                    # 6.5.8 Lấy dữ liệu từng dòng
                    classname = row['Lớp']
                    sessionname = row['Tên buổi']
                    startDate = pd.to_datetime(row["Ngày bắt đầu"], format="%y/%m/%d", errors='coerce')
                    endDate = pd.to_datetime(row["Ngày kết thúc"], format="%yy/%m/%d", errors='coerce')
                    time = row["Thời gian"]

                    # 6.5.9 Kiểm tra dữ liệu trong file (ngày tháng có hợp lệ)
                    if pd.isna(startDate) or pd.isna(endDate) or startDate > endDate:
                        # 6.5.10 Nếu dữ liệu không hợp lệ, hiển thị thông báo lỗi và dừng quá trình
                        QMessageBox.warning(self, "Lỗi",
                                            f"Ngày bắt đầu hoặc kết thúc không hợp lệ tại dòng {index + 1}")
                        break

                    # 6.5.11 Kiểm tra lớp học có tồn tại trong cơ sở dữ liệu hay không
                    check_query = "SELECT COUNT(*) FROM classes WHERE nameC = %s and TId = %s"
                    cursor.execute(check_query, (classname, Global.GLOBAL_ACCOUNTID))
                    result = cursor.fetchone()


                    if result[0] == 0:
                        # MAIN FLOW: Lớp học chưa tồn tại → thêm mới
                        query = "INSERT INTO classes (nameC, TId) VALUES (%s, %s)"
                        cursor.execute(query, (classname, Global.GLOBAL_ACCOUNTID))
                        db.commit()
                        class_id = cursor.lastrowid
                    else:
                        print("vao day")
                        #  MAIN FLOW: Lớp học đã tồn tại → lấy class_id
                        # Nếu lớp học đã tồn tại, lấy ID của lớp học
                        query_get_id = "SELECT CId FROM classes WHERE nameC = %s  and TId = %s"
                        cursor.execute(query_get_id, (classname, Global.GLOBAL_ACCOUNTID))
                        class_id = cursor.fetchone()[0]

                    # 6.5.12 Tính số tuần
                    weeks = ((endDate - startDate).days // 7) + 1
                    for n in range(weeks + 1):
                        date = startDate + timedelta(weeks=n)
                        # Tách chuỗi bằng dấu '-'
                        start_time, end_time = map(str.strip, time.split('-'))

                        # 6.5.13 Kiểm tra trùng buổi học
                        query_check = """
                                    SELECT sessionId FROM sessions
                                    WHERE cId = %s AND sessionDate = %s AND startTime = %s
                                    """
                        cursor.execute(query_check, (class_id, date, start_time))
                        existing_session = cursor.fetchone()

                        # ALTERNATE FLOW (3): Buổi học trùng
                        if existing_session:
                            QMessageBox.warning(self, "Lỗi", f"Buổi học đã trùng vào {date} và {start_time}!")
                            break
                        else:
                            # 6.5.14 Thêm buổi học mới
                            query_session = """
                                        INSERT INTO sessions (cId, sessionName, sessionDate, startTime, endTime)
                                        VALUES (%s, %s, %s, %s, %s)
                                        """
                            values = (class_id, sessionname, date, start_time, end_time)
                            cursor.execute(query_session, values)
                            db.commit()
                            print("Lưu buổi học thành công!")
                except Exception as e:
                    # ALTERNATE FLOW (4): Lỗi khi thêm dòng
                    db.rollback()
                    QMessageBox.warning(self, "Lỗi", f"Lỗi khi lưu buổi học: {e}")
                    print(f"Lỗi khi lưu buổi học:" + e)
                    break
            # 6.5.15 Đóng kết nối
            cursor.close()
            db.close()

            # 6.5.16 Cập nhật lại danh sách lớp học
            class_id = self.loadData()
            self.classname.clear()
            self.classname.addItems(class_id)
            print("load du lieu da luu")
            self.closeImportPopup()
            self.showMessage("Dữ liệu đã được import thành công!", "Thông báo", QMessageBox.Icon.Information)
        except Exception as e:
            # ALTERNATE FLOW (5): Lỗi khi đọc file
            db.rollback()
            self.closeImportPopup()
            self.showMessage(f"Đã có lỗi khi đọc file: {str(e)}", "Lỗi", QMessageBox.Icon.Critical)

    