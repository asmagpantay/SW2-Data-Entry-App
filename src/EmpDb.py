from EmpDbEntry import EmpDbEntry

import json
import os
import csv

class EmpDb:
    """
    - simple database to store EmpDbEntry objects
    """    

    def __init__(self, init=False, dbName='EmpDb.csv'):
        """
        - initialize database variables here
        - mandatory :
            - any type can be used to store database entries for EmpDbEntry objects
            - e.g. list of class, list of dictionary, list of tuples, dictionary of tuples etc.
        """
        # CSV filename         
        self.dbName = dbName
        # initialize container of database entries 
        self.dbEntries = []

    def fetch_students(self):
        """
        - returns a list of tuples containing Student entry fields
        - example
          [('123', 'Brian Baker', 'SW-Engineer', 'Male', 'On-Site'),
           ('124', 'Eileen Dover', 'SW-Engineer', 'Male', 'On-Site'),
           ('125', 'Ann Chovey', 'SW-Engineer', 'Male', 'On-Site')]
        """
        studentList = [(entry.id, entry.name, entry.program, entry.gender, entry.status) for entry in self.dbEntries]
        return studentList

    def insert_student(self, id, name, program, gender, status):
        """
        - inserts an entry in the database
        - no return value
        """
        newEntry = EmpDbEntry(id=id, name=name, program=program, gender=gender, status=status)
        self.dbEntries.append(newEntry)

    def delete_student(self, id):
        """
        - deletes the corresponding entry in the database as specified by 'id'
        - no return value
        """
        self.dbEntries = [entry for entry in self.dbEntries if entry.id != id]

    def update_student(self, new_id, new_name, new_program, new_gender, new_status, id):
        """
        - updates the corresponding entry in the database as specified by 'id'
        - no return value
        """
        for entry in self.dbEntries:
            if entry.id == id:
                entry.id = new_id
                entry.name = new_name
                entry.program = new_program
                entry.gender = new_gender
                entry.status = new_status
                break

    def export_csv(self):
        """
        - exports database entries as a CSV file
        - CSV : Comma Separated Values
        - no return value
        - example
        12,Eileen Dover,SW-Engineer,Male,On-Site
        13,Ann Chovey,HW-Engineer,Female,On-Site
        14,Chris P. Bacon,SW-Engineer,Male,On-Leave
        15,Russell Sprout,SW-Engineer,Male,Remote
        16,Oscar Lott,Project-Manager,Male,On-Site        
        """
        import csv
        with open(self.dbName, 'w', newline='') as csvfile:
            fieldnames = ['id', 'name', 'program', 'gender', 'status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entry in self.dbEntries:
                writer.writerow({'id': entry.id, 'name': entry.name, 'program': entry.program, 'gender': entry.gender, 'status': entry.status})

    def export_json(self, outputFile='students.json'):
        """
        - exports database entries as a JSON file
        - no return value
        - example
        [
            {"id": "123", "name": "Brian Baker", "program": "SW-Engineer", "gender": "Male", "status": "On-Site"},
            {"id": "124", "name": "Eileen Dover", "program": "SW-Engineer", "gender": "Male", "status": "On-Site"},
            {"id": "125", "name": "Ann Chovey", "program": "SW-Engineer", "gender": "Male", "status": "On-Site"}
        ]
        """
        records = [{'id': entry.id, 'name': entry.name, 'program': entry.program, 'gender': entry.gender, 'status': entry.status} for entry in self.dbEntries]

        # Write to JSON file
        with open(outputFile, 'w') as f:
            json.dump(records, f, indent=4)


    def id_exists(self, id):
        """
        - returns True if an entry exists for the specified 'id'
        - else returns False
        """
        return any(entry.id == id for entry in self.dbEntries)
    
    def import_csv(self, filePath):
        """
            - imports CSV data into the EmpDb object
            - filePath : string, path to CSV file
            - no return value
        """
        if not os.path.exists(filePath) or not os.path.isfile(filePath) or not os.access(filePath, os.R_OK):
            raise Exception("CSV file not found or not readable")

        with open(filePath, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Skip header row
            for row in csvreader:
                self.insert_student(row[0], row[1], row[2], row[3], row[4])