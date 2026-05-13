import glob
import os


def read_highscore_files():
    files = glob.glob("highscore_*.txt")

    if not files:
        print("Keine Highscore-Dateien gefunden.")
        return

    for file_name in files:
        base_name = os.path.basename(file_name)
        gamertag = base_name.replace("highscore_", "").replace(".txt", "")

        print(f"\nGamertag: {gamertag}")

        with open(file_name, "r") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                try:
                    game, scores_raw = line.split(":")
                    scores = [int(s) for s in scores_raw.split(",")]

                    print(f"Spiel: {game}")
                    print(f"Scores: {scores}")
                    print(f"Bester Score: {max(scores)}")

                    print()

                except ValueError:
                    print(f"Fehlerhafte Zeile: {line}")


# Start
read_highscore_files()