HOW TO RUN THE CODE: (I'm using flask so I have updated the forwardPorts in devcontainer.json)
__________________________________
Run 'flask db upgrade' from within python-django/interview_calendar to create the required tables in the postgres db.

Run 'python seed_data.py' from within interview_calendar
to put some data in the tables.

Run python app.py to run the app.

Use postman to test the endpoint 'http://localhost:5000/appointments' 
with json input: 
{
  "student_id": 1,
  "instructor_id": 1,
  "start_time": "2025-06-16T10:30:00Z",
  "end_time": "2025-06-16T11:30:00Z"
}

then try with json input:
{
  "student_id": 2,
  "instructor_id": 1,
  "start_time": "2025-06-16T10:30:00Z",
  "end_time": "2025-06-16T11:30:00Z"
}

------------------------------------------------------
Alternatively, use testcases to test:

Create a test db using:
psql -U postgres -h localhost -p 5432 -c "CREATE DATABASE test_db;"

Then run pytest from within interview_calendar


____________________________________________________________________________________

ASSUMPTIONS:

All times will be sent in utc format from the front-end and will be stored in utc format in the backend.