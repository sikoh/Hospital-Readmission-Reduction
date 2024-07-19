from data_loading import load_data
from analysis import analyze_results
from visualizations import create_visualizations
import logging

def main():
    try:
        # Load data
        df = load_data()
        
        # Analyze results
        results = analyze_results(df)
        
        # Create visualizations
        create_visualizations(df, results)

        logging.info("A/B testing analysis completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred during the A/B testing analysis: {e}")

if __name__ == "__main__":
    main()