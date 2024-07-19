import psycopg2
import random
from datetime import datetime, timedelta

# Connect to the database
conn = psycopg2.connect(
    dbname="patientcare_ab_test",
    user="[name]", 
    password="[psw]",  
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Helper functions
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w

# Constants and lists
GENDERS = [("Male", 48), ("Female", 48), ("Non-binary", 2), ("Other", 2)]
ETHNICITIES = [("Caucasian", 60), ("African American", 13), ("Hispanic", 18), ("Asian", 6), ("Other", 3)]
CHRONIC_CONDITIONS = ["None", "Diabetes", "Hypertension", "Heart Disease", "COPD", "Asthma", "Arthritis", "Cancer", "Depression", "Anxiety"]
SOCIOECONOMIC_STATUS = ["Low", "Medium", "High"]
PROGRAMS = ["Diabetes Management", "Cardiac Care", "Respiratory Health", "Mental Health Support", "Weight Management"]
DEPARTMENTS = ["Emergency", "Internal Medicine", "Cardiology", "Pulmonology", "Oncology", "Orthopedics", "Neurology", "Psychiatry"]
ADMISSION_REASONS = ["Chest Pain", "Shortness of Breath", "Abdominal Pain", "Fever", "Injury", "Chronic Disease Management"]
MEDICATIONS = ["Metformin", "Lisinopril", "Atorvastatin", "Albuterol", "Sertraline", "Ibuprofen", "Omeprazole", "Gabapentin"]

# Insert data into patients table
for i in range(1, 10001):
    age = random.randint(18, 85)
    gender = weighted_choice(GENDERS)
    ethnicity = weighted_choice(ETHNICITIES)
    ses = random.choice(SOCIOECONOMIC_STATUS)
    
    # Age-appropriate chronic conditions
    if age > 50:
        condition = random.choice(CHRONIC_CONDITIONS)
    else:
        condition = random.choice(CHRONIC_CONDITIONS[:5])  # Less likely to have chronic conditions
    
    cur.execute("""
    INSERT INTO patients (PatientID, Age, Gender, Ethnicity, SocioeconomicStatus, ChronicCondition)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        f"P{i:04d}", age, gender, ethnicity, ses, condition
    ))

# Insert data into program_enrollment table
for i in range(1, 10001):
    patient_id = f"P{i:04d}"
    cur.execute("SELECT ChronicCondition FROM patients WHERE PatientID = %s", (patient_id,))
    condition = cur.fetchone()[0]
    
    enrolled = random.random() < 0.6 if condition != "None" else random.random() < 0.2
    program = None
    if enrolled:
        if condition == "Diabetes":
            program = "Diabetes Management"
        elif condition in ["Heart Disease", "Hypertension"]:
            program = "Cardiac Care"
        elif condition in ["COPD", "Asthma"]:
            program = "Respiratory Health"
        elif condition in ["Depression", "Anxiety"]:
            program = "Mental Health Support"
        else:
            program = random.choice(PROGRAMS)

    cur.execute("""
    INSERT INTO program_enrollment (PatientID, EnrolledInProgram, ProgramType, EnrollmentDate)
    VALUES (%s, %s, %s, %s)
    """, (
        patient_id,
        enrolled,
        program,
        random_date(datetime(2024, 1, 1), datetime(2024, 6, 30)) if enrolled else None
    ))

# Insert data into hospital_visits table
visit_id = 1
for i in range(1, 10001):
    patient_id = f"P{i:04d}"
    cur.execute("SELECT ChronicCondition FROM patients WHERE PatientID = %s", (patient_id,))
    condition = cur.fetchone()[0]
    
    num_visits = random.choices([0, 1, 2, 3], weights=[40, 30, 20, 10])[0]
    last_discharge = None
    
    for _ in range(num_visits):
        if last_discharge:
            admission_date = last_discharge + timedelta(days=random.randint(30, 180))
        else:
            admission_date = random_date(datetime(2023, 1, 1), datetime(2024, 6, 30))
        
        los = random.randint(1, 14)
        discharge_date = admission_date + timedelta(days=los)
        last_discharge = discharge_date
        
        department = random.choice(DEPARTMENTS)
        reason = random.choice(ADMISSION_REASONS)
        is_readmission = random.random() < 0.2 if condition != "None" else random.random() < 0.1
        
        cur.execute("""
        INSERT INTO hospital_visits (VisitID, PatientID, AdmissionDate, DischargeDate, Department, AdmissionReason, IsReadmission)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            f"V{visit_id:05d}", patient_id, admission_date, discharge_date, department, reason, is_readmission
        ))
        visit_id += 1

# Insert data into survey_responses table
for i in range(1, 6001):  # Assume 60% response rate
    patient_id = f"P{random.randint(1, 10000):04d}"
    cur.execute("SELECT COUNT(*) FROM hospital_visits WHERE PatientID = %s", (patient_id,))
    visit_count = cur.fetchone()[0]
    
    satisfaction = random.randint(1, 10)
    if visit_count > 0:
        satisfaction = max(1, min(10, satisfaction + random.randint(-2, 2)))  # Adjust based on visit history
    
    recommendation = weighted_choice([("Yes", 70), ("No", 10), ("Maybe", 20)])
    if satisfaction < 5:
        recommendation = weighted_choice([("Yes", 10), ("No", 60), ("Maybe", 30)])
    
    cur.execute("""
    INSERT INTO survey_responses (ResponseID, PatientID, SurveyDate, Satisfaction, Recommendation, CareQuality, CommunicationRating)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        f"R{i:04d}",
        patient_id,
        random_date(datetime(2024, 1, 1), datetime(2024, 6, 30)),
        satisfaction,
        recommendation,
        random.randint(1, 10),
        random.randint(1, 10)
    ))

# Insert data into medications table
for i in range(1, 10001):
    patient_id = f"P{i:04d}"
    cur.execute("SELECT ChronicCondition FROM patients WHERE PatientID = %s", (patient_id,))
    condition = cur.fetchone()[0]
    
    num_medications = random.choices([0, 1, 2, 3], weights=[20, 40, 30, 10])[0]
    if condition != "None":
        num_medications = max(num_medications, 1)
    
    for _ in range(num_medications):
        medication = random.choice(MEDICATIONS)
        start_date = random_date(datetime(2024, 1, 1), datetime(2024, 6, 30))
        
        cur.execute("""
        INSERT INTO medications (PatientID, Medication, StartDate, EndDate)
        VALUES (%s, %s, %s, %s)
        """, (
            patient_id,
            medication,
            start_date,
            start_date + timedelta(days=random.randint(30, 365)) if random.random() < 0.3 else None
        ))

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()
print("Data has been inserted into the database.")
