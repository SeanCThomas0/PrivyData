import csv
from models import Student
from database import Base, engine, db_session

def init_db():
    Base.metadata.create_all(bind=engine)

    # Check if the database is already populated
    if db_session.query(Student).count() == 0:
        # Read data from CSV file
        with open(r'C:\student_api_project\modified_data.csv', 'r') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                # Convert string values to appropriate types
                student_data = {
                    'StudentID': int(row['StudentID']),
                    'Age': int(row['Age']),
                    'Gender': int(row['Gender']),
                    'Ethnicity': int(row['Ethnicity']),
                    'ParentalEducation': int(row['ParentalEducation']),
                    'StudyTimeWeekly': float(row['StudyTimeWeekly']),
                    'Absences': int(row['Absences']),
                    'Tutoring': int(row['Tutoring']),
                    'ParentalSupport': int(row['ParentalSupport']),
                    'Extracurricular': int(row['Extracurricular']),
                    'Sports': int(row['Sports']),
                    'Music': int(row['Music']),
                    'Volunteering': int(row['Volunteering']),
                    'GPA': float(row['GPA']),
                    'GradeClass': float(row['GradeClass']),
                    'Name': row['Name'],
                    'Zipcode': row['Zipcode']
                }
                student = Student(**student_data)
                db_session.add(student)

        db_session.commit()
        print("Database populated with data from CSV file.")
    else:
        print("Database already contains data. Skipping population.")