from flask import Blueprint, request, jsonify
from models import Student
from database import db_session
import numpy as np
import pandas as pd
import opendp.prelude as dp

api_bp = Blueprint('api', __name__)

# Enable necessary features in OpenDP
dp.enable_features('contrib')

col_names = ["StudentID", "Age", "Gender", "Ethnicity", "ParentalEducation",
             "StudyTimeWeekly", "Absences", "Tutoring", "ParentalSupport", "Extracurricular", 
             "Sports", "Music", "Volunteering", "GPA", "GradeClass", "Name", "Zipcode"]

# Define bounds for clamping
age_bounds = (14.0, 18.0)  # explicitly casting to float
gpa_bounds = (0.0, 4.0)    # explicitly casting to float
absences_bounds = (0.0, 35.0)  # explicitly casting to float

# Define privacy parameters
privacy_unit = dp.unit_of(contributions=1)
privacy_loss = dp.loss_of(epsilon=0.25)

# Read the local CSV file without getting the column names
data = pd.read_csv('modified_data.csv', header=None)

# Convert the DataFrame to a CSV string without the header
data_csv = data.to_csv(index=False, header=False)

# Create the DP context
context = dp.Context.compositor(
    data=data_csv,
    privacy_unit=privacy_unit,
    privacy_loss=privacy_loss,
    split_evenly_over=6
)

# Define function to create mean query with DP
def create_mean_query(context, col_names, column_name, min_value, max_value, dp_count):
    return (
        context.query()
        .split_dataframe(",", col_names=col_names)
        .select_column(column_name, str)
        .cast_default(float)
        .clamp((float(min_value), float(max_value)))  # ensure bounds are float
        .resize(size=dp_count, constant=min_value)
        .mean()
        .laplace()
    )

# Define function to create count query with DP
def create_count_query(context, col_names, column_name):
    return (
        context.query()
        .split_dataframe(",", col_names=col_names)
        .select_column(column_name, str)
        .count()
        .laplace()
    )



# Other routes can remain as they are
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

    return jsonify(result)

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


@api_bp.route('/students/stats', methods=['GET'])
def get_student_dp_stats():
    students = Student.query.all()
    dp_count = len(students)
    print('dp')

    # DP queries
    age_mean_query = create_mean_query(context, col_names, "Age", age_bounds[0], age_bounds[1], dp_count)
    gpa_mean_query = create_mean_query(context, col_names, "GPA", gpa_bounds[0], gpa_bounds[1], dp_count)
    absences_mean_query = create_mean_query(context, col_names, "Absences", absences_bounds[0], absences_bounds[1], dp_count)
    print('dp1')

    age_mean = age_mean_query.release()
    gpa_mean = gpa_mean_query.release()
    absences_mean = absences_mean_query.release()
    print('dp2')

    age_count_query = create_count_query(context, col_names, "Age")
    gpa_count_query = create_count_query(context, col_names, "GPA")
    absences_count_query = create_count_query(context, col_names, "Absences")
    print('dp3')
    age_count = age_count_query.release()
    gpa_count = gpa_count_query.release()
    absences_count = absences_count_query.release()

    stats = {
        'age_mean': age_mean,
        'gpa_mean': gpa_mean,
        'absences_mean': absences_mean,
        'age_count': age_count,
        'gpa_count': gpa_count,
        'absences_count': absences_count,
    }

    return jsonify(stats)

@api_bp.route('/students/stat', methods=['GET'])
def get_student_normal_stat():
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