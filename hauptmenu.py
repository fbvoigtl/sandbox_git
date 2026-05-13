import os
import json

DATA_DIR = os.path.join(os.path.dirname(__file__), "spielerdaten")


def spieler_init(name: str) -> dict:
    os.makedirs(DATA_DIR, exist_ok=True)

    settings_pfad = os.path.join(DATA_DIR, f"settings_{name}.txt")
    highscore_pfad = os.path.join(DATA_DIR, f"highscore_{name}.txt")
    tmp_pfad = os.path.join(DATA_DIR, f"tmp.txt")

    if not os.path.exists(settings_pfad):
        with open(settings_pfad, "w") as f:
            json.dump({"farbe": "#FFFFFF"}, f, indent=2)

    if not os.path.exists(highscore_pfad):
        with open(highscore_pfad, "w") as f:
            pass

    with open(tmp_pfad, "w") as f:
        json.dump({"gamertag": name}, f, indent=2)

    return {"settings": settings_pfad, "highscore": highscore_pfad, "tmp": tmp_pfad}


def lade_highscores(name: str) -> dict:
    pfad = os.path.join(DATA_DIR, f"highscore_{name}.txt")
    with open(pfad) as f:
        return json.load(f)


def zeige_hauptmenu(name: str):
    while True:
        print(f"\n{'='*40}")
        print(f"  Hauptmenü  –  Spieler: {name}")
        print(f"{'='*40}")
        print("  [1]  Spiel 1 starten")
        print("  [2]  Spiel 2 starten")
        print("  [3]  Highscores anzeigen")
        print("  [4]  Einstellungen")
        print("  [0]  Beenden")
        print(f"{'='*40}")

        auswahl = input("Auswahl: ").strip()

        if auswahl == "1":
            starte_spiel(name, "spiel1")
        elif auswahl == "2":
            starte_spiel(name, "spiel2")
        elif auswahl == "3":
            scores = lade_highscores(name)
            print(f"\nHighscores für {name}:")
            for spiel, punkte in scores.items():
                print(f"  {spiel}: {punkte} Punkte")
        elif auswahl == "4":
            zeige_einstellungen(name)
        elif auswahl == "0":
            print("Auf Wiedersehen!")
            break
        else:
            print("Ungültige Eingabe.")


def starte_spiel(name: str, spiel_key: str):
    tmp_pfad = os.path.join(DATA_DIR, f"tmp_{name}.txt")
    with open(tmp_pfad) as f:
        tmp = json.load(f)
    tmp["aktives_spiel"] = spiel_key
    tmp["punkte"] = 0
    with open(tmp_pfad, "w") as f:
        json.dump(tmp, f, indent=2)

    print(f"\n{spiel_key} gestartet – hier käme das Spiel...")

    # Beispiel: Spieler erzielt 42 Punkte
    punkte = 42
    tmp["punkte"] = punkte
    tmp["aktives_spiel"] = None
    with open(tmp_pfad, "w") as f:
        json.dump(tmp, f, indent=2)

    highscore_pfad = os.path.join(DATA_DIR, f"highscore_{name}.txt")
    with open(highscore_pfad) as f:
        scores = json.load(f)
    if punkte > scores.get(spiel_key, 0):
        scores[spiel_key] = punkte
        with open(highscore_pfad, "w") as f:
            json.dump(scores, f, indent=2)
        print(f"Neuer Highscore: {punkte} Punkte!")
    else:
        print(f"Dein Highscore bleibt: {scores[spiel_key]} Punkte.")


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
        settings = json.load(f)

    while True:
        print(f"\n{'='*40}")
        print(f"  Einstellungen  –  Spieler: {name}")
        print(f"{'='*40}")
        print(f"  Aktuelle Farbe: {settings['farbe']}")
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
            settings["farbe"] = hex_wert
            with open(settings_pfad, "w") as f:
                json.dump(settings, f, indent=2)
            wende_farbe_an(hex_wert)
            print(f"Farbe gesetzt: {label} ({hex_wert})")
            break
        else:
            print("Ungültige Eingabe.")


def main():
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
        settings = json.load(f)
    wende_farbe_an(settings["farbe"])
    print(f"\nSpieler '{name}' geladen.")

    zeige_hauptmenu(name)


if __name__ == "__main__":
    main()
