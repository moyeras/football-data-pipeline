import os
import sys
import io
import logging
import requests
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup, Comment
import matplotlib.pyplot as plt

# ---------- CONFIGURATION ----------
URL = "https://fbref.com/en/players/82ec26c1/Lamine-Yamal"
RAW_HTML_PATH = "data/raw/lamine_yamal_shooting.html"
RAW_CSV_PATH = "data/processed/lamine_yamal_shooting.csv"
CLEANED_CSV_PATH = "data/processed/lamine_yamal_stats_cleaned.csv"
PLOT_PATH = "output/plots/goals_vs_xg.png"

# ---------- SETUP ----------
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ---------- STEP 1: DATA COLLECTION ----------
def collect_data():
    logging.info("🔎 Collecting shooting data from FBref...")
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Save raw HTML
    os.makedirs(os.path.dirname(RAW_HTML_PATH), exist_ok=True)
    with open(RAW_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    # Parse hidden tables in comments
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment_soup = BeautifulSoup(comment, 'html.parser')
        for table in comment_soup.find_all("table"):
            soup.append(table)

    table = soup.find("table", {"id": "stats_shooting_dom_lg"})
    if table:
        df = pd.read_html(StringIO(str(table)))[0]
        os.makedirs(os.path.dirname(RAW_CSV_PATH), exist_ok=True)
        df.to_csv(RAW_CSV_PATH, index=False)
        logging.info(f"✅ Data collected and saved to {RAW_CSV_PATH}")
    else:
        raise ValueError("❌ Shooting table not found on the page.")

# ---------- STEP 2: DATA CLEANING ----------
def clean_data():
    logging.info("🧼 Cleaning raw shooting data...")
    df = pd.read_csv(RAW_CSV_PATH)

    df.columns = [
        "Season", "Age", "Squad", "Country", "Competition", "LeagueRank", "Minutes_90s",
        "Goals", "Shots", "Shots_on_Target", "SoT%", "Shots_per_90", "SoT_per_90", "Goals_per_Shot",
        "Goals_per_SoT", "Avg_Shot_Distance", "Free_Kick_Goals", "Penalties", "Penalties_Attempted",
        "xG", "npxG", "npxG_per_Shot", "G_minus_xG", "npG_minus_xG", "Matches"
    ]

    df = df[df['Season'].str.contains("202")].reset_index(drop=True)
    non_numeric = ["Season", "Squad", "Country", "Competition", "LeagueRank", "Matches"]
    numeric_cols = df.columns.difference(non_numeric)
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    os.makedirs(os.path.dirname(CLEANED_CSV_PATH), exist_ok=True)
    df.to_csv(CLEANED_CSV_PATH, index=False)
    logging.info(f"✅ Cleaned data saved to {CLEANED_CSV_PATH}")

# ---------- STEP 3: DATA ANALYSIS / PLOTTING ----------
def plot_goals_vs_xg():
    logging.info("📊 Generating goals vs xG visualization...")
    df = pd.read_csv(CLEANED_CSV_PATH)

    df.columns = [
        'Season', 'Age', 'Squad', 'Country', 'Comp', 'LgRank', '90s', 'Goals', 'Shots',
        'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'Dist', 'FK', 'PK', 'PKatt',
        'xG', 'npxG', 'npxG/Sh', 'G-xG', 'np:G-xG', 'Matches'
    ]

    df = df[df['Season'].str.contains('-')]
    df['Goals'] = pd.to_numeric(df['Goals'], errors='coerce')
    df['xG'] = pd.to_numeric(df['xG'], errors='coerce')

    fig, ax = plt.subplots(figsize=(10, 6))
    x = range(len(df))
    ax.bar(x, df['Goals'], width=0.4, label='Goals', color='dodgerblue')
    ax.bar([i + 0.4 for i in x], df['xG'], width=0.4, label='Expected Goals (xG)', color='orange')

    for i, (g, xg) in enumerate(zip(df['Goals'], df['xG'])):
        ax.text(i, g + 0.1, f"{g:.1f}", ha='center', fontsize=9, color='blue')
        ax.text(i + 0.4, xg + 0.1, f"{xg:.1f}", ha='center', fontsize=9, color='darkorange')

    ax.set_xticks([i + 0.2 for i in x])
    ax.set_xticklabels(df['Season'])
    ax.set_ylabel("Count")
    ax.set_xlabel("Season")
    ax.set_title("Lamine Yamal: Goals vs Expected Goals (xG) by Season")
    ax.legend()
    ax.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()

    os.makedirs(os.path.dirname(PLOT_PATH), exist_ok=True)
    plt.savefig(PLOT_PATH)
    plt.show()
    logging.info(f"✅ Plot saved to: {PLOT_PATH}")

# ---------- MAIN ----------
def main():
    collect_data()
    clean_data()
    plot_goals_vs_xg()
    logging.info("🏁 Pipeline completed successfully!")

if __name__ == "__main__":
    main()
