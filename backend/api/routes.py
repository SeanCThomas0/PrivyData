from flask import Blueprint, request, jsonify
from models import Student
from database import db_session
from utils.privacy import add_noise
import numpy as np


api_bp = Blueprint('api', __name__)

import opendp.prelude as dp
dp.enable_features('contrib')
laplace_mechanism = dp.space_of(float) >> dp.m.then_laplace(scale=1.)
dp_value = laplace_mechanism(123.0)
print(dp_value)



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
    sensitive_fields = ['GPA']
    #    for student in result:
    #   for field in sensitive_fields:
    #       student['GPA'] = add_noise(student['GPA'])
    #
    #
    return jsonify(result)

@api_bp.route('/students/stats', methods=['GET'])
def get_student_stats():
    students = Student.query.all()
    gpas = [student.GPA for student in students]
    ages = [student.Age for student in students]

    stats = {
        'gpa_mean': np.mean(gpas),
        'gpa_median': np.median(gpas),
        'gpa_std': np.std(gpas),
        'age_mean': np.mean(ages),
        'age_median': np.median(ages),
        'age_std': np.std(ages),
        'total_students': len(students)
    }

    return jsonify(stats)

@api_bp.route('/students/performance', methods=['GET'])
def get_performance_breakdown():
    students = Student.query.all()
    performance = {
        'high_performers': len([s for s in students if s.GPA >= 3.5]),
        'medium_performers': len([s for s in students if 2.5 <= s.GPA < 3.5]),
        'low_performers': len([s for s in students if s.GPA < 2.5])
    }

    return jsonify(performance)

@api_bp.route('/students', methods=['POST'])
def add_student():
    data = request.json
    new_student = Student(**data)
    db_session.add(new_student)
    db_session.commit()
    return jsonify(new_student.to_dict()), 201


@api_bp.route('/students/filtered_stats', methods=['GET'])
def get_filtered_stats():
    query = Student.query

    # Apply filters based on query parameters
    for column in Student.__table__.columns:
        value = request.args.get(column.name)
        if value:
            if column.name in ['Ethnicity', 'Gender', 'ParentalEducation']:
                query = query.filter(getattr(Student, column.name) == value)
            elif column.type.python_type in (int, float):
                try:
                    query = query.filter(getattr(Student, column.name) >= float(value))
                except ValueError:
                    # If conversion to float fails, ignore this filter.
                    pass

    stat_type = request.args.get('statType')
    
    students = query.all()
    
    if stat_type == 'GPA':
        values = [student.GPA for student in students]
    elif stat_type == 'Age':
        values = [student.Age for student in students]
    elif stat_type == 'Absences':
        values = [student.Absences for student in students]
    else:
        return jsonify({"error": "Invalid stat type"}), 400

    if not values:
        return jsonify({
            "mean": None,
            "median": None,
            "min": None,
            "max": None,
            "std": None,
            "count": 0
        })

    stats = {
        'mean': float(np.mean(values)),
        'median': float(np.median(values)),
        'min': float(np.min(values)),
        'max': float(np.max(values)),
        'std': float(np.std(values)),
        'count': len(values)
    }

    return jsonify(stats)