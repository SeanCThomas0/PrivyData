from flask import Blueprint, request, jsonify
from models import Student
from database import db_session

api_bp = Blueprint('api', __name__)

@api_bp.route('/students', methods=['GET'])
def get_students():
    query = Student.query

    # Define mappings for string comparisons
    string_comparisons = {
        'eq': '__eq__',
        'contains': 'contains',
        'startswith': 'startswith',
        'endswith': 'endswith'
    }

    for column in Student.__table__.columns:
        value = request.args.get(column.name)
        comparison = request.args.get(f'{column.name}_comparison', 'eq')
        
        if value:
            if column.type.python_type in (int, float):
                query = query.filter(getattr(Student, column.name) >= float(value))
            elif column.type.python_type == str:
                if comparison in string_comparisons:
                    filter_func = getattr(getattr(Student, column.name), string_comparisons[comparison])
                    query = query.filter(filter_func(value))
                else:
                    query = query.filter(getattr(Student, column.name) == value)

    students = query.all()
    result = [student.to_dict() for student in students]
    
    return jsonify(result)

@api_bp.route('/students', methods=['POST'])
def add_student():
    data = request.json
    new_student = Student(**data)
    db_session.add(new_student)
    db_session.commit()
    return jsonify(new_student.to_dict()), 201