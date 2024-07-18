import psycopg2
import random
from datetime import datetime, timedelta

# Connect to the database
conn = psycopg2.connect(
    dbname="patientcare_ab_test",
    user="[enter_name]",
    password="[enter_pw]",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Helper function to generate random dates
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# Insert data into patients table
for i in range(1, 10001):
    cur.execute("""
    INSERT INTO patients (PatientID, Age, Gender, ChronicCondition)
    VALUES (%s, %s, %s, %s)
    """, (
        f"P{i:02d}",
        random.randint(18, 85),
        random.choice(["Male", "Female"]),
        random.choice(["None", "Diabetes", "Hypertension", "Heart Disease", "COPD"])
    ))

# Insert data into program_enrollment table
for i in range(1, 10001):
    enrolled = random.choice([True, False])
    cur.execute("""
    INSERT INTO program_enrollment (PatientID, EnrolledInProgram, EnrollmentDate)
    VALUES (%s, %s, %s)
    """, (
        f"P{i:02d}",
        enrolled,
        random_date(datetime(2023, 1, 1), datetime(2023, 12, 31)) if enrolled else None
    ))

# Insert data into hospital_visits table
visit_id = 1
for i in range(1, 10001):
    num_visits = random.randint(0, 3)
    for _ in range(num_visits):
        admission_date = random_date(datetime(2023, 1, 1), datetime(2024, 3, 31))
        discharge_date = admission_date + timedelta(days=random.randint(1, 14))
        cur.execute("""
        INSERT INTO hospital_visits (VisitID, PatientID, AdmissionDate, DischargeDate, IsReadmission)
        VALUES (%s, %s, %s, %s, %s)
        """, (
            f"V{visit_id:03d}",
            f"P{i:02d}",
            admission_date,
            discharge_date,
            random.choice([True, False])
        ))
        visit_id += 1

# Insert data into survey_responses table
for i in range(1, 5001):  # Assume 50% response rate
    cur.execute("""
    INSERT INTO survey_responses (ResponseID, PatientID, SurveyDate, Satisfaction, Recommendation)
    VALUES (%s, %s, %s, %s, %s)
    """, (
        f"R{i:04d}",
        f"P{random.randint(1, 10000):02d}",
        random_date(datetime(2023, 1, 1), datetime(2024, 3, 31)),
        random.randint(1, 10),
        random.choice(["Yes", "No", "Maybe"])
    ))

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()

print("Data has been inserted into the database.")