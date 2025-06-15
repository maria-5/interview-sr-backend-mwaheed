from datetime import datetime, timedelta, timezone
from psycopg.types.range import Range
from app import create_app
from api.models import Student, Instructor, InstructorAvailability
from extensions import db

app = create_app()

with app.app_context():
    student = Student(name="Test Student", email="student1@example.com")
    student1 = Student(name="Adam Smith", email="adam.smith@example.com")
    instructor = Instructor(name="Test Instructor", email="instructor@example.com")
    db.session.add_all([student, student1, instructor])
    db.session.commit()

    # Hardcoded datetime: June 16, 2025, 10:00 AM UTC
    start_time = datetime(2025, 6, 16, 10, 0, tzinfo=timezone.utc)
    end_time = start_time + timedelta(hours=2)    
    availability = InstructorAvailability(
        instructor_id=instructor.id,
        available_time=Range(start_time, end_time, '[]')  # inclusive bounds
    )
    db.session.add(availability)
    db.session.commit()

    print("Seed data inserted successfully.")
