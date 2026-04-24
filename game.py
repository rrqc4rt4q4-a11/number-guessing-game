#!/usr/bin/env python3
"""Number Guessing Game with levels, scores, and colorful UI."""

import random
import time

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

LEVELS = {
    "1": {"name": "Easy",   "range": 50,  "attempts": 10, "emoji": "🟢"},
    "2": {"name": "Medium", "range": 100, "attempts": 7,  "emoji": "🟡"},
    "3": {"name": "Hard",   "range": 200, "attempts": 5,  "emoji": "🔴"},
}


def draw_bar(attempts_left, max_attempts):
    filled = int((attempts_left / max_attempts) * 20)
    color = GREEN if filled > 13 else YELLOW if filled > 6 else RED
    bar = "█" * filled + "░" * (20 - filled)
    return f"[{color}{bar}{RESET}] {attempts_left}/{max_attempts}"


def calc_score(attempts_used, max_attempts, number_range):
    base = 1000
    penalty = (attempts_used - 1) * (base // max_attempts)
    bonus = number_range // 10
    return max(0, base - penalty + bonus)


def play_game(level):
    name = level["name"]
    max_num = level["range"]
    max_attempts = level["attempts"]
    emoji = level["emoji"]
    secret = random.randint(1, max_num)
    attempts_left = max_attempts
    history = []

    print(f"\n{BOLD}{CYAN}╔══════════════════════════════════╗")
    print(f"║  {emoji} {name} Mode — Guess 1 to {max_num:<6}  ║")
    print(f"╚══════════════════════════════════╝{RESET}\n")

    start_time = time.time()

    while attempts_left > 0:
        print(f"  Attempts left: {draw_bar(attempts_left, max_attempts)}")
        if history:
            print(f"  Previous guesses: {YELLOW}{', '.join(map(str, history))}{RESET}")
        try:
            guess = int(input(f"\n  Your guess: "))
        except ValueError:
            print(f"  {RED}Please enter a valid number!{RESET}")
            continue

        if guess < 1 or guess > max_num:
            print(f"  {RED}Please guess between 1 and {max_num}!{RESET}")
            continue

        history.append(guess)
        attempts_left -= 1

        if guess == secret:
            elapsed = round(time.time() - start_time, 1)
            attempts_used = max_attempts - attempts_left
            score = calc_score(attempts_used, max_attempts, max_num)
            print(f"\n  {GREEN}{BOLD}Correct! The number was {secret}!{RESET}")
            print(f"  Time: {elapsed}s")
            print(f"  Attempts used: {attempts_used}/{max_attempts}")
            print(f"  Score: {YELLOW}{BOLD}{score}{RESET}\n")
            return score
        elif guess < secret:
            diff = secret - guess
            hint = "Very close!" if diff <= 5 else "Go higher!"
            print(f"  {BLUE}{hint} Too low!{RESET}")
        else:
            diff = guess - secret
            hint = "Very close!" if diff <= 5 else "Go lower!"
            print(f"  {MAGENTA}{hint} Too high!{RESET}")

    print(f"\n  {RED}{BOLD}Game over! The number was {secret}.{RESET}\n")
    return 0


def main():
    total_score = 0
    games_played = 0
    wins = 0

    print(f"\n{BOLD}{CYAN}╔══════════════════════════════════╗")
    print(f"║     NUMBER GUESSING GAME         ║")
    print(f"╚══════════════════════════════════╝{RESET}")

    while True:
        print(f"\n{BOLD}  Choose difficulty:{RESET}")
        for key, lvl in LEVELS.items():
            print(f"  [{key}] {lvl['name']} — 1 to {lvl['range']}, {lvl['attempts']} attempts")
        print(f"  [4] Stats")
        print(f"  [5] Quit")

        choice = input(f"\n  Choose [1-5]: ").strip()

        if choice in LEVELS:
            score = play_game(LEVELS[choice])
            games_played += 1
            total_score += score
            if score > 0:
                wins += 1
            again = input(f"  Play again? (y/n): ").strip().lower()
            if again != "y":
                break
        elif choice == "4":
            print(f"\n{BOLD}{CYAN}Your Stats:{RESET}")
            print(f"  Games played : {games_played}")
            print(f"  Wins         : {GREEN}{wins}{RESET}")
            print(f"  Losses       : {RED}{games_played - wins}{RESET}")
            print(f"  Total score  : {YELLOW}{total_score}{RESET}")
            if games_played > 0:
                avg = total_score // games_played
                print(f"  Average score: {avg}")
        elif choice == "5":
            print(f"\n  {CYAN}Thanks for playing! Final score: {YELLOW}{total_score}{RESET}\n")
            break
        else:
            print(f"  {RED}Please choose 1-5.{RESET}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{YELLOW}Game cancelled.{RESET}")
