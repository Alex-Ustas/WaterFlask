# Show text in terminal

from colorama import init, Fore, Back, Style

init(autoreset=True)

# char: color, style
COLORSET = {
    'A': ['RED', 'NORMAL'],
    'B': ['GREEN', 'NORMAL'],
    'C': ['BLUE', 'NORMAL'],
    'D': ['YELLOW', 'NORMAL'],
    'E': ['MAGENTA', 'NORMAL'],
    'F': ['CYAN', 'NORMAL'],
    'G': ['WHITE', 'NORMAL'],
    'H': ['LIGHTGREEN_EX', 'NORMAL'],
    'I': ['GREEN', 'BRIGHT'],
    'J': ['YELLOW', 'BRIGHT'],
    'K': ['MAGENTA', 'BRIGHT'],
    'L': ['WHITE', 'BRIGHT'],
    'M': ['BLUE', 'BRIGHT'],
    'N': ['CYAN', 'BRIGHT'],
    'O': ['LIGHTRED_EX', 'NORMAL'],
}


def print_text(text, view='normal'):
    """Print text \n
    view=critical - red text \n
    view=warning - yellow text \n
    view=ok - green text"""
    if view == 'critical':
        print(f'{Fore.RED}{text}')
    elif view == 'warning':
        print(f'{Fore.YELLOW}{text}')
    elif view == 'ok':
        print(f'{Fore.GREEN}{text}')
    else:
        print(text)


def color_char(char: str) -> str:
    if char in COLORSET.keys():
        fore = eval('Fore.' + COLORSET[char][0])
        style = eval('Style.' + COLORSET[char][1])
        return fore + style + char + Style.RESET_ALL
    else:
        return char


def color_string(text: str) -> str:
    color_text = list(color_char(char) for char in text)
    color_text = ''.join(color_text)
    return color_text


def show_colors():
    for char in COLORSET.keys():
        print(color_char(char), end=' ')
    print()


def show_flasks(flasks: list):
    one_row = len(flasks) // 2 + len(flasks) % 2
    for i in range(one_row):
        print(f'{i + 1} - [{color_string(flasks[i].upper().replace(" ", "."))}]', end='')
        if one_row + i < len(flasks):
            print(f'\t\t{one_row + i + 1} - [{color_string(flasks[one_row + i].upper().replace(" ", "."))}]')
        else:
            print('\n')


def show_steps(steps: dict):
    for key, item in steps.items():
        print(f'{key:04d}  {item[0]}:\t{color_string(flasks_to_line(item[1]))}')


def flasks_to_line(flasks: list) -> str:
    line = ''
    for flask in flasks:
        flask = flask.strip().upper()
        if len(flask) < 4:
            flask += '.' * (4 - len(flask))
        line += f' [{flask}]'
    return line.strip()
