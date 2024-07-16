from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import csv
import os

engine = create_engine('sqlite:///students.db')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import models
    Base.metadata.create_all(bind=engine)

    if db_session.query(models.Student).count() == 0:
        csv_path = 'modified_data.csv'
        if not os.path.exists(csv_path):
            print(f"Error: {csv_path} not found.")
            return

        try:
            with open(csv_path, 'r') as csvfile:
                csvreader = csv.DictReader(csvfile)
                for row in csvreader:
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
                    student = models.Student(**student_data)
                    db_session.add(student)

            db_session.commit()
            print("Database populated with data from CSV file.")
        except Exception as e:
            print(f"An error occurred while reading the CSV file: {str(e)}")
    else:
        print("Database already contains data. Skipping population.")