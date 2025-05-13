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
    
    def execute_query(self, query, values=None, fetch=False):
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
                
            if fetch:
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
        """Get student information by ID"""
        query = "SELECT SId, nameSt, CCCD, gender, `class` FROM students WHERE SId = %s"
        return self.execute_query(query, (student_id,), fetch=True)
    
    def get_all_students(self):
        """Get all students"""
        query = "SELECT SId, nameSt, CCCD, gender, `class` FROM students"
        return self.execute_query(query, fetch=True)
    
    def update_student(self, student_id, name, dob, gender, cccd, email, address, phone, student_class):
        """Update student information"""
        query = """
        UPDATE students
        SET nameSt = %s, dob = %s, gender = %s, CCCD = %s, email = %s, address = %s, phone = %s, `class` = %s
        WHERE SId = %s
        """
        values = (name, dob, gender, cccd, email, address, phone, student_class, student_id)
        return self.execute_query(query, values)
    
    def delete_student(self, student_id):
        """Delete student by ID"""
        query = "DELETE FROM students WHERE SId = %s"
        return self.execute_query(query, (student_id,))
    
    def get_student_details(self, student_id):
        """Get detailed student information by ID including photo path"""
        query = """SELECT SId, nameSt, `class`, CCCD, gender, dob, email, phone, address, photo_path 
                   FROM students 
                   WHERE SId = %s
            """
        return self.execute_query(query, (student_id,), fetch=True)
    
   