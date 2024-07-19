from database_utils import execute_query
import logging

def load_data():
    query = """
    SELECT 
        p.PatientID,
        p.Age,
        p.Gender,
        p.ChronicCondition,
        pe.EnrolledInProgram,
        CASE WHEN COUNT(hv.VisitID) > 1 THEN TRUE ELSE FALSE END AS IsReadmission,
        AVG(sr.Satisfaction) AS Satisfaction,
        MIN(CASE WHEN hv.IsReadmission THEN 
            EXTRACT(DAY FROM hv.AdmissionDate - LAG(hv.DischargeDate) OVER (PARTITION BY p.PatientID ORDER BY hv.AdmissionDate))
        END) AS DaysToReadmission
    FROM 
        patients p
    LEFT JOIN 
        program_enrollment pe ON p.PatientID = pe.PatientID
    LEFT JOIN 
        hospital_visits hv ON p.PatientID = hv.PatientID
    LEFT JOIN
        survey_responses sr ON p.PatientID = sr.PatientID
    GROUP BY 
        p.PatientID, pe.EnrolledInProgram
    """
    try:
        df = execute_query(query)
        if df.empty:
            logging.warning("The query returned an empty dataset.")
        return df
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        raise