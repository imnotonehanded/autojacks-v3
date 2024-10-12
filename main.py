import keyboard
from colorama import Fore
import time
from num2words import num2words
from json import loads
from tqdm import tqdm
import os
import random

toggle = False

with open("config.json", "r") as config_file:
    config_json = loads(config_file.read())
    try:
        wpm = config_json["wpm"]
        delay = config_json["time_to_start"]
        toggle_key = config_json["toggle_key"]
    except KeyError:
        print(f"{Fore.RED}ERR: Config.json is not set up correctly, please make sure you include the following fields:\n"
              f"\twpm (number, words per minute)\n"
              f"\ttime_to_start (how long in seconds it'll take to start jumping)\n"
              f"\ttoggle_key (key to start/stop program)")
        exit()

    cps = (wpm * 5) / 60 if isinstance(wpm, int) else 4
    delay = delay if isinstance(delay, int) else 5
    toggle_key = toggle_key if keyboard.parse_hotkey(toggle_key) else "right ctrl"

def main():
    global toggle

    print(Fore.RESET)
    print(f"{Fore.YELLOW}[1] ONE! | JJs\n{Fore.BLUE}[2] One. | GJs\n{Fore.GREEN}[3] O N E ONE! | HJs")

    choice = int(input(f"{Fore.WHITE}Enter your selection: ")) or 1
    amount = int(input("How many jumping jacks: "))
    match choice:
        case 1 | 2:
            os.system("cls")
            print(f"{Fore.CYAN}Press {toggle_key} to start")

            for i in tqdm(range(amount), unit="JJ"):
                while not toggle:
                    time.sleep(0.2)

                jump_and_slash()

                word_to_send = format_word(i, choice)
                time.sleep(random_delay(2/len(word_to_send)))
                keyboard.write(word_to_send)
                time.sleep(len(word_to_send) / cps)

                keyboard.press("enter")
                time.sleep(random_delay(0.2))
            toggle = False
            main()
        case 3:
            os.system("cls")
            print(f"{Fore.CYAN}Press {toggle_key} to start")

            for i in tqdm(range(amount), unit="JJ"):
                word_to_send = format_word(i, 3)

                for j in word_to_send.strip(" ").strip("!"):
                    while not toggle:
                        time.sleep(0.2)

                    jump_and_slash()

                    time.sleep(random_delay(0.3))
                    keyboard.write(j)
                    time.sleep(random_delay(0.7))

                    keyboard.press("enter")
                    time.sleep(random_delay(0.2))

                jump_and_slash()
                time.sleep(random_delay(2/len(word_to_send)))
                keyboard.write(word_to_send)
                time.sleep(len(word_to_send) / cps)

                keyboard.press("enter")
                time.sleep(random_delay(0.2))
            toggle = False
            main()

def random_delay(sec: float):
    random_min = sec - random.uniform(0, sec * 0.1)
    random_max = sec + random.uniform(0, sec * 0.1)

    return random.uniform(random_min, random_max)

def jump_and_slash():
    keyboard.press('space')
    time.sleep(random_delay(0.2))
    keyboard.release('space')

    keyboard.press_and_release('/')

def toggle_pause():
    global toggle
    toggle = not toggle

def format_word(number: int, mode: 1 | 2 | 3):
    match mode:
        case 1 | 3:
            return (num2words(int(number)+1)
                    .replace("-", " ")
                    .replace("and", "")
                    .upper()
                    + "!"
                    )
        case 2:
            return (num2words(int(number)+1)
                    .replace("-", " ")
                    + "."
                    )


keyboard.add_hotkey(toggle_key, toggle_pause)
main()