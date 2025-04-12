import pandas as pd
import os
import logging

def clean_shooting_data(input_path, output_path):
    try:
        logging.info("📥 Loading raw data...")
        df = pd.read_csv(input_path)

        # Rename columns
        df.columns = [
            "Season", "Age", "Squad", "Country", "Competition", "LeagueRank", "Minutes_90s",
            "Goals", "Shots", "Shots_on_Target", "SoT%", "Shots_per_90", "SoT_per_90", "Goals_per_Shot",
            "Goals_per_SoT", "Avg_Shot_Distance", "Free_Kick_Goals", "Penalties", "Penalties_Attempted",
            "xG", "npxG", "npxG_per_Shot", "G_minus_xG", "npG_minus_xG", "Matches"
        ]
        logging.info(" Columns renamed")

        # Filter valid seasons
        df = df[df['Season'].str.contains("202")].reset_index(drop=True)
        logging.info(" Filtered valid seasons")

        # Convert numeric columns
        non_numeric = ["Season", "Squad", "Country", "Competition", "LeagueRank", "Matches"]
        numeric_cols = df.columns.difference(non_numeric)
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
        logging.info(" Converted numeric columns")

        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save cleaned data
        df.to_csv(output_path, index=False)
        logging.info(f" Cleaned data saved to: {output_path}")

    except Exception as e:
        logging.error(f" Error during data cleaning: {e}")

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    input_file = "data/processed/lamine_yamal_shooting.csv"
    output_file = "data/processed/lamine_yamal_stats_cleaned.csv"
    clean_shooting_data(input_file, output_file)

if __name__ == "__main__":
    main()
