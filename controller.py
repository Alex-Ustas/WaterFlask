import loader

EMPTY_FLASK = ' ' * 4


def solve(num: str, **flasks):
    show_flasks(flasks[num])
    flasks, steps, cases, status = solving(flasks[num], [], [], 'In')
    if status == 'Ok':
        for i in range(len(steps)):
            print(f'{i + 1:04d}  {steps[i]}:\t{loader.flasks_to_line(cases[i])}')
    else:
        print(steps)


def solving(flasks: list, steps: list, cases: list, status: str) -> (list, list, list, str):
    for flask in flasks:
        if flask != '':
            if len(flask.replace(flask[0], '')) > 0 or len(flask) < 4:
                break
    else:
        return flasks, steps, cases, 'Ok'
    for i in range(len(flasks)):
        flask_from = flasks[i].strip()
        if flask_from == '' or len(flask_from.replace(flask_from[0], '')) == 0 and len(flask_from) == 4:
            continue
        color = flask_from[-1]
        for j in range(len(flasks)):
            if j != i:
                flask_to = flasks[j].strip()
                if flask_to == '' and len(flask_from.replace(flask_from[0], '')) == 0:
                    continue
                if flask_to == '' or flask_to[-1] == color and len(flask_to) < 4:
                    new = list()
                    for k in range(len(flasks)):
                        if k == i:
                            new.append(flasks[k][:-1])
                        elif k == j:
                            new.append(flasks[k].strip() + color)
                        else:
                            new.append(flasks[k].strip())
                    if new in cases:
                        continue
                    else:
                        steps.append(f'{i + 1} -> {j + 1}')
                        cases.append(new)
                        if len(cases) == 1:
                            loader.save_steps(1, steps[-1], new, flasks)
                        else:
                            loader.save_steps(len(cases), steps[-1], new)
                        new, steps, cases, status = solving(new, steps, cases, 'In')
                        if status == 'Ok':
                            return new, steps, cases, status
    return flasks, steps, cases, 'Failed'


def generate_game(num='0', **flasks):
    flask = flask_number()
    print(flask)


def create_game(num='0', **kwargs):
    num = flask_number()
    symbols = list(chr(i) for i in range(ord('A'), ord('A') + num))
    symbols = ''.join(symbols)
    amount = '0' * num
    flasks = dict()
    flasks['0'] = list()
    print('Enter flasks:')
    for i in range(num):
        print(f'{symbols}\n{amount}')
        flask = input(f'{i + 1}: ').upper()
        if check_flask(flask, symbols):
            if flasks['0']:
                flasks['0'].append(flask)
            else:
                flasks['0'] = [flask]
        while not check_flask(flask, symbols):
            print('Wrong input')
            flask = input(f'{i + 1}: ').upper()
            if check_flask(flask, symbols):
                if flasks['0']:
                    flasks['0'].append(flask)
                else:
                    flasks['0'] = [flask]
        q = list(map(int, list(j for j in amount)))
        for j in range(len(symbols)):
            if symbols[j] in flask:
                q[j] += flask.count(symbols[j])
        amount = ''.join(list(map(str, q)))
    flasks['0'].append(EMPTY_FLASK)
    flasks['0'].append(EMPTY_FLASK)
    menu(loader.load_menu('create'), '0', **flasks)


def save_flask(num='0', **flasks):
    while EMPTY_FLASK in flasks[num]:
        flasks[num].remove(EMPTY_FLASK)
    loader.save_flask(flasks[num])


def check_flask(flask: str, symbols: str) -> int:
    if len(flask) != 4:
        return 0
    for char in flask:
        if char not in symbols:
            return 0
    return 1


def show_flasks(flasks: list):
    one_row = len(flasks) // 2 + len(flasks) % 2
    for i in range(one_row):
        print(f'{i + 1} - [{flasks[i].upper().replace(" ", ".")}]', end='')
        if one_row + i < len(flasks):
            print(f'\t\t{one_row + i + 1} - [{flasks[one_row + i].upper().replace(" ", ".")}]')
        else:
            print('\n')


def load_flask(num='z', **kwargs):
    flasks = loader.load_flasks()
    print('Total flasks:', len(flasks))
    flask = None
    while flask is None:
        num = input('Enter flask number: ')
        flask = flasks.get(num, None)
        if flask is None:
            print('Wrong number')
    show_flasks(flasks[num])
    if flasks[num][-1] == 'test':
        flasks[num] = flasks[num][:-1]
    else:
        flasks[num].append(EMPTY_FLASK)
        flasks[num].append(EMPTY_FLASK)
    menu(loader.load_menu('load'), num, **flasks)


def flask_number() -> int:
    num = 'a'
    flask = 0
    while flask < 4 or flask > 15:
        while not num.isdigit():
            num = input('Number of flasks (4 - 15): ')
            if not num.isdigit():
                print('Please enter number of flasks')
        flask = int(num)
        if 16 > flask > 3:
            break
        print('Wrong number of flask!')
        num = 'a'
    return flask


def menu(menu_items: list, num='0', **kwargs):
    while True:
        for i in range(len(menu_items)):
            if i == len(menu_items) - 1:
                print(f'0 - {menu_items[i][0]}')
            else:
                print(f'{i + 1} - {menu_items[i][0]}')
        item = input('Your choice: ')
        if not item.isdigit():
            print('Please enter number from the list')
        elif 0 < int(item) < len(menu_items):
            func = menu_items[int(item) - 1][1]
            if func == 'dummy':
                print('Under construction')
            else:
                func = eval(func)
                func(num, **kwargs)
        elif item == '0':
            break
        else:
            print('Wrong number')
        print()


def main_menu():
    menu(loader.load_menu('main'))


if __name__ == '__main__':
    main_menu()
