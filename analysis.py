import pandas as pd
import numpy as np
from scipy import stats
import logging

def analyze_results(df):
    results = {}
    try:
        control_group = df[df['EnrolledInProgram'] == False]
        treatment_group = df[df['EnrolledInProgram'] == True]

        if control_group.empty or treatment_group.empty:
            raise ValueError("One or both groups are empty. Cannot perform analysis.")

        control_readmission_rate = control_group['IsReadmission'].mean()
        treatment_readmission_rate = treatment_group['IsReadmission'].mean()

        results['control_readmission_rate'] = control_readmission_rate
        results['treatment_readmission_rate'] = treatment_readmission_rate

        logging.info(f"Control group readmission rate: {control_readmission_rate:.2%}")
        logging.info(f"Treatment group readmission rate: {treatment_readmission_rate:.2%}")

        contingency_table = pd.crosstab(df['EnrolledInProgram'], df['IsReadmission'])
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)

        results['chi2'] = chi2
        results['p_value'] = p_value

        logging.info(f"Chi-square statistic: {chi2:.4f}")
        logging.info(f"p-value: {p_value:.4f}")

        relative_risk_reduction = (control_readmission_rate - treatment_readmission_rate) / control_readmission_rate
        results['relative_risk_reduction'] = relative_risk_reduction
        logging.info(f"Relative Risk Reduction: {relative_risk_reduction:.2%}")

        results['readmission_rates'] = analyze_readmission_rates(df)
        results['satisfaction_scores'] = analyze_patient_satisfaction(df)
        results['days_to_readmission'] = analyze_days_to_readmission(df)
        results['subgroup_results'] = perform_subgroup_analysis(df)

        return results
    except Exception as e:
        logging.error(f"Error in analyze_results: {e}")
        raise

def analyze_readmission_rates(df):
    try:
        readmission_rates = df.groupby('EnrolledInProgram')['IsReadmission'].mean()
        logging.info("\nReadmission Rates:")
        logging.info(readmission_rates)
        
        enrolled = df[df['EnrolledInProgram']]['IsReadmission'].astype(float)
        not_enrolled = df[~df['EnrolledInProgram']]['IsReadmission'].astype(float)
        
        if len(enrolled) > 1 and len(not_enrolled) > 1:
            t_stat, p_value = stats.ttest_ind(enrolled, not_enrolled)
            logging.info(f"T-statistic: {t_stat}, P-value: {p_value}")
        else:
            logging.warning("Not enough data to perform t-test")
        
        return readmission_rates.to_dict()
    except Exception as e:
        logging.error(f"Error in analyze_readmission_rates: {e}")
        raise

def analyze_patient_satisfaction(df):
    try:
        satisfaction = df.groupby('EnrolledInProgram')['Satisfaction'].mean()
        logging.info("\nAverage Satisfaction Scores:")
        logging.info(satisfaction)
        
        enrolled = df[df['EnrolledInProgram']]['Satisfaction']
        not_enrolled = df[~df['EnrolledInProgram']]['Satisfaction']
        t_stat, p_value = stats.ttest_ind(enrolled, not_enrolled)
        logging.info(f"T-statistic: {t_stat}, P-value: {p_value}")
        
        return satisfaction.to_dict()
    except Exception as e:
        logging.error(f"Error in analyze_patient_satisfaction: {e}")
        raise

def analyze_days_to_readmission(df):
    try:
        days_to_readmission = df.groupby('EnrolledInProgram')['DaysToReadmission'].mean()
        logging.info("\nAverage Days to Readmission:")
        logging.info(days_to_readmission)
        
        enrolled = df[df['EnrolledInProgram']]['DaysToReadmission']
        not_enrolled = df[~df['EnrolledInProgram']]['DaysToReadmission']
        t_stat, p_value = stats.ttest_ind(enrolled, not_enrolled, nan_policy='omit')
        logging.info(f"T-statistic: {t_stat}, P-value: {p_value}")
        
        return days_to_readmission.to_dict()
    except Exception as e:
        logging.error(f"Error in analyze_days_to_readmission: {e}")
        raise

def perform_subgroup_analysis(df):
    try:
        subgroup_results = {}
        for condition in df['ChronicCondition'].unique():
            subgroup = df[df['ChronicCondition'] == condition]
            control_rate = subgroup[subgroup['EnrolledInProgram'] == False]['IsReadmission'].mean()
            treatment_rate = subgroup[subgroup['EnrolledInProgram'] == True]['IsReadmission'].mean()
            subgroup_results[condition] = {
                'control_rate': control_rate,
                'treatment_rate': treatment_rate
            }
            logging.info(f"\nSubgroup: {condition}")
            logging.info(f"Control readmission rate: {control_rate:.2%}")
            logging.info(f"Treatment readmission rate: {treatment_rate:.2%}")
        return subgroup_results
    except Exception as e:
        logging.error(f"Error in perform_subgroup_analysis: {e}")
        raise

