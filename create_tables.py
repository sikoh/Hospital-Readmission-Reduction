import psycopg2
from psycopg2 import sql
from database_utils import get_db_connection

def create_tables():
    conn = get_db_connection()

    with conn.cursor() as cur:
        # Create Patients table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            PatientID VARCHAR(50) PRIMARY KEY,
            Age INTEGER,
            Gender VARCHAR(50),
            Ethnicity VARCHAR(100),
            SocioeconomicStatus VARCHAR(100),
            ChronicCondition VARCHAR(150)
        );
        """)
        print("Patients table created successfully")

        # Create Program Enrollment table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS program_enrollment (
            EnrollmentID SERIAL PRIMARY KEY,
            PatientID VARCHAR(50) REFERENCES patients(PatientID),
            EnrolledInProgram BOOLEAN,
            ProgramType VARCHAR(150),
            EnrollmentDate DATE
        );
        """)
        print("Program Enrollment table created successfully")

        # Create Hospital Visits table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS hospital_visits (
            VisitID VARCHAR(6) PRIMARY KEY,
            PatientID VARCHAR(50) REFERENCES patients(PatientID),
            AdmissionDate DATE,
            DischargeDate DATE,
            Department VARCHAR(80),
            AdmissionReason VARCHAR(150),
            IsReadmission BOOLEAN
        );
        """)
        print("Hospital Visits table created successfully")

        # Create Survey Responses table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS survey_responses (
            ResponseID VARCHAR(50) PRIMARY KEY,
            PatientID VARCHAR(50) REFERENCES patients(PatientID),
            SurveyDate DATE,
            Satisfaction INTEGER,
            Recommendation VARCHAR(150),
            CareQuality INTEGER,
            CommunicationRating INTEGER
        );
        """)
        print("Survey Responses table created successfully")

        # Create Medications table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS medications (
            MedicationID SERIAL PRIMARY KEY,
            PatientID VARCHAR(50) REFERENCES patients(PatientID),
            Medication VARCHAR(150),
            StartDate DATE,
            EndDate DATE
        );
        """)
        print("Medications table created successfully")

    conn.commit()
    conn.close()
    print("All tables created successfully")

if __name__ == "__main__":
    create_tables()