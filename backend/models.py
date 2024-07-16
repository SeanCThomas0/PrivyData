from sqlalchemy import Column, Integer, String, Float
from database import Base

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    gender = Column(String(10))
    gpa = Column(Float)
    zip_code = Column(String(10))

    def __init__(self, name, gender, gpa, zip_code):
        self.name = name
        self.gender = gender
        self.gpa = gpa
        self.zip_code = zip_code

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'gpa': self.gpa,
            'zip_code': self.zip_code
        }