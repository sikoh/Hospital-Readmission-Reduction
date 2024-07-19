import matplotlib.pyplot as plt
import seaborn as sns
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_visualizations(df, results):
    try:
        # Set style for all plots
        plt.style.use('seaborn')

        # Create all visualizations
        create_overall_readmission_plot(results)
        create_subgroup_analysis_plot(results)
        create_age_distribution_plot(df)
        create_gender_distribution_plot(df)
        create_satisfaction_plot(results)
        create_days_to_readmission_plot(results)

        logging.info("All visualizations have been created and saved successfully.")
    except Exception as e:
        logging.error(f"Error in create_visualizations: {e}")
        raise

def create_overall_readmission_plot(results):
    try:
        plt.figure(figsize=(10, 6))
        sns.barplot(x=['Control', 'Treatment'], 
                    y=[results['control_readmission_rate'], results['treatment_readmission_rate']])
        plt.title('Readmission Rates: Control vs Treatment')
        plt.ylabel('Readmission Rate')
        plt.savefig('overall_readmission_rates.png')
        plt.close()
        logging.info("Overall readmission plot created successfully.")
    except Exception as e:
        logging.error(f"Error creating overall readmission plot: {e}")
        raise

def create_subgroup_analysis_plot(results):
    try:
        conditions = list(results['subgroup_results'].keys())
        control_rates = [results['subgroup_results'][c]['control_rate'] for c in conditions]
        treatment_rates = [results['subgroup_results'][c]['treatment_rate'] for c in conditions]

        plt.figure(figsize=(12, 6))
        x = range(len(conditions))
        width = 0.35
        plt.bar([i - width/2 for i in x], control_rates, width, label='Control')
        plt.bar([i + width/2 for i in x], treatment_rates, width, label='Treatment')
        plt.xlabel('Chronic Condition')
        plt.ylabel('Readmission Rate')
        plt.title('Readmission Rates by Chronic Condition')
        plt.xticks(x, conditions, rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.savefig('subgroup_analysis.png')
        plt.close()
        logging.info("Subgroup analysis plot created successfully.")
    except Exception as e:
        logging.error(f"Error creating subgroup analysis plot: {e}")
        raise

def create_age_distribution_plot(df):
    try:
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x='Age', hue='EnrolledInProgram', multiple='stack')
        plt.title('Age Distribution: Control vs Treatment')
        plt.savefig('age_distribution.png')
        plt.close()
        logging.info("Age distribution plot created successfully.")
    except Exception as e:
        logging.error(f"Error creating age distribution plot: {e}")
        raise

def create_gender_distribution_plot(df):
    try:
        plt.figure(figsize=(10, 6))
        sns.countplot(data=df, x='Gender', hue='EnrolledInProgram')
        plt.title('Gender Distribution: Control vs Treatment')
        plt.savefig('gender_distribution.png')
        plt.close()
        logging.info("Gender distribution plot created successfully.")
    except Exception as e:
        logging.error(f"Error creating gender distribution plot: {e}")
        raise

def create_satisfaction_plot(results):
    try:
        plt.figure(figsize=(10, 6))
        sns.barplot(x=['Control', 'Treatment'], 
                    y=[results['satisfaction_scores'][False], results['satisfaction_scores'][True]])
        plt.title('Average Satisfaction Scores: Control vs Treatment')
        plt.ylabel('Satisfaction Score')
        plt.savefig('satisfaction_scores.png')
        plt.close()
        logging.info("Satisfaction plot created successfully.")
    except Exception as e:
        logging.error(f"Error creating satisfaction plot: {e}")
        raise

def create_days_to_readmission_plot(results):
    try:
        plt.figure(figsize=(10, 6))
        sns.barplot(x=['Control', 'Treatment'], 
                    y=[results['days_to_readmission'][False], results['days_to_readmission'][True]])
        plt.title('Average Days to Readmission: Control vs Treatment')
        plt.ylabel('Days to Readmission')
        plt.savefig('days_to_readmission.png')
        plt.close()
        logging.info("Days to readmission plot created successfully.")
    except Exception as e:
        logging.error(f"Error creating days to readmission plot: {e}")
        raise