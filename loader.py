# Save to csv, load from csv

import os

FLASK_CSV = 'data/flasks.csv'
MENU_CSV = 'data/menu.csv'
STEPS_FILE = 'data/steps.txt'


def load_menu(menu_id: str) -> list:
    """Load menu from csv to list"""
    menu = list()
    if not os.path.exists(MENU_CSV):
        return menu
    with open(MENU_CSV, 'r', encoding='utf-8') as file:
        all_lines = file.readlines()
    for line in all_lines:
        line = line.replace('\n', '')
        items = line.split(';')
        if items[0] == menu_id:
            for i in range(1, len(items)):
                menu.append(items[i].split(','))
            break
    return menu


def load_flasks() -> dict:
    """Load data from csv to dict"""
    flasks = dict()
    if not os.path.exists(FLASK_CSV):
        return flasks
    with open(FLASK_CSV, 'r', encoding='utf-8') as file:
        all_lines = file.readlines()
    for line in all_lines:
        line = line.replace('\n', '')
        if line:
            items = line.split(';')
            flasks[items[0]] = items[1:]
    return flasks


def save_flask(flask: list):
    """Write flask to file"""
    flasks = load_flasks()
    last = max(list(map(int, flasks.keys()))) + 1

    if os.path.exists(FLASK_CSV):
        file = open(FLASK_CSV, 'a', encoding='utf-8')
    else:
        file = open(FLASK_CSV, 'w', encoding='utf-8')
    line = f'{last};' + ';'.join(flask)
    file.write(line + '\n')
    file.close()


def save_steps(steps: dict, flasks: list, num: int):
    if os.path.exists(STEPS_FILE):
        file = open(STEPS_FILE, 'a', encoding='utf-8')
    else:
        file = open(STEPS_FILE, 'w', encoding='utf-8')
    file.write('_' * 40 + '\n')
    file.write(f'{num:04d}\t\t\t{flasks_to_line(flasks)}\n')
    for key, item in steps.items():
        file.write(f'{key:04d}  {item[0]}:\t{flasks_to_line(item[1])}\n')
    file.close()


def flasks_to_line(flasks: list) -> str:
    line_flask = ['[' + flask.strip().upper().ljust(4, ".") + ']' for flask in flasks]
    return ' '.join(line_flask)
