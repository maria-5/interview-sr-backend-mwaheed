from extensions import db
from sqlalchemy.dialects.postgresql import TSTZRANGE
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import ExcludeConstraint
from app import db

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    # Add more fields as needed

class Instructor(db.Model):
    __tablename__ = 'instructors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    # Add more fields as needed

class InstructorAvailability(db.Model):
    __tablename__ = 'instructor_availability'
    id = db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id', ondelete='CASCADE'), nullable=False)
    available_time = db.Column(TSTZRANGE, nullable=False)

    instructor = db.relationship('Instructor', backref=db.backref('availabilities', lazy='dynamic'))

    __table_args__ = (
        # Prevent overlapping availability intervals per instructor
        ExcludeConstraint(
            ('instructor_id', '='), 
            ('available_time', '&&'), 
            name='exclude_instructor_availability_overlaps'
        ),
    )

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id', ondelete='CASCADE'), nullable=False)
    appointment_time = db.Column(TSTZRANGE, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='booked') 

    student = db.relationship('Student', backref=db.backref('appointments', lazy='dynamic'))
    instructor = db.relationship('Instructor', backref=db.backref('appointments', lazy='dynamic'))

    __table_args__ = (
        # Prevent overlapping appointments for the same student
        ExcludeConstraint(
            ('student_id', '='), 
            ('appointment_time', '&&'), 
            name='exclude_student_appointments_overlap'
        ),
        # Prevent overlapping appointments for the same instructor
        ExcludeConstraint(
            ('instructor_id', '='), 
            ('appointment_time', '&&'), 
            name='exclude_instructor_appointments_overlap'
        ),
        # ensure appointment_time lower bound < upper bound
        CheckConstraint("lower(appointment_time) < upper(appointment_time)", name='check_appointment_time_valid_range'),
    )
