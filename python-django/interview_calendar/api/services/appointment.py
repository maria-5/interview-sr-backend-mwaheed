from extensions import db
from api.models import Appointment, InstructorAvailability
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import TSTZRANGE
from psycopg.types.range import Range

def create_appointment(student_id, instructor_id, start_time, end_time):
    appointment_time = Range(start_time, end_time, bounds='[)')

    appointment = Appointment(
        student_id = student_id,
        instructor_id = instructor_id,
        appointment_time = appointment_time,
    )
    db.session.add(appointment)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise e  # Re-raise so the route can handle it

    return appointment


def is_instructor_available(instructor_id, student_id, start_time, end_time):
    requested_range = Range(start_time, end_time, bounds='[]')

    # Check if requested time fits inside any available time
    availability = InstructorAvailability.query.filter(
        InstructorAvailability.instructor_id == instructor_id,
        InstructorAvailability.available_time.op("@>")(requested_range)  # contains
    ).first()

    if not availability:
        return False

    # Check for conflicting instructor appointment
    instructor_conflict = Appointment.query.filter(
        Appointment.instructor_id == instructor_id,
        Appointment.appointment_time.op("&&")(requested_range)  # overlaps
    ).first()

    # Check for conflicting student appointment
    student_conflict = Appointment.query.filter(
        Appointment.student_id == student_id,
        Appointment.appointment_time.op("&&")(requested_range)
    ).first()

    return not (instructor_conflict or student_conflict)