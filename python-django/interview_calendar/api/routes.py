from flask import Flask, request, jsonify
from schemas.appointment_schema import AppointmentSchema, AppointmentResponseSchema
from marshmallow import ValidationError
from api.services import appointment as appointment_service
from sqlalchemy.exc import IntegrityError
from psycopg.errors import ExclusionViolation, ForeignKeyViolation

def register_routes(app):
    @app.route("/api/hello")
    def hello():
        return {"message": "Hello from Flask!"}

    @app.route("/test", methods=["GET", "POST"])
    def test():
        print("TEST endpoint hit")
        return {"status": "ok"}

    @app.route("/appointments", methods=["POST"])
    def create_appointment():
        try:
            # Validate and deserialize request data
            validated_data = AppointmentSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

        student_id = validated_data["student_id"]
        instructor_id = validated_data["instructor_id"]
        start_time = validated_data["start_time"]
        end_time = validated_data["end_time"]

        try:
            if not appointment_service.is_instructor_available(instructor_id, student_id, start_time, end_time):
                return jsonify({"error": "Instructor is not available at this time."}), 400

            appointment = appointment_service.create_appointment(student_id, instructor_id, start_time, end_time)
            return jsonify({
                "message": "Appointment scheduled successfully",
                "appointment": AppointmentResponseSchema().dump(appointment)
            }), 201
        except IntegrityError as e:
            orig = getattr(e, "orig", None)

            if isinstance(orig, ExclusionViolation):
                return jsonify({
                    "error": "The selected time slot is already booked. Please choose a different time."
                }), 409

            elif isinstance(orig, ForeignKeyViolation):
                return jsonify({
                    "error": "The student or instructor you selected does not exist. Please check your selection."
                }), 400

            return jsonify({
                "error": "There was a problem saving your appointment. Please try again."
            }), 400