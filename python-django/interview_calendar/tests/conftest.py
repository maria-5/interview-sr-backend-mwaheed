import os
import sys
import pytest
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import text
from datetime import datetime, timedelta, timezone
from psycopg.types.range import Range

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_migrate import upgrade
from app import create_app, db
from config import TestConfig

@pytest.fixture(scope='session')
def app():
    app = create_app(config_class=TestConfig)
    with app.app_context():
        yield app

@pytest.fixture(scope='session')
def database(app):
    with app.app_context():
        # Drop all tables before migration
        db.session.execute(text('DROP SCHEMA public CASCADE;'))
        db.session.execute(text('CREATE SCHEMA public;'))
        db.session.commit()

        upgrade()  # Apply migrations to the test DB
        yield db
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def client(app, database):
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='function', autouse=True)
def session():
    # Start a connection and transaction
    connection = db.engine.connect()
    transaction = connection.begin()

    # Create a new scoped session bound to this connection
    session_factory = sessionmaker(bind=connection)
    scoped_sess = scoped_session(session_factory)

    # Override the Flask-SQLAlchemy session with this scoped session
    db.session = scoped_sess

    yield scoped_sess  # provide the session to the test

    # Rollback everything after test finishes
    transaction.rollback()
    connection.close()
    scoped_sess.remove()

@pytest.fixture(scope="function")
def sample_data(app):
    from api.models import db, Student, Instructor, InstructorAvailability

    student = Student(name="Test Student", email="student@example.com")
    instructor = Instructor(name="Test Instructor", email="instructor@example.com")
    db.session.add_all([student, instructor])
    db.session.commit()

    now = datetime.now(timezone.utc)
    availability = InstructorAvailability(
        instructor_id=instructor.id,
        available_time=Range(now, now + timedelta(hours=2), '[]')
    )
    db.session.add(availability)
    db.session.commit()

    return {
        "student_id": student.id,
        "instructor_id": instructor.id,
        "start": now,
        "end": now + timedelta(minutes=30)
    }
