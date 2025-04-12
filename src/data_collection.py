import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
from io import StringIO
import sys
import io
import os
import logging

def main():
    # Setup logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.info("Starting data collection...")

    # Fix encoding issue on Windows
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # Target URL and paths
    url = "https://fbref.com/en/players/82ec26c1/Lamine-Yamal"
    raw_output_path = "data/raw/lamine_yamal_shooting.html"
    csv_output_path = "data/processed/lamine_yamal_shooting.csv"

    # Ensure directories exist
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    # Fetch page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Save raw HTML
    with open(raw_output_path, "w", encoding="utf-8") as f:
        f.write(soup.prettify())
    logging.info(f" Raw HTML saved to {raw_output_path}")

    # Parse hidden tables inside HTML comments
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment_soup = BeautifulSoup(comment, 'html.parser')
        for table in comment_soup.find_all("table"):
            soup.append(table)

    # Locate the shooting stats table
    shooting_table = soup.find("table", {"id": "stats_shooting_dom_lg"})

    # Extract to DataFrame
    if shooting_table:
        df = pd.read_html(StringIO(str(shooting_table)))[0]
        df.to_csv(csv_output_path, index=False)
        logging.info(f" Shooting table saved to {csv_output_path}")
        print(df.head())
    else:
        logging.warning(" Shooting table not found.")

# 🔁 Ensure the main() runs when script is executed
if __name__ == "__main__":
    main()
