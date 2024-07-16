from flask import Blueprint, request, jsonify
from models import Student
from database import db_session
from utils.privacy import add_noise
import numpy as np

api_bp = Blueprint('api', __name__)

@api_bp.route('/students', methods=['GET'])
def get_students():
    gpa = request.args.get('gpa', type=float)
    zip_code = request.args.get('zip_code')
    gender = request.args.get('gender')

    query = Student.query

    if gpa:
        query = query.filter(Student.gpa >= gpa)
    if zip_code:
        query = query.filter(Student.zip_code == zip_code)
    if gender:
        query = query.filter(Student.gender == gender)

    students = query.all()
    result = [student.to_dict() for student in students]
    
    # Apply differential privacy
    for student in result:
        student['gpa'] = add_noise(student['gpa'])

    return jsonify(result)

@api_bp.route('/students', methods=['POST'])
def add_student():
    data = request.json
    new_student = Student(
        name=data['name'],
        gender=data['gender'],
        gpa=data['gpa'],
        zip_code=data['zip_code']
    )
    db_session.add(new_student)
    db_session.commit()
    return jsonify(new_student.to_dict()), 201