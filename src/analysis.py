import pandas as pd
import matplotlib.pyplot as plt
import os
import logging

def plot_goals_vs_xg(input_file, output_file):
    try:
        logging.info(" Loading cleaned dataset...")
        df = pd.read_csv(input_file)

        # Rename and clean columns
        df.columns = [
            'Season', 'Age', 'Squad', 'Country', 'Comp', 'LgRank', '90s', 'Goals', 'Shots',
            'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'Dist', 'FK', 'PK', 'PKatt',
            'xG', 'npxG', 'npxG/Sh', 'G-xG', 'np:G-xG', 'Matches'
        ]

        # Filter for actual seasons (not summary rows like "3 Seasons")
        df = df[df['Season'].str.contains('-')]

        # Convert columns
        df['Goals'] = pd.to_numeric(df['Goals'], errors='coerce')
        df['xG'] = pd.to_numeric(df['xG'], errors='coerce')

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 6))
        x = range(len(df))

        bars1 = ax.bar(x, df['Goals'], width=0.4, label='Goals', color='dodgerblue')
        bars2 = ax.bar([i + 0.4 for i in x], df['xG'], width=0.4, label='Expected Goals (xG)', color='orange')

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

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        plt.savefig(output_file)
        plt.show()
        logging.info(f" Plot saved to: {output_file}")

    except Exception as e:
        logging.error(f" Error generating plot: {e}")

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    input_file = "data/processed/lamine_yamal_stats_cleaned.csv"
    output_file = "output/plots/goals_vs_xg.png"
    plot_goals_vs_xg(input_file, output_file)

if __name__ == "__main__":
    main()
