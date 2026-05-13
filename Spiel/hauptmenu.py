import os
import subprocess
import sys

DATA_DIR = os.path.join(os.path.dirname(__file__), "spielerdaten")
SPIEL_DIR = os.path.dirname(__file__)


def spieler_init(name: str) -> dict:
    os.makedirs(DATA_DIR, exist_ok=True)

    settings_pfad = os.path.join(DATA_DIR, f"settings_{name}.txt")
    highscore_pfad = os.path.join(DATA_DIR, f"highscore_{name}.txt")
    tmp_pfad = os.path.join(DATA_DIR, "tmp.txt")

    if not os.path.exists(settings_pfad):
        with open(settings_pfad, "w") as f:
            f.write("#FFFFFF\n")

    if not os.path.exists(highscore_pfad):
        open(highscore_pfad, "w").close()

    with open(tmp_pfad, "w") as f:
        f.write(name + "\n")

    return {"settings": settings_pfad, "highscore": highscore_pfad, "tmp": tmp_pfad}


def lade_highscores(name: str) -> dict:
    pfad = os.path.join(DATA_DIR, f"highscore_{name}.txt")
    scores = {}
    with open(pfad) as f:
        for zeile in f:
            zeile = zeile.strip()
            if ":" in zeile:
                spiel, werte = zeile.split(":", 1)
                scores[spiel] = [int(p) for p in werte.split(",") if p]
    return scores


def zeige_hauptmenu(name: str):
    while True:
        print(f"\n{'='*40}")
        print(f"  Hauptmenü  –  Spieler: {name}")
        print(f"{'='*40}")
        print("  [1]  Starfighter")
        print("  [2]  Highscores anzeigen")
        print("  [3]  Einstellungen")
        print("  [0]  Beenden")
        print(f"{'='*40}")

        auswahl = input("Auswahl: ").strip()

        if auswahl == "1":
            starte_spiel("starfighter")
            git_auto_save(name)
        elif auswahl == "2":
            scores = lade_highscores(name)
            print(f"\nHighscores für {name}:")
            if scores:
                for spiel, werte in scores.items():
                    print(f"  {spiel}: {','.join(str(p) for p in werte)}")
            else:
                print("  Noch keine Einträge.")
        elif auswahl == "3":
            zeige_einstellungen(name)
        elif auswahl == "0":
            print("Auf Wiedersehen!")
            break
        else:
            print("Ungültige Eingabe.")


def starte_spiel(spiel_key: str):
    spiel_pfad = os.path.join(SPIEL_DIR, f"{spiel_key}.py")
    subprocess.run([sys.executable, spiel_pfad])


def git_auto_save(name: str):
    settings = os.path.join("spielerdaten", f"settings_{name}.txt")
    highscore = os.path.join("spielerdaten", f"highscore_{name}.txt")

    status = subprocess.run(
        ["git", "status", "--porcelain", settings, highscore],
        cwd=SPIEL_DIR, capture_output=True, text=True
    )
    if status.returncode != 0:
        print(f"[!] Git-Status fehlgeschlagen: {status.stderr.strip()}")
        return
    if not status.stdout.strip():
        return

    result = subprocess.run(
        ["git", "add", settings, highscore],
        cwd=SPIEL_DIR, capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"[!] Git-Add fehlgeschlagen: {result.stderr.strip()}")
        return

    result = subprocess.run(
        ["git", "commit", "-m", f"Auto-save: {name} nach Starfighter"],
        cwd=SPIEL_DIR, capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"[!] Git-Commit fehlgeschlagen: {result.stderr.strip()}")
        return

    result = subprocess.run(
        ["git", "push"],
        cwd=SPIEL_DIR, capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"[!] Git-Push fehlgeschlagen: {result.stderr.strip()}")
        return

    print(f"Spielstand von '{name}' gespeichert und gepusht.")


def wende_farbe_an(hex_farbe: str):
    r = int(hex_farbe[1:3], 16)
    g = int(hex_farbe[3:5], 16)
    b = int(hex_farbe[5:7], 16)
    print(f"\033[38;2;{r};{g};{b}m", end="", flush=True)


FARBEN = {
    "1": ("Weiß",       "#FFFFFF"),
    "2": ("Grün",       "#00FF00"),
    "3": ("Cyan",       "#00FFFF"),
    "4": ("Gelb",       "#FFFF00"),
    "5": ("Orange",     "#FF8800"),
    "6": ("Rot",        "#FF0000"),
    "7": ("Pink",       "#FF00FF"),
    "8": ("Hellblau",   "#00AAFF"),
    "9": ("Eigener Hex-Code", None),
}


def zeige_einstellungen(name: str):
    settings_pfad = os.path.join(DATA_DIR, f"settings_{name}.txt")
    with open(settings_pfad) as f:
        farbe = f.read().strip()

    while True:
        print(f"\n{'='*40}")
        print(f"  Einstellungen  –  Spieler: {name}")
        print(f"{'='*40}")
        print(f"  Aktuelle Farbe: {farbe}")
        print()
        for key, (label, hex_wert) in FARBEN.items():
            vorschau = f"({hex_wert})" if hex_wert else ""
            print(f"  [{key}]  {label} {vorschau}")
        print("  [0]  Zurück")
        print(f"{'='*40}")

        auswahl = input("Auswahl: ").strip()

        if auswahl == "0":
            break
        elif auswahl in FARBEN:
            label, hex_wert = FARBEN[auswahl]
            if hex_wert is None:
                eingabe = input("Hex-Code eingeben (z.B. #FF0000): ").strip().upper()
                if len(eingabe) == 7 and eingabe.startswith("#"):
                    try:
                        int(eingabe[1:], 16)
                        hex_wert = eingabe
                    except ValueError:
                        print("Ungültiger Hex-Code.")
                        continue
                else:
                    print("Format muss #RRGGBB sein.")
                    continue
            farbe = hex_wert
            with open(settings_pfad, "w") as f:
                f.write(farbe + "\n")
            wende_farbe_an(farbe)
            print(f"Farbe gesetzt: {label} ({farbe})")
            break
        else:
            print("Ungültige Eingabe.")


def git_auto_pull():
    result = subprocess.run(
        ["git", "pull"],
        cwd=SPIEL_DIR, capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"[!] Git-Pull fehlgeschlagen: {result.stderr.strip()}")


def main():
    git_auto_pull()
    print("╔══════════════════════════════════════╗")
    print("║       Willkommen im Spielmenü        ║")
    print("╚══════════════════════════════════════╝")

    while True:
        name = input("\nBitte gib deinen Spielernamen ein: ").strip()
        if name:
            break
        print("Name darf nicht leer sein.")

    dateien = spieler_init(name)
    with open(dateien["settings"]) as f:
        farbe = f.read().strip()
    wende_farbe_an(farbe)
    print(f"\nSpieler '{name}' geladen.")

    zeige_hauptmenu(name)


if __name__ == "__main__":
    main()
