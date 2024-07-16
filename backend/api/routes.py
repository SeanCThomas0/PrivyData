from flask import Blueprint, request, jsonify
from models import Student
from database import db_session
from utils.privacy import add_noise
import numpy as np

api_bp = Blueprint('api', __name__)

@api_bp.route('/students', methods=['GET'])
def get_students():
    query = Student.query

    for column in Student.__table__.columns:
        value = request.args.get(column.name)
        if value:
            if column.type.python_type in (int, float):
                query = query.filter(getattr(Student, column.name) >= float(value))
            else:
                query = query.filter(getattr(Student, column.name) == value)

    students = query.all()
    result = [student.to_dict() for student in students]
    
    # Apply differential privacy to sensitive fields
    sensitive_fields = ['GPA', 'StudyTimeWeekly', 'Absences']
    for student in result:
        for field in sensitive_fields:
            student[field] = add_noise(student[field])

    return jsonify(result)

@api_bp.route('/students', methods=['POST'])
def add_student():
    data = request.json
    new_student = Student(**data)
    db_session.add(new_student)
    db_session.commit()
    return jsonify(new_student.to_dict()), 201