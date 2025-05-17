import MySQLdb as mdb
import numpy as np

class DatabaseManagement:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.db_name = 'facerecognitionsystem'
    
    def connect(self):
        """Create and return a database connection"""
        try:
            db = mdb.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                db=self.db_name
            )
            return db
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return None
    
    def execute_query(self, query, values=None, fetch=False, fetchone=False):
        """Execute a query and return results if needed"""
        db = self.connect()
        if not db:
            return None
        
        cursor = db.cursor()
        result = None
        
        try:
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
                
            if fetchone:
                result = cursor.fetchone()
                # If no record found with fetchone, return None, not 0
                if result is None:
                    return None
            elif fetch:
                result = cursor.fetchall()
            else:
                db.commit()
                result = cursor.rowcount
                
        except Exception as e:
            print(f"Error executing query: {e}")
        finally:
            cursor.close()
            db.close()
            
        return result
    
    def get_student_by_id(self, student_id):
        """Get a student by ID
        Returns a single tuple with student details or None if not found
        """
        query = """
        SELECT s.SId, s.nameSt, s.CCCD, s.gender, c.nameC, s.dob, s.photo_path
        FROM students s
        LEFT JOIN studentsofclass sc ON s.SId = sc.SId
        LEFT JOIN classes c ON sc.CId = c.CId
        WHERE s.SId = %s
        """
        return self.execute_query(query, (student_id,), fetchone=True)
    
    # 7.1.7. DatabaseManagement thực hiện truy vấn đến cơ sở dữ liệu (Database).
    # 7.1.8. Cơ sở dữ liệu (Database) trả về danh sách các lớp (bao gồm CId và nameC).
    def get_all_classes(self):
        query = """
        SELECT CId, nameC 
        FROM classes
        ORDER BY nameC
        """
        result = self.execute_query(query, fetch=True)
        return result if result else []

    # 7.1.14. DatabaseManagement thực hiện truy vấn đến cơ sở dữ liệu (Database).
    # 7.1.15. Cơ sở dữ liệu (Database) trả về danh sách tất cả sinh viên với thông tin cơ bản (ID, tên, CCCD, giới tính, lớp).
    def get_all_students(self):
        query = """
        SELECT s.SId, s.nameSt, s.CCCD, s.gender, c.nameC
        FROM students s
        LEFT JOIN studentsofclass sc ON s.SId = sc.SId
        LEFT JOIN classes c ON sc.CId = c.CId
        """
        result = self.execute_query(query, fetch=True)
        return result if result else []
    
    def get_students_by_class(self, class_id):
        """Get all students in a specific class
        Returns list of student tuples or empty list if none found
        """
        query = """
        SELECT s.SId, s.nameSt, s.CCCD, s.gender, c.nameC
        FROM students s
        JOIN studentsofclass sc ON s.SId = sc.SId
        JOIN classes c ON sc.CId = c.CId
        WHERE c.CId = %s
        """
        result = self.execute_query(query, (class_id,), fetch=True)
        return result if result else []
    
    def delete_student(self, student_id):
        query = "DELETE FROM students WHERE SId = %s"
        return self.execute_query(query, (student_id,))

    def update_student(self, student_id, name, dob, gender, cccd, class_name):
        # Update student information
        query1 = """
        UPDATE students
        SET nameSt = %s, dob = %s, gender = %s, CCCD = %s
        WHERE SId = %s
        """
        values1 = (name, dob, gender, cccd, student_id)
        result1 = self.execute_query(query1, values1)
        
        # Cập nhật lớp học (nếu có)
        if class_name:
            # Get class ID from class name
            class_query = "SELECT CId FROM classes WHERE nameC = %s"
            class_id = self.execute_query(class_query, (class_name,), fetchone=True)
            
            if class_id:
                class_id = class_id[0]
                # Kiểm tra xem có bản ghi nào trong studentsofclass chưa
                check_query = "SELECT * FROM studentsofclass WHERE SId = %s"
                existing = self.execute_query(check_query, (student_id,), fetch=True)
                
                if existing:
                    # Cập nhật bản ghi hiện có
                    query2 = "UPDATE studentsofclass SET CId = %s WHERE SId = %s"
                    values2 = (class_id, student_id)
                else:
                    # Thêm bản ghi mới
                    query2 = "INSERT INTO studentsofclass (CId, SId) VALUES (%s, %s)"
                    values2 = (class_id, student_id)
                    
                self.execute_query(query2, values2)
        
        return result1

    # 7.1.24. Truy vấn SQL chi tiết để lấy toàn bộ thông tin của sinh viên có ID và lớp tương ứng.
    # 7.1.25. Cơ sở dữ liệu (Database) trả về thông tin chi tiết của sinh viên.
    def get_student_by_id_and_class(self, student_id, class_name):
        query = """
        SELECT s.SId, s.nameSt, s.CCCD, s.gender, c.nameC, s.dob, s.photo_path
        FROM students s
        JOIN studentsofclass sc ON s.SId = sc.SId
        JOIN classes c ON sc.CId = c.CId
        WHERE s.SId = %s AND c.nameC = %s
        """
        return self.execute_query(query, (student_id, class_name), fetchone=True)

    def get_all_instances_by_student_id(self, student_id):
        """Get all instances of a student across all classes
        Returns a list of tuples with student details or empty list if none found
        """
        query = """
        SELECT s.SId, s.nameSt, s.CCCD, s.gender, c.nameC
        FROM students s
        JOIN studentsofclass sc ON s.SId = sc.SId
        JOIN classes c ON sc.CId = c.CId
        WHERE s.SId = %s
        """
        result = self.execute_query(query, (student_id,), fetch=True)
        return result if result else []





    def get_attendance_data(self):
        """Lấy dữ liệu học sinh có điểm danh"""
        query = """
        SELECT c.nameC, s.SId, s.nameSt, ses.sessionName, ses.sessionDate 
        FROM classes c
        JOIN sessions ses ON c.CId = ses.CId
        JOIN studentsInSessions ss ON ses.sessionId = ss.sessionId
        JOIN students s ON ss.SId = s.SId
        WHERE ss.attendance = 'present'
        ORDER BY c.CId, ss.sessionId, s.nameSt
        """
        result = self.execute_query(query, fetch=True)
        return result if result else []

    def get_no_attendance_data(self):
        """Lấy dữ liệu học sinh không điểm danh"""
        query = """
        SELECT c.nameC, s.SId, s.nameSt, ses.sessionName, ses.sessionDate 
        FROM classes c
        JOIN sessions ses ON c.CId = ses.CId
        JOIN studentsInSessions ss ON ses.sessionId = ss.sessionId
        JOIN students s ON ss.SId = s.SId
        WHERE ss.attendance = 'absent'
        ORDER BY c.CId, ses.sessionId, s.nameSt
        """
        result = self.execute_query(query, fetch=True)
        return result if result else []

    def get_class_statistics(self):
        """Lấy danh sách lớp và thống kê điểm danh"""
        # Lấy danh sách tất cả các lớp
        query_classes = """
        SELECT CId, nameC
        FROM classes
        ORDER BY CId
        """
        classes_result = self.execute_query(query_classes, fetch=True)
        class_names = {row[0]: row[1] for row in classes_result} if classes_result else {}

        # Lấy số học sinh có điểm danh
        query_present = """
        SELECT c.nameC, COUNT(ss.SId) AS present_students_count
        FROM classes c
        JOIN sessions s ON c.CId = s.CId
        JOIN studentsinsessions ss ON s.sessionId = ss.sessionId
        WHERE ss.attendance = 'present'
        GROUP BY c.CId
        """
        present_result = self.execute_query(query_present, fetch=True)
        hoc_sinh_co_diem_danh = {row[0]: row[1] for row in present_result} if present_result else {}

        # Lấy số học sinh vắng
        query_absent = """
        SELECT c.nameC, COUNT(ss.SId) AS absent_students_count
        FROM classes c
        JOIN sessions s ON c.CId = s.CId
        JOIN studentsInSessions ss ON s.sessionId = ss.sessionId
        WHERE ss.attendance = 'absent'
        GROUP BY c.CId
        """
        absent_result = self.execute_query(query_absent, fetch=True)
        hoc_sinh_vang = {row[0]: row[1] for row in absent_result} if absent_result else {}

        return class_names, hoc_sinh_co_diem_danh, hoc_sinh_vang

   