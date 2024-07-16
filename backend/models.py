from sqlalchemy import Column, Integer, Float, String
from database import Base

class Student(Base):
    __tablename__ = 'students'
    StudentID = Column(Integer, primary_key=True)
    Age = Column(Integer)
    Gender = Column(Integer)
    Ethnicity = Column(Integer)
    ParentalEducation = Column(Integer)
    StudyTimeWeekly = Column(Float)
    Absences = Column(Integer)
    Tutoring = Column(Integer)
    ParentalSupport = Column(Integer)
    Extracurricular = Column(Integer)
    Sports = Column(Integer)
    Music = Column(Integer)
    Volunteering = Column(Integer)
    GPA = Column(Float)
    GradeClass = Column(Float)
    Name = Column(String(100))
    Zipcode = Column(String(10))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}