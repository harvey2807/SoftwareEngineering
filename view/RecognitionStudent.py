import sys
from PyQt6.QtCore import Qt, QTimer, QDate, QTime
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QPushButton, QLineEdit, QGridLayout, QTableWidget, QHeaderView, QTabWidget, QTableWidgetItem, QApplication, QFileDialog
import cv2
import os
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import MySQLdb as mdb
import Global

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'

#9.1.0. Lớp RecognitionStudentView được khởi tạo với tham chiếu đến stacked wideget
class RecognitionStudentView(QWidget):
    #9.1.1. __init__ () được gọi để khởi tạo giao diện người dùng, kết nối cơ sở dử liệu và tải mô hình nhận diện.
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()
        # Connect to database
        db = mdb.connect(
            host='localhost',
            user='root',
            passwd='',
            db="facerecognitionsystem"
        )
        cursor = db.cursor()

        # Load model
        self.model = load_model("D:\\DangTranTanLuc\\model (91-73).keras")

        self.start_recognition = False
        self.count = 0
        self.recognition_name = 0
        self.fronter = []
        print(self.fronter)

        # Fetch student data
        cursor.execute("select SId, nameSt from students")
        rows = cursor.fetchall()    
        ids = [item[0] for item in rows]
        names = [item[1] for item in rows]
        print(names)
        print(ids)

        self.mapIdtoName = {}
        for i in range(len(ids)):
            self.mapIdtoName[ids[i]] = names[i]
        print(self.mapIdtoName)
        self.label_map = ids

        self.current_image = None

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                color: black;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit, QComboBox, QTableWidget {
                border: 1px solid black;
                border-radius: 4px;
                padding: 6px;
            }
            QPushButton {
                border: 1px solid black;
                border-radius: 4px;
                padding: 8px;
                color: white;
                background-color: #4CAF50;
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

        # Grid Layout
        self.grid_layout = QGridLayout()

        # Recognition Group
        self.recognition_group = QGroupBox("Màn hình nhận diện")
        self.recognition_layout = QVBoxLayout()
        self.recognition_group.setLayout(self.recognition_layout)

        # Class and Session Selection
        choose_layout = QHBoxLayout()
        self.course_label = QLabel("Lớp:")
        self.course_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.course_label.setStyleSheet("border: none")
        self.classname = QLabel("")
        self.classname.setStyleSheet("padding:1px 2px; border: 1px solid gray;")
        self.classname.setFixedHeight(25)

        self.class_label = QLabel("Buổi:")
        self.class_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.class_label.setStyleSheet("border: none")
        self.sessionname = QLabel("")
        self.sessionname.setStyleSheet("padding:1px 2px; border: 1px solid gray;")
        self.sessionname.setFixedHeight(25)

        #9.1.2. Bộ đếm thời gian self.timerzoro được khởi động để gọi loadSessionData() mỗi giây.
        self.timerzoro = QTimer(self)
        self.timerzoro.timeout.connect(
            lambda: self.loadSessionData(
                QDate.currentDate().toString("yyyy-MM-dd"),
                QTime.currentTime().toString("hh:mm:ss")
            )
        )
        self.timerzoro.start(1000)

        choose_layout.addWidget(self.course_label)
        choose_layout.addWidget(self.classname)
        choose_layout.addWidget(self.class_label)
        choose_layout.addWidget(self.sessionname)
        self.recognition_layout.addLayout(choose_layout)

        # Tab Widget
        self.tab = QTabWidget(self)
        self.tab.setStyleSheet("""
            QTabBar::tab:selected { 
                background: white; 
                border-bottom: 1px solid #0078D7;
                padding: 5px;
            }
        """)

        # Table for Attendance
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Tên sinh viên", "Thời gian"])
        self.table.setFixedSize(700, 360)
        header = self.table.horizontalHeader()
        for i in range(self.table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        # Image Display
        self.image_display = QLabel()
        self.image_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_display.setStyleSheet("border: 1px solid black; text-align: center; border-radius: 3px;")
        self.image_display.setFixedSize(700, 360)

        self.tab.addTab(self.image_display, 'Nhận diện')
        self.tab.addTab(self.table, 'Thông tin điểm danh')
        self.recognition_layout.addWidget(self.tab, alignment=Qt.AlignmentFlag.AlignCenter)

        # Buttons
        camera_buttons_layout = QHBoxLayout()
        #9.1.5. Khi giáo viên nhấn vào nút “Tải ảnh”, phương thức load_image() được kích hoạt.
        self.load_image_btn = QPushButton("Tải Ảnh")
        self.load_image_btn.clicked.connect(self.load_image)
        #9.1.18. Khi nhấp vào “Nhận diện lại”, phương thức remove_inf() được gọi
        self.reset_recognition = QPushButton("Nhận diện lại")
        self.reset_recognition.clicked.connect(self.remove_inf)
        #9.1.21. Nhấn lưu danh sách
        self.viewList = QPushButton("Lưu danh sách")
        self.viewList.clicked.connect(self.saveDataToDB)

        camera_buttons_layout.addWidget(self.load_image_btn)
        camera_buttons_layout.addWidget(self.reset_recognition)
        camera_buttons_layout.addWidget(self.viewList)
        self.recognition_layout.addLayout(camera_buttons_layout)

        self.grid_layout.addWidget(self.recognition_group, 0, 0)

        # Student Recognition Info
        self.infor_content = QWidget(self)
        self.infor_playout = QVBoxLayout(self.infor_content)

        session_group = QGroupBox("Nhận diện sinh viên")
        session_layout = QGridLayout()
        session_group.setLayout(session_layout)
        session_group.setStyleSheet("""
            border: 1px solid gray;
            background-color: white; border-radius: 5px;
            padding-top: 5px;
            padding-bottom: 5px;
        """)
        self.label_image = QLabel()
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        session_layout.addWidget(self.label_image)
        self.infor_playout.addWidget(session_group)

        self.attendance_group = QGroupBox("Điểm danh thành công")
        self.attendance_group.setStyleSheet("""
            border: 1px solid gray;
            background-color: white; border-radius: 5px;
            padding-top: 10px;
            padding-right: 5px;
            padding-bottom: 10px;
            margin-top: 10px;
            margin-bottom: 10px;
        """)
        self.attendance_layout = QGridLayout()
        self.attendance_group.setLayout(self.attendance_layout)

        self.id_label = QLabel("ID sinh viên:")
        self.id_label.setStyleSheet("border: none")
        self.id_input = QLineEdit()
        self.id_input.setReadOnly(True)
        self.id_input.setStyleSheet("""
            border: 1px solid #CCCCCC;
            border-radius: 4px;
            padding: 5px;
            margin-bottom: 10px;
        """)

        self.name_label = QLabel("Tên sinh viên:")
        self.name_label.setStyleSheet("border: none")
        self.name_input = QLineEdit()
        self.name_input.setReadOnly(True)
        self.name_input.setStyleSheet("""
            border: 1px solid #CCCCCC;
            border-radius: 4px;
            padding: 5px;
            margin-bottom: 10px;
        """)

        self.time_label = QLabel("Thời gian:")
        self.time_label.setStyleSheet("border: none")
        self.time_input = QLineEdit()
        self.time_input.setReadOnly(True)
        self.time_input.setStyleSheet("""
            border: 1px solid #CCCCCC;
            border-radius: 4px;
            padding: 5px;
            margin-bottom: 10px;
        """)
        self.attendance_layout.addWidget(self.id_label, 0, 0)
        self.attendance_layout.addWidget(self.id_input, 0, 1)
        self.attendance_layout.addWidget(self.name_label, 1, 0)
        self.attendance_layout.addWidget(self.name_input, 1, 1)
        self.attendance_layout.addWidget(self.time_label, 2, 0)
        self.attendance_layout.addWidget(self.time_input, 2, 1)

        self.infor_playout.addWidget(self.attendance_group)
        self.grid_layout.addWidget(self.infor_content, 0, 1)

        self.grid_layout.setColumnStretch(0, 2)
        self.grid_layout.setColumnStretch(1, 1)
        self.setLayout(self.grid_layout)

    #9.1.3. loadSessionData(self, date, time) truy vấn cơ sở dữ liệu để tìm các buổi học đang hoạt động cho giáo viên hiện tại.
    def loadSessionData(self, date, time):
        session_names = []
        print(Global.GLOBAL_ACCOUNTID, date, time)
        try:
            db = mdb.connect(
                host='localhost',
                user='root',
                passwd='',
                db="facerecognitionsystem"
            )
            cursor = db.cursor()
            #Truy vấn nếu thời gian hiện tại nằm giữa thời gian bắt đầu và kết thúc của một buổi hoc.
            query = """
                select c.nameC, s.sessionName
                from sessions s join classes c 
                    on s.CId = c.CId
                where c.TId = %s AND s.sessionDate = %s AND (%s between s.startTime and s.endTime)
            """
            input_data = (Global.GLOBAL_ACCOUNTID, date, time)
            cursor.execute(query, input_data)
            results = cursor.fetchall()
            if not results:
                print("Không có lớp học nào trong hệ thống.")
                session_names = ["", ""]
                #Nếu không tìm thấy buổi học, giá trị trống được hiển thị và chức năng nhận diện bị vô hiệu hóa.
                self.start_recognition = False
            else:
                for data in results[0]:
                    session_names.append(data)
                # Nếu tìm thấy buổi học đang hoạt động, tên lớp và tên buổi học được hiển thị trên giao diện, và chức năng nhận diện được kích hoạt.    
                self.start_recognition = True
            self.classname.setText(session_names[0])
            self.sessionname.setText(session_names[1])
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu: {e}")
        finally:
            cursor.close()
            db.close()
    #9.1.8. face_extractor(img) phát hiện khuôn mặt trong ảnh grayscale sử dụng Haar cascade.
    def face_extractor(self, img):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(img, 1.3, 5)
        if len(faces) == 0:
            return None
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
            cropped_face = img[y:y + h, x:x + w]
            #9.1.9. Trả về những khuôn mặt đã được detected 
            return cropped_face
        return None

    #Phương thức mở hộp thoại chọn tệp cho tệp hình ảnh.
    # 9.1.6. Khi giáo viên nhấn vào nút “Tải ảnh”, phương thức load_image() được kích hoạt.
    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn ảnh", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.current_image = cv2.imread(file_path)
            if self.current_image is None:
                self.image_display.setText("Không thể tải ảnh")
                return
            #Nếu tải thành công, phương thức process_image() được gọi để chuyển đổi ảnh đã tải từ không gian màu BGR sang RGB.
            self.process_image()
    #9.1.7. phương thức process_image() được gọi để chuyển đổi ảnh đã tải từ không gian màu BGR sang RGB
    def process_image(self):
        if self.current_image is None:
            return
        frame = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
        #9.1.6. Một bộ phân loại Haar cascade được sử dụng để phát hiện khuôn mặt trong ảnh.
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(frame, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
        height, width, channel = frame.shape
        step = channel * width
        q_image = QImage(frame.data, width, height, step, QImage.Format.Format_RGB888)
        self.image_display.setPixmap(QPixmap.fromImage(q_image).scaled(700, 360, Qt.AspectRatioMode.KeepAspectRatio))
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
        #9.1.8. face_extractor(img) phát hiện khuôn mặt trong ảnh grayscale sử dụng Haar cascade.
        face = self.face_extractor(gray)

        #9.1.7. Nếu nhận diện được kích hoạt và phát hiện khuôn mặt, update_face_recognitioned() được gọi.
        if self.start_recognition and face is not None:
            self.update_face_recognitioned(face, frame)
    #9.1.10. update_face_recognitioned(face_img, frame1) xử lý khuôn mặt đã trích xuất để nhận diện
    def update_face_recognitioned(self, face_img, frame1):
        image_recognition = face_img
        size = self.label_image.size()
        if image_recognition is not None:
            w, h = image_recognition.shape[:2]
            try:
                #9.1.11. Ảnh khuôn mặt được resize thành 224x224.
                face_resized = cv2.resize(image_recognition, (224, 224))
                im = Image.fromarray(face_resized, 'RGB')
                img_array = np.array(im)
                img_array = np.expand_dims(img_array, axis=0) / 255.0
                #9.1.12. Mô hình đã được train dự đoán ID sinh viên từ khuôn mặt.
                pred = self.model.predict(img_array)
                predicted_class = np.argmax(pred, axis=1)
                #9.1.13. Chỉ số lớp được dự đoán ánh xạ đến ID sinh viên sử dụng self.label_map
                name = self.label_map[predicted_class[0]]
                self.recognition_name = name
                #9.1.14. Tên sinh viên được lấy từ self.mapIdtoName .
                cv2.putText(frame1, self.mapIdtoName[int(name)-1], (0, 15), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 255, 0), 1)
                print(name, self.fronter)
                frame = cv2.cvtColor(face_resized, cv2.COLOR_BGR2RGB)
                height, width, channel = frame.shape
                step = channel * width
                q_image = QImage(frame.data, 224, 224, step, QImage.Format.Format_RGB888)
                #9.1.15. Nếu ID sinh viên nhận diện không có trong self.fronter thì ID sinh viên, tên, thời gian được hiển thị trên giao diện, thông tin này được lưu trong self.data
                if name not in self.fronter:
                    if self.count < 1:
                        self.fronter.append(name)
                        self.id_input.setText(str(name-1))
                        self.name_input.setText(self.mapIdtoName[int(name)-1])
                        self.time_input.setText(QTime.currentTime().toString("hh:mm:ss"))
                        #9.1.16. Thông tin này được lưu trong self.data
                        self.data = [str(name-1), self.mapIdtoName[int(name)-1], QTime.currentTime().toString("hh:mm:ss")]
                        
                        self.saveData(self.data)
                        print("Thông tin học sinh", self.fronter)
                        self.label_image.setPixmap(QPixmap.fromImage(q_image))
                        self.count = 2
                else:
                    self.count = 0
            except Exception as e:
                print(f"Error during face processing: {e}")

    #9.1.19. Khi nhấp vào “Nhận diện lại”, phương thức remove_inf() được gọi
    def remove_inf(self):
        #9.1.17. delete_last_row() xóa mục cuối cùng ra khỏi bảng điểm danh.
        self.delete_last_row()
        name = self.recognition_name
        self.id_input.clear()
        self.name_input.clear()
        self.time_input.clear()
        self.label_image.setPixmap(QPixmap())
        #9.1.18. Nếu sinh viên có trong self.fronter(), nó được xóa để cho phép nhận diện lại.
        if name in self.fronter:
            self.fronter.remove(name)
            print(self.fronter)
        self.count = 0
    #9.1.17. saveData(self.data) thêm thông tin vào bảng điểm danh, ID sinh viên được thêm vào self.fronter để ngăn chặn trùng lặp.
    def saveData(self, data_array):
        current_row = self.table.rowCount()
        self.table.insertRow(current_row)
        for col, value in enumerate(data_array):
            if col < self.table.columnCount():
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(current_row, col, item)

    #9.1.22. Khi nhấn vào “Lưu danh sách”, phương thức saveDataToDB() được gọi.
    def saveDataToDB(self):
        rows = self.table.rowCount()
        cols = self.table.columnCount()
        print("running...")
        data = []
        for row in range(rows):
            row_data = []
            for col in range(cols):
                item = self.table.item(row, col)
                row_data.append(item.text() if item else "")
            data.append(row_data)
        try:
            db = mdb.connect(
                host='localhost',
                user='root',
                passwd='',
                db="facerecognitionsystem"
            )
            cursor = db.cursor()
            query = """
                update studentsinsessions
                set attendance = "present",
                    attendancedTime = %s
                where sessionId in (
                    select sessionId from sessions where sessionName = %s AND CId in (
                    select CId from classes where nameC = %s)) AND SId = %s;
            """
            className = self.classname.text()
            sessionName = self.sessionname.text()
            if isinstance(data, list):
                for item in data:
                    if len(item) >= 3:
                        dataneedsave = (item[2], sessionName, className, int(item[0]))
                        print(cursor.execute(query, dataneedsave))
                        db.commit()
                        print(f"Saved: {item[1]}")
                    else:
                        print("Dữ liệu không hợp lệ trong item:", item)
            else:
                print("Data phải là một danh sách")
        except Exception as e:
            print(f"Lỗi khi lưu: {e}")
        self.fronter.clear()
        self.start_recognition = True
        self.table.setRowCount(0)

    #9.1.2020. delete_last_row() xóa mục cuối cùng ra khỏi bảng điểm danh.
    def delete_last_row(self):
        row_count = self.table.rowCount()
        print("Xóa rồi")
        if row_count > 0:
            self.table.removeRow(row_count - 1)

    def closeEvent(self, event):
        event.accept()  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = RecognitionStudentView(None)
    main_window.show()
    sys.exit(app.exec())