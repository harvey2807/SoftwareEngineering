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

    def showMessage(self, text, title, icon):
        msg = QMessageBox(self)
        msg.setIcon(icon)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def showImportPopup(self):
        self.import_popup = QMessageBox(self)
        self.import_popup.setIcon(QMessageBox.Icon.Information)
        self.import_popup.setText("Đang import vào CSDL...")
        self.import_popup.setWindowTitle("Thông báo")
        self.import_popup.setStandardButtons(QMessageBox.StandardButton.NoButton)
        self.import_popup.setModal(True)
        self.import_popup.show()

    def closeImportPopup(self):
        # Đóng popup thông báo
        if hasattr(self, 'import_popup'):
            self.import_popup.close()

    # 4.2.6 Use Case: Thêm buổi học
    def save_session(self):
        # 6.6.3 Người dùng nhập thông tin vào các trường giao diện:
        # 6.6.4 Người dùng click nút “Lưu buổi học”

        # 6.6.5 Hệ thống kết nối tới cơ sở dữ liệu
        db = mdb.connect(
            host='localhost',
            user='root',
            passwd='',
            db="facerecognitionsystem"
        )
        cursor = db.cursor()

        # 6.6.6 Hệ thống lấy dữ liệu từ input
        session_id = self.id_input.text()
        sessionName = self.sessionName.text()
        startTime = self.startTime.text()
        endTime = self.end_time.text()
        date = self.datetime.date().toString("yyyy-MM-dd")  # Convert date to the proper format
        className = self.classname.currentText()

        # Câu lệnh SQL để chèn dữ liệu
        try:
            # 6.6.7 Hệ thống lấy cId từ bảng classes bằng tên lớp
            query_class = "SELECT cId FROM classes WHERE nameC = %s"
            cursor.execute(query_class, (className,))
            class_result = cursor.fetchone()

            # MF: Lớp học tồn tại
            if class_result:
                # 6.6.8 Hệ thống kiểm tra xem buổi học đã tồn tại với cùng class_id, date, và startTime chưa
                class_id = class_result[0]
                query_check = """
                            SELECT sessionId FROM sessions
                            WHERE cId = %s AND sessionDate = %s AND startTime = %s
                            """
                cursor.execute(query_check, (class_id, date, startTime))
                existing_session = cursor.fetchone()
                # 6.6.9 Nếu có buổi học trùng:
                    # Hiển thị: &quot;Buổi học đã tồn tại vào ngày và giờ này!&quot; bằng QMessageBox.warning Kết thúc Use Case
                if existing_session:
                    # AF(1): Buổi học đã tồn tại → Cảnh báo và kết thúc Use Case
                    print("Lỗi: Buổi học này đã tồn tại vào ngày và giờ này!")
                    QMessageBox.warning(self, "Lỗi", "Buổi học đã tồn tại vào ngày và giờ này!")
                else:
                    # 6.6.10 Nếu không có buổi học trùng: Thực hiện chèn dữ liệu mới vào bảng sessions:
                    query_session = """
                                INSERT INTO sessions (sessionId, cId, sessionName, sessionDate, startTime, endTime)
                                VALUES (%s, %s, %s, %s, %s, %s)
                                """
                    values = (session_id, class_id, sessionName, date, startTime, endTime)
                    # 6.6.11 Thực thi và commit dữ liệu
                    cursor.execute(query_session, values)
                    db.commit()
                    print("Lưu buổi học thành công!")
                    # 6.6.12 Hiển thị thông báo: &quot;Buổi học đã được lưu thành công!&quot; bằng
                    # QMessageBox.information
                    QMessageBox.information(self, "Thành công", "Buổi học đã được lưu thành công!")

                    # 6.6.13 Gọi reset_fields() để làm sạch các ô nhập
                    self.reset_fields()
            else:
                # AF(2): Lớp học không tồn tại
                print("Không tìm thấy lớp học phù hợp.")

        except Exception as e:
            # AF(3): Lỗi hệ thống hoặc lỗi khi insert buổi học
            print(f"Lỗi khi lưu buổi học: {e}")
        # 6.6.14 Đóng kết nối cơ sở dữ liệu
        cursor.close()
        db.close()

    # 4.2.4 Use Case: Sửa thông tin buổi học
    def edit_session(self):
        # 6.4.2 Người dùng nhập ID buổi học vào ô nhập (id_input)
        # 6.4.3 Người dùng nhập các thông tin cập nhật:
            # Tên buổi học (sessionName)
            # Ngày diễn ra (datetime)
            # Giờ bắt đầu (startTime)
            # Giờ kết thúc (endTime)
            # Tên lớp (classname)
        # 6.4.4 Người dùng click nút “Sửa buổi học”

        # 6.4.5 Hệ thống lấy dữ liệu từ input
        session_id = self.id_input.text().strip()

        # 6.4.6 Hệ thống kiểm tra nếu ID buổi học rỗng
        if not session_id:
            # 6.4.7 Nếu rỗng, hiển thị: &quot;ID buổi học không được để trống!&quot;
            # ALTERNATE FLOW (1): Không nhập ID buổi học
            print("ID buổi học không được để trống!")
            return

        # 6.4.8 Hệ thống kết nối đến cơ sở dữ liệu
        try:
            db = mdb.connect(
                host='localhost',
                user='root',
                passwd='',
                db="facerecognitionsystem"
            )
            cursor = db.cursor()

            # 6.4.9 Hệ thống lấy các giá trị từ giao diện
            sessionName = self.sessionName.text()
            startTime = self.startTime.text()
            endTime = self.end_time.text()
            date = self.datetime.date().toString("yyyy-MM-dd")  # Convert date to the proper format
            className = self.classname.currentText()

            # 6.4.10 Hệ thống kiểm tra nếu tất cả các trường đều trống
            if not sessionName and not startTime and not endTime and not date and not className:
                # 6.4.11 Nếu đúng, hiển thị: &quot;Vui lòng nhập đầy đủ thông tin cần thiết!&quot;
                # ALTERNATE FLOW (2): Tất cả các trường trống
                print("Vui lòng nhập đầy đủ thông tin cần thiết!")
                return

            # 6.4.12 Hệ thống truy vấn để lấy classId tương ứng với className từ bảng
            query_class = "SELECT cId FROM classes WHERE nameC = %s"
            cursor.execute(query_class, (className,))
            class_result = cursor.fetchone()
            class_id = class_result[0]

            # 6.4.13 Hệ thống chuẩn bị truy vấn cập nhật buổi học:
            query = """
                    UPDATE sessions
                    SET  CId = %s, sessionName = %s, sessionDate = %s, startTime = %s, endTime = %s
                    WHERE sessionId = %s
                    """
            values = (class_id, sessionName, date, startTime, endTime, session_id)

            # 6.4.14 Hệ thống thực thi truy vấn và commit dữ liệu
            cursor.execute(query, values)
            db.commit()

            # 6.4.15 Nếu không có hàng nào bị ảnh hưởng
            if cursor.rowcount == 0:
                # ALTERNATE FLOW (3): Không tìm thấy session để sửa
                # 6.4.16 Hiển thị: &quot;Không tìm thấy buổi học với ID để sửa.&quot;
                print(f"Không tìm thấy buổi học với ID {session_id} để sửa.")
                # 6.4.17 Xóa các trường nhập liệu
                self.reset_fields()
            # 6.4.18 Nếu sửa thành công
            else:
                # 6.4.19Hiển thị: &quot;Sửa thông tin buổi học với ID thành công!&quot;
                print(f"Sửa thông tin buổi học với ID {session_id} thành công!")
                # 6.4.20 Xóa các trường nhập liệu
                self.reset_fields()

        except Exception as e:
            # 6.4.21 Hệ thống đóng kết nối cơ sở dữ liệu
            # ALTERNATE FLOW (4): Lỗi hệ thống/CSDL
            print(f"Lỗi khi sửa thông tin buổi học: {e}")
        finally:
            cursor.close()
            db.close()

    # 4.2.3 Use case Xóa buổi học
    def delete_session(self):
        # 6.3.3 Người dùng nhập ID buổi học vào ô nhập (id_input)
        # 6.3.4 Người dùng click nút “Xóa buổi học”

        # 6.3.5 Hệ thống lấy session_id từ input
        session_id = self.id_input.text().strip()

        # 6.3.6 Kiểm tra giá trị sessionId
        if not session_id:
            # 6.3.7 Nếu rỗng, hiển thị thông báo: &quot;Cần nhập ID Học sinh để xóa!&quot;
            # ALTERNATE FLOW (1): ID rỗng
            print("Cần nhập ID Học sinh để xóa!")
            return

        # 6.3.7 Hệ thống kết nối tới cơ sở dữ liệu
        try:
            db = mdb.connect(
                host='localhost',
                user='root',
                passwd='',
                db="facerecognitionsystem"
            )
            cursor = db.cursor()

            # Câu lệnh SQL để xóa dữ liệu
            query = "DELETE FROM sessions WHERE sessionId = %s"
            cursor.execute(query, (session_id,))

            # 6.3.8 Hệ thống thực hiện xóa sessionId vừa nhập
            db.commit()

            # 6.3.9 Hệ thống hiện thị thông báo thành công:
            print(f"Xóa thông tin Học sinh với ID {session_id} thành công!")

            # 6.3.10 Xóa các trường nhập liệu:
            self.reset_fields()  # Reset các ô nhập liệu
        except Exception as e:
            # ALTERNATE FLOW (2): Lỗi kết nối hoặc truy vấn CSDL
            print(f"Lỗi khi xóa học sinh: {e}")
        finally:
            # 6.3.11 Hệ thống đóng kết nối CSDL
            cursor.close()
            db.close()

    # 4.2.2 Use Case: Tìm kiếm buổi học
    def search_session(self):
        # 6.2.2 Người dùng nhập từ khóa vào ô tìm kiếm (QLineEdit)
        # 6.2.3 Người dùng click nút &quot;Tìm kiếm&quot;

        # 6.2.4 Hệ thống lấy từ khóa từ ô nhập và loại bỏ khoảng trắng
        keyword = self.search_input.text().strip()

        # 6.2.5 Hệ thống kiểm tra nếu từ khóa rỗng
        if not keyword:
            # 🔀 ALTERNATE FLOW (1): Từ khóa rỗng
            print("Cần nhập từ khóa để tìm kiếm!")
            QMessageBox.warning(self, "Thiếu từ khóa", "Vui lòng nhập từ khóa để tìm kiếm!")
            return

        # 6.2.6 Hệ thống kiểm tra nếu chưa đăng nhập (kiểm tra Global.GLOBAL_ACCOUNTID)
        if not Global.GLOBAL_ACCOUNTID:
            # 6.2.7 Nếu chưa đăng nhập, hiển thị thông báo lỗi: &quot;Chưa đăng nhập hoặc không có ID giáo viên!&quot;
            # ALTERNATE FLOW (2): Chưa đăng nhập
            print("Chưa đăng nhập hoặc không có ID giáo viên!" + Global.GLOBAL_ACCOUNTID)

        # 6.2.8 Hệ thống kết nối đến cơ sở dữ liệu và Thực hiện truy vấn
        try:
            db = mdb.connect(
                host='localhost',
                user='root',
                passwd='',
                db="facerecognitionsystem"
            )
            cursor = db.cursor()
            print(Global.GLOBAL_ACCOUNTID)
            print("%" + keyword + "%")
            query = """
                   SELECT sessionId,sessionName, classes.nameC, sessionDate, startTime, endTime
                   FROM sessions
                   JOIN classes ON sessions.cId = classes.cId
                   JOIN teachers t ON classes.TId = t.TID
                   WHERE classes.nameC LIKE %s AND t.TID = %s
                   """
            cursor.execute(query, ("%" + keyword + "%", Global.GLOBAL_ACCOUNTID))  # Thêm dấu % vào từ khóa
            results = cursor.fetchall()

            # 6.2.9 Thực hiện truy vấn Hệ thống kiểm tra kết quả truy vấn
            if not results:
                # 6.2.10 Nếu không có kết quả, hiển thị thông báo: &quot;Không tìm thấy buổi học nào
                # với từ khóa này.&quot; -> Kết thúc usecase
                # ALTERNATE FLOW (3): Không tìm thấy kết quả
                print("Không tìm thấy buổi học nào với từ khóa này.")
                return

            # 6.2.11 Hệ thống hiển thị kết quả trong bảng (QTableWidget)
            # Duyệt từng hàng kết quả và gán giá trị vào các ô tương ứng
            self.table.setRowCount(len(results))
            for row_idx, row_data in enumerate(results):
                for col_idx, col_data in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        except Exception as e:
            # ALTERNATE FLOW (4): Lỗi khi kết nối hoặc truy vấn CSDL
            print(f"Lỗi khi tìm kiếm: {e}")

    # xem tất cả
    def view_all_session(self):
        try:
            db = mdb.connect(
                host='localhost',
                user='root',
                passwd='',
                db="facerecognitionsystem"
            )
            cursor = db.cursor()
            query = """
                    SELECT sessionId,sessionName, classes.nameC, sessionDate, startTime, endTime
                    FROM sessions
                    JOIN classes ON sessions.cId = classes.cId
                    JOIN teachers t ON classes.TId = t.TID
                    WHERE t.TID = %s
                    """
            cursor.execute(query, (Global.GLOBAL_ACCOUNTID,))
            results = cursor.fetchall()

            # Kiểm tra nếu không có kết quả
            if not results:
                print("Không có buổi học nào trong hệ thống.")
                self.reset_fields()
                return

            # Cập nhật bảng
            self.table.setRowCount(len(results))  # Cập nhật số dòng trong bảng
            # Điền dữ liệu vào bảng
            for row_idx, row_data in enumerate(results):
                for col_idx, col_data in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        except Exception as e:
            print(f"Lỗi khi xem tất cả: {e}")
            self.reset_fields()
        finally:
            cursor.close()
            db.close()

    def loadData(self):
        # Mảng để chứa dữ liệu
        class_names = []
        print(Global.GLOBAL_ACCOUNTID)

        try:
            # Kết nối đến cơ sở dữ liệu
            db = mdb.connect(
                host='localhost',
                user='root',
                passwd='',
                db="facerecognitionsystem"
            )
            cursor = db.cursor()

            # Truy vấn để lấy tên lớp học
            query = """
                    SELECT nameC
                    FROM classes 
                    JOIN teachers t ON classes.TId = t.TID
                    WHERE t.TID = %s
                    """
            cursor.execute(query, (Global.GLOBAL_ACCOUNTID,))  # Lọc theo giáo viên
            results = cursor.fetchall()

            # Kiểm tra nếu không có kết quả
            if not results:
                print("Không có lớp học nào trong hệ thống.")
                return class_names  # Trả về mảng rỗng

            # Lấy dữ liệu từ kết quả truy vấn và lưu vào mảng class_names
            class_names = [result[0] for result in results]  # result[0] là tên lớp học

        except Exception as e:
            print(f"Lỗi khi tải dữ liệu: {e}")

        finally:
            # Đóng kết nối và cursor
            cursor.close()
            db.close()

        return class_names

    # 4.2.1 Use case: Thêm lớp học
    # 6.1.3 Người dùng click nút &quot;Thêm lớp học&quot sẽ gọi hàm add_class_popup vì đã gán sự kiện;
    def add_class_popup(self):
        # 6.1.4: Hệ thống khởi tạo QDialog chứa tên và kích thước màn hình
        dialog = QDialog(self)
        dialog.setWindowTitle("Thêm Lớp Học")
        dialog.setFixedSize(300, 150)

        layout = QVBoxLayout()

        # 6.1.5: Hệ thống khởi tạo QLabel chứa tên màn hình
        label = QLabel("Nhập tên lớp học:")

        # 6.1.6: Hệ thống khởi tạo QLineEdit để nhập tên lớp học
        class_name_input = QLineEdit()
        class_name_input.setPlaceholderText("Tên lớp học...")

        # 6.1.7: Hệ thống khởi tạo QBoxLayout chứa layout cho 2 nút "Thêm" và "Hủy"
        button_layout = QHBoxLayout()

        # 6.1.8: Hệ thống khởi tạo 2 nút Thêm và Hủy và cho vào layout Button
        add_button = QPushButton("Thêm")
        cancel_button = QPushButton("Hủy")
        button_layout.addWidget(add_button)
        button_layout.addWidget(cancel_button)

        # 6.1.9: Thêm các thành phần vào layout chính
        layout.addWidget(label)
        layout.addWidget(class_name_input)
        layout.addLayout(button_layout)

        # 6.1.10: Hệ thống thiết lập layout chính cho QDialog.
        dialog.setLayout(layout)

        # Hàm sự kiện của nút thêm lớp học
        def handle_add_class():

            # 6.1.13 Người dùng nhập tên lớp học vào ô input.

            # 6.1.14 Lấy tên lớp học từ ô input.
            class_name = class_name_input.text().strip()

            # 6.1.14 Người dùng click nút "Thêm".

            # 6.1.15 Hệ thống kiểm tra tên lớp học: nếu hợp lệ → tiếp tục; nếu không → Alternate Flow (1).
            if not class_name:
                # 6.1.16 + Alternate Flow: kiểm tra không hợp lệ
                QMessageBox.warning(dialog, "Lỗi", "Tên lớp học không được để trống!")
                return  # Quay lại bước 13

            # 6.1.17 Hệ thống gọi API hoặc thao tác CSDL để lưu tên lớp học.
            try:
                db = mdb.connect(
                    host='localhost',
                    user='root',
                    passwd='',
                    db="facerecognitionsystem"
                )
                cursor = db.cursor()

                # Thực hiện truy vấn để thêm lớp học
                query = "INSERT INTO classes (nameC, TId) VALUES (%s, %s)"
                cursor.execute(query, (class_name, Global.GLOBAL_ACCOUNTID))
                db.commit()

                # 6.1.18 Hệ thống hiển thị thông báo "Thêm thành công".
                QMessageBox.information(dialog, "Thành công", "Lớp học đã được thêm thành công!")

                # 6.1.19 Hệ thống cập nhật combobox tên lớp học.
                self.classname.addItem(class_name)

                # 6.1.20 Hệ thống đóng QDialog.
                dialog.accept()  # Đóng popup

            except Exception as e:
                # Alternate Flow (2): Gặp lỗi khi thao tác với DB (API hoặc CSDL) -> Kết thúc useCase
                QMessageBox.critical(dialog, "Lỗi", f"Lỗi khi thêm lớp học: {e}")
            finally:
                cursor.close()  
                db.close()

        # 6.1.11 Hệ thống gán sự kiện click cho nút "Thêm" và "Hủy".
        add_button.clicked.connect(handle_add_class)
             # Alternate Flow (3): Người dùng bấm nút "Hủy"
        cancel_button.clicked.connect(dialog.reject)

        # 6.1.12 Hiện Thị Dialog
        dialog.exec()