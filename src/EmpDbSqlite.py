'''
This is the interface to an SQLite Database
'''

import json
import sqlite3
import csv

class EmpDbSqlite:
    def __init__(self, dbName='Students.db'):
        super().__init__()
        self.dbName = dbName
        self.csvFile = self.dbName.replace('.db', '.csv')
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Students (
                id TEXT PRIMARY KEY,
                name TEXT,
                program TEXT,
                gender TEXT,
                status TEXT)''')
        self.conn.commit()
        self.conn.close()

    def connect_cursor(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()        

    def commit_close(self):
        self.conn.commit()
        self.conn.close()        

    def create_table(self):
        self.connect_cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Students (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    program TEXT,
                    gender TEXT,
                    status TEXT)''')
        self.commit_close()

    def fetch_students(self):
        self.connect_cursor()
        self.cursor.execute('SELECT * FROM Students')
        students =self.cursor.fetchall()
        self.conn.close()
        return students

    def insert_student(self, id, name, program, gender, status):
        self.connect_cursor()
        self.cursor.execute('INSERT INTO Students (id, name, program, gender, status) VALUES (?, ?, ?, ?, ?)',
                    (id, name, program, gender, status))
        self.commit_close()

    def delete_student(self, id):
        self.connect_cursor()
        self.cursor.execute('DELETE FROM Students WHERE id = ?', (id,))
        self.commit_close()

    def update_student(self, name, program, gender, status, id):
        self.connect_cursor()
        self.cursor.execute('''UPDATE Students SET name=?, program=?, gender=?, status=? WHERE id=?''', (self, name, program, gender, status, id))
        self.commit_close()
        
    def id_exists(self, id):
        self.connect_cursor()
        self.cursor.execute('SELECT COUNT(*) FROM Students WHERE id = ?', (id,))
        result =self.cursor.fetchone()
        self.conn.close()
        return result[0] > 0

    def export_csv(self):
        with open(self.csvFile, "w") as filehandle:
            dbEntries = self.fetch_students()
            for entry in dbEntries:
                print(entry)
                filehandle.write(f"{entry[0]},{entry[1]},{entry[2]},{entry[3]},{entry[4]}\n")

    def export_json(self, dbName, outputFile='students.json'):
        self.connect_cursor(dbName)
        self.cursor.execute('SELECT * FROM Students')
        students = self.cursor.fetchall()
        self.conn.close()

        # Convert tuples to dictionaries
        records = [dict(student) for student in students]

        # Write to JSON file
        with open(outputFile, 'w') as f:
            json.dump(records, f, indent=4)
        
    def import_csv(self, file_path):
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip the header row
            for row in reader:
                self.insert_student(row[0], row[1], row[2], row[3], row[4])

def test_EmpDb():
    iEmpDb = EmpDbSqlite(dbName='EmpDbSql.db')

    for entry in range(30):
        iEmpDb.insert_student(str(entry), f'Name{entry} Surname{entry}', f'BS CoE {entry}', 'Male', 'Enrolled')
        assert iEmpDb.id_exists(entry)

    all_entries = iEmpDb.fetch_students()
    assert len(all_entries) == 30

    for entry in range(10, 20):
        iEmpDb.update_student(f'Name{entry} Surname{entry}', f'BS CoE {entry}', 'Female', 'Not Enrolled', str(entry))
        assert iEmpDb.id_exists(entry)

    all_entries = iEmpDb.fetch_students()
    assert len(all_entries) == 30

    for entry in range(10):
        iEmpDb.delete_student(entry)
        assert not iEmpDb.id_exists(entry)

    all_entries = iEmpDb.fetch_students()
    assert len(all_entries) == 20