import os
import random
import sys
import time
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
GAME_NAME = "starfighter"
ENEMY_SPRITE = "VVVVV"
ENEMY_HALF_WIDTH = len(ENEMY_SPRITE) // 2
ENEMY_FALL_INTERVAL = 3
INITIAL_MAX_ENEMIES = 2
MAX_ENEMIES = 5
ENEMIES_PER_MAX_INCREASE = 10


def clear_screen():
    print("\033[2J\033[H", end="")


def move_cursor(row, col):
    print(f"\033[{row};{col}H", end="")


def hide_cursor():
    print("\033[?25l", end="")


def show_cursor():
    print("\033[?25h", end="")


def color_from_hex(hex_code):
    value = hex_code.strip().lstrip("#")
    if len(value) != 6:
        return ""
    try:
        r = int(value[0:2], 16)
        g = int(value[2:4], 16)
        b = int(value[4:6], 16)
    except ValueError:
        return ""
    return f"\033[38;2;{r};{g};{b}m"


def find_first_existing(paths):
    for path in paths:
        if path.exists():
            return path
    return paths[0]


def load_gamertag():
    tmp_path = find_first_existing(
        [
            BASE_DIR / "spielerdaten" / "tmp.txt",
            ROOT_DIR / "spielerdaten" / "tmp.txt",
        ]
    )
    try:
        tag = tmp_path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        tag = "gamertag"
    return tag or "gamertag"


def profile_paths(gamertag):
    return {
        "settings": find_first_existing(
            [
                BASE_DIR / "spielerdaten" / f"settings_{gamertag}.txt",
                BASE_DIR / f"settings_{gamertag}.txt",
                ROOT_DIR / f"settings_{gamertag}.txt",
                BASE_DIR / "settings_gamertag.txt",
            ]
        ),
        "highscore": find_first_existing(
            [
                BASE_DIR / "spielerdaten" / f"highscore_{gamertag}.txt",
                BASE_DIR / f"highscore_{gamertag}.txt",
                ROOT_DIR / f"highscore_{gamertag}.txt",
                BASE_DIR / "highscore_gamertag.txt",
            ]
        ),
    }


def load_terminal_color(settings_path):
    try:
        return color_from_hex(settings_path.read_text(encoding="utf-8").splitlines()[0])
    except (FileNotFoundError, IndexError):
        return ""


def save_score(highscore_path, score):
    highscore_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        lines = highscore_path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        lines = ["", f"{GAME_NAME}:"]

    while len(lines) < 2:
        lines.append("")

    game_line_index = None
    for index, line in enumerate(lines):
        if line.startswith(f"{GAME_NAME}:"):
            game_line_index = index
            break

    if game_line_index is None:
        game_line_index = 1
        if lines[game_line_index].strip():
            lines.insert(game_line_index, f"{GAME_NAME}:")
        else:
            lines[game_line_index] = f"{GAME_NAME}:"

    current = lines[game_line_index].strip()
    separator = "" if current.endswith(":") else ","
    lines[game_line_index] = f"{current}{separator}{score}"
    highscore_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


class Keyboard:
    def __enter__(self):
        self.windows = os.name == "nt"
        if self.windows:
            import msvcrt

            self.msvcrt = msvcrt
        else:
            import termios
            import tty

            self.termios = termios
            self.old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
        return self

    def __exit__(self, exc_type, exc, tb):
        if not self.windows:
            self.termios.tcsetattr(sys.stdin, self.termios.TCSADRAIN, self.old_settings)

    def get_key(self):
        if self.windows:
            if not self.msvcrt.kbhit():
                return None
            key = self.msvcrt.getch()
            if key in (b"\x00", b"\xe0"):
                key = self.msvcrt.getch()
                return {"K": "left", "M": "right"}.get(key.decode(errors="ignore"))
            return key.decode(errors="ignore").lower()

        import select

        if select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.read(1).lower()
        return None


def terminal_size():
    size = os.get_terminal_size()
    width = max(40, min(size.columns, 100))
    height = max(20, min(size.lines, 35))
    return width, height


def draw_border(width, height):
    move_cursor(2, 1)
    print("+" + "-" * (width - 2) + "+", end="")
    for row in range(3, height):
        move_cursor(row, 1)
        print("|", end="")
        move_cursor(row, width)
        print("|", end="")
    move_cursor(height, 1)
    print("+" + "-" * (width - 2) + "+", end="")


def countdown(gamertag, color):
    clear_screen()
    hide_cursor()
    for number in (3, 2, 1):
        clear_screen()
        width, height = terminal_size()
        text = f"Star Fighter startet in {number}"
        move_cursor(1, 1)
        print(f"{color}{gamertag}\033[0m", end="")
        move_cursor(height // 2, max(1, (width - len(text)) // 2))
        print(f"{color}{text}\033[0m", end="")
        sys.stdout.flush()
        time.sleep(1)
    clear_screen()


def draw_game(gamertag, color, player_x, shots, enemies, score, lives, width, height):
    clear_screen()
    move_cursor(1, 1)
    print(f"{color}{gamertag}\033[0m", end="")
    info = f"Score: {score}  Leben: {lives}  A/D oder Pfeile: bewegen  Space: schiessen  Q: Ende"
    move_cursor(1, max(1, width - len(info) + 1))
    print(info[:width], end="")
    draw_border(width, height)

    for shot in shots:
        if 3 <= shot["y"] < height and 2 <= shot["x"] < width:
            move_cursor(shot["y"], shot["x"])
            print("|", end="")

    for enemy in enemies:
        start_x = enemy["x"] - ENEMY_HALF_WIDTH
        enemy_end_x = start_x + len(ENEMY_SPRITE) - 1
        if 3 <= enemy["y"] < height and 2 <= start_x and enemy_end_x < width:
            move_cursor(enemy["y"], start_x)
            print(ENEMY_SPRITE, end="")

    ship = "/^\\"
    move_cursor(height - 1, player_x - 1)
    print(f"{color}{ship}\033[0m", end="")
    sys.stdout.flush()


def max_visible_enemies(defeated_enemies):
    increases = defeated_enemies // ENEMIES_PER_MAX_INCREASE
    return min(MAX_ENEMIES, INITIAL_MAX_ENEMIES + increases)


def game_loop(gamertag, color):
    width, height = terminal_size()
    player_x = width // 2
    shots = []
    enemies = []
    score = 0
    lives = 100
    defeated_enemies = 0
    tick = 0
    fall_tick = 0
    next_enemy_in = 4
    frame_time = 0.04

    with Keyboard() as keyboard:
        while lives > 0:
            started = time.monotonic()
            key = keyboard.get_key()
            if key in ("q", "\x1b"):
                break
            if key in ("a", "left"):
                player_x = max(3, player_x - 2)
            if key in ("d", "right"):
                player_x = min(width - 2, player_x + 2)
            if key == " ":
                shots.append({"x": player_x, "y": height - 2})

            tick += 1
            if tick >= next_enemy_in and len(enemies) < max_visible_enemies(defeated_enemies):
                tick = 0
                next_enemy_in = max(2, 7 - score // 500)
                enemies.append(
                    {"x": random.randint(2 + ENEMY_HALF_WIDTH, width - 1 - ENEMY_HALF_WIDTH), "y": 3}
                )

            for shot in shots:
                shot["y"] -= 1
            fall_tick += 1
            if fall_tick >= ENEMY_FALL_INTERVAL:
                fall_tick = 0
                for enemy in enemies:
                    enemy["y"] += 1

            new_shots = []
            hit_shots = set()
            hit_enemies = set()
            for shot_index, shot in enumerate(shots):
                for enemy_index, enemy in enumerate(enemies):
                    if abs(shot["x"] - enemy["x"]) <= ENEMY_HALF_WIDTH and shot["y"] == enemy["y"]:
                        hit_shots.add(shot_index)
                        hit_enemies.add(enemy_index)
                        score += 100
                        defeated_enemies += 1
                        break

            for shot_index, shot in enumerate(shots):
                if shot_index not in hit_shots and shot["y"] > 2:
                    new_shots.append(shot)
            shots = new_shots

            new_enemies = []
            for enemy_index, enemy in enumerate(enemies):
                if enemy_index in hit_enemies:
                    continue
                if enemy["y"] >= height - 1:
                    lives -= 1
                    continue
                if enemy["y"] == height - 1 and abs(enemy["x"] - player_x) <= ENEMY_HALF_WIDTH:
                    lives -= 1
                    continue
                new_enemies.append(enemy)
            enemies = new_enemies

            score += 1
            draw_game(gamertag, color, player_x, shots, enemies, score, lives, width, height)

            remaining = frame_time - (time.monotonic() - started)
            if remaining > 0:
                time.sleep(remaining)

    return score


def ask_save_score(gamertag, color, score):
    clear_screen()
    width, height = terminal_size()
    lines = [
        "GAME OVER",
        f"{gamertag}, dein Score: {score}",
        "Highscore speichern? (j/n)",
    ]
    for index, line in enumerate(lines):
        move_cursor(height // 2 + index, max(1, (width - len(line)) // 2))
        print(f"{color}{line}\033[0m" if index == 0 else line, end="")
    sys.stdout.flush()

    while True:
        choice = input().strip().lower()
        if choice in ("j", "n"):
            return choice == "j"
        move_cursor(height // 2 + len(lines) + 1, max(1, (width - 31) // 2))
        print("Bitte j oder n eingeben.", end="")
        sys.stdout.flush()


def game_over(gamertag, color, score, saved):
    clear_screen()
    width, height = terminal_size()
    saved_text = "Score wurde gespeichert." if saved else "Score wurde nicht gespeichert."
    lines = [
        "GAME OVER",
        f"{gamertag}, dein Score: {score}",
        saved_text,
        "Enter druecken, um zurueckzukehren.",
    ]
    for index, line in enumerate(lines):
        move_cursor(height // 2 + index, max(1, (width - len(line)) // 2))
        print(f"{color}{line}\033[0m" if index == 0 else line, end="")
    sys.stdout.flush()
    input()


def main():
    os.system("")
    gamertag = load_gamertag()
    paths = profile_paths(gamertag)
    color = load_terminal_color(paths["settings"])

    try:
        countdown(gamertag, color)
        score = game_loop(gamertag, color)
        saved = ask_save_score(gamertag, color, score)
        if saved:
            save_score(paths["highscore"], score)
        game_over(gamertag, color, score, saved)
    finally:
        show_cursor()
        print("\033[0m", end="")


if __name__ == "__main__":
    main()
