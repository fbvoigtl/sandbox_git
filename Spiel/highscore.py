import glob
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "spielerdaten"


def read_highscore_files():
    files = glob.glob(str(DATA_DIR / "highscore_*.txt"))

    if not files:
        print("Keine Highscore-Dateien gefunden.")
        return

    for file_name in files:
        base_name = os.path.basename(file_name)
        gamertag = base_name.replace("highscore_", "").replace(".txt", "")
        found_scores = False

        print(f"\nGamertag: {gamertag}")

        with open(file_name, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                try:
                    game, scores_raw = line.split(":", 1)
                    scores = [int(s) for s in scores_raw.split(",") if s.strip()]

                    if not scores:
                        print(f"Spiel: {game}")
                        print("Noch keine Scores gespeichert.")
                        print()
                        continue

                    print(f"Spiel: {game}")
                    print(f"Scores: {scores}")
                    print(f"Bester Score: {max(scores)}")
                    found_scores = True

                    print()

                except ValueError:
                    print(f"Fehlerhafte Zeile: {line}")

        if not found_scores:
            print("Noch keine Scores gespeichert.")


# Start
read_highscore_files()
