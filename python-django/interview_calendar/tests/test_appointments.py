# tests/test_appointments.py

import json
from datetime import datetime, timedelta, timezone
#from api.models import db, Student, Instructor, InstructorAvailability
from psycopg.types.range import Range


def test_create_appointment_success(client, sample_data):
    payload = {
        "student_id": sample_data["student_id"],
        "instructor_id": sample_data["instructor_id"],
        "start_time": sample_data["start"].isoformat(),
        "end_time": sample_data["end"].isoformat()
    }

    response = client.post("/appointments", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 201
    assert "id" in response.get_json()

def test_create_appointment_outside_availability(client, sample_data):
    start = datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(days=1)
    end = start + timedelta(minutes=30)

    payload = {
        "student_id": sample_data["student_id"],
        "instructor_id": sample_data["instructor_id"],
        "start_time": start.isoformat(),
        "end_time": end.isoformat()
    }

    response = client.post("/appointments", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 400
    assert "Instructor is not available" in response.get_json()["error"]

def test_create_appointment_conflict(client, sample_data):
    # Create an initial appointment to create a conflict
    initial_payload = {
        "student_id": sample_data["student_id"],
        "instructor_id": sample_data["instructor_id"],
        "start_time": sample_data["start"].isoformat(),
        "end_time": sample_data["end"].isoformat()
    }
    client.post("/appointments", data=json.dumps(initial_payload), content_type="application/json")

    # Attempt to create a conflicting appointment
    conflict_start = sample_data["start"] + timedelta(minutes=15)
    conflict_end = conflict_start + timedelta(minutes=30)

    conflict_payload = {
        "student_id": sample_data["student_id"],
        "instructor_id": sample_data["instructor_id"],
        "start_time": conflict_start.isoformat(),
        "end_time": conflict_end.isoformat()
    }

    response = client.post("/appointments", data=json.dumps(conflict_payload), content_type="application/json")
    print(response.get_json())

    assert response.status_code == 400
    assert "Instructor is not available at this time." in response.get_json().get("error", "")

def test_create_appointment_invalid_time(client, sample_data):
    # Invalid time range where start is after end
    start = datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(minutes=30)
    end = datetime.utcnow().replace(tzinfo=timezone.utc)

    payload = {
        "student_id": sample_data["student_id"],
        "instructor_id": sample_data["instructor_id"],
        "start_time": start.isoformat(),
        "end_time": end.isoformat()
    }

    response = client.post("/appointments", data=json.dumps(payload), content_type="application/json")

    assert response.status_code == 400
    assert "Start time must be before end time." in response.get_json().get("errors", {}).get("start_time", [])

def test_create_appointment_nonexistent_instructor(client, sample_data):
    # Use a nonexistent instructor ID
    payload = {
        "student_id": sample_data["student_id"],
        "instructor_id": 9999,  # Nonexistent instructor
        "start_time": sample_data["start"].isoformat(),
        "end_time": sample_data["end"].isoformat()
    }

    response = client.post("/appointments", data=json.dumps(payload), content_type="application/json")

    assert response.status_code == 400
    assert "Instructor does not exist." in response.get_json().get("errors", {}).get("instructor_id", [])

def test_create_appointment_missing_fields(client):
    payload = {
        "student_id": 1,  # Assuming student with ID 1 exists
        "instructor_id": 1  # Assuming instructor with ID 1 exists
        # Missing start_time and end_time
    }

    response = client.post("/appointments", data=json.dumps(payload), content_type="application/json")
    print(response.get_json())
    assert response.status_code == 400
    assert "Missing data for required field." in response.get_json().get("errors", {}).get("start_time", [])
    assert "Missing data for required field." in response.get_json().get("errors", {}).get("end_time", [])

def test_create_appointment_invalid_date_format(client, sample_data):
    # Using an invalid date format
    payload = {
        "student_id": sample_data["student_id"],
        "instructor_id": sample_data["instructor_id"],
        "start_time": "invalid-date",
        "end_time": "also-invalid"
    }

    response = client.post("/appointments", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 400
    assert "Not a valid datetime." in response.get_json()["errors"]["start_time"]
    assert "Not a valid datetime." in response.get_json()["errors"]["end_time"]