from marshmallow import Schema, fields, validates_schema, ValidationError
from datetime import datetime, timezone
from api.models import Appointment, Student, Instructor
from extensions import db

class AppointmentSchema(Schema):
    class Meta:
        model = Appointment
        load_instance = True
        include_fk = True

    student_id = fields.Int(required=True)
    instructor_id = fields.Int(required=True)
    start_time = fields.DateTime(required=True) # accepts ISO8601 strings, converts to datetime
    end_time = fields.DateTime(required=True)

    @validates_schema
    def validate_entities_and_time(self, data, **kwargs):
        #Ensure both are in UTC
        if data["start_time"].tzinfo != timezone.utc or data["end_time"].tzinfo != timezone.utc:
            print('hi')
            raise ValidationError("Start and end times must be in UTC.", field_name="start_time")

        if data["start_time"] >= data["end_time"]:
            print('hi2')
            raise ValidationError("Start time must be before end time.", field_name="start_time")

        # Check if student exists
        if not db.session.get(Student, data["student_id"]):
            print('hi3')
            raise ValidationError("Student does not exist.", field_name="student_id")

        # Check if instructor exists
        if not db.session.get(Instructor, data["instructor_id"]):
            print('hi4')
            raise ValidationError("Instructor does not exist.", field_name="instructor_id")
                
class AppointmentResponseSchema(Schema):
    id = fields.Int()
    student_id = fields.Int()
    instructor_id = fields.Int()
    start_time = fields.DateTime()
    end_time = fields.DateTime()