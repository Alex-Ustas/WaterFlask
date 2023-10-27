import loader, view

COLORS = 4
EMPTY_FLASK = ' ' * COLORS


def gameplay(num: str, **flasks):
    flasks = flasks[num].copy()
    flasks.append(EMPTY_FLASK)
    flasks.append(EMPTY_FLASK)
    view.show_flasks(flasks)

    delimiter = ' .,-_>'
    steps = dict()
    steps[0] = ['begin', flasks.copy()]
    while True:
        step = input('Enter step\n(from to, r - back one step, s - Steps, 0 - Exit): ').strip()
        if step == '0':
            break
        if step.lower() == 'r':
            if len(steps) < 2:
                view.print_text("Still no one step", 'warning')
                continue
            last_step = max(steps.keys())
            new = steps[last_step - 1][1]
            steps.pop(last_step)
            for i in range(len(flasks)):
                flasks[i] = new[i] + ' ' * (COLORS - len(new[i]))
            view.show_flasks(flasks)
            continue
        if step.lower() == 's':
            if len(steps) < 2:
                view.print_text("Still no one step", 'warning')
                continue
            view.show_steps(steps)
            continue
        for sep in delimiter:
            if sep in step:
                step = step.split(sep)
                break
        else:
            view.print_text('Wrong input', 'critical')
            continue
        if len(step) != 2:
            view.print_text('Wrong input', 'critical')
            continue
        flag = True
        for part in step:
            if not part.isdigit():
                flag = False
                break
        if not flag:
            view.print_text('Wrong input', 'critical')
            continue
        step = list(map(int, step))
        if step[0] == 0 or step[1] == 0 or step[0] == step[1] or step[0] > len(flasks) or step[1] > len(flasks):
            view.print_text('Wrong flask number', 'critical')
            continue
        new = list(flask.strip() for flask in flasks)
        if len(new[step[0] - 1]) == 0 or len(new[step[1] - 1]) == COLORS:
            view.print_text("Wrong step, can't move color", 'critical')
            continue
        color = new[step[0] - 1][-1]
        if len(new[step[1] - 1]) > 0:
            if new[step[1] - 1][-1] != color:
                view.print_text("Wrong step, can't move color", 'critical')
                continue
        for i in range(len(new)):
            if i == step[0] - 1:
                new[i] = new[i][:-1]
            elif i == step[1] - 1:
                new[i] += color
        for i in range(len(flasks)):
            flasks[i] = new[i] + ' ' * (COLORS - len(new[i]))
        last_step = 0 if steps == {} else max(steps.keys())
        steps[last_step + 1] = [f'{step[0]} -> {step[1]}', new]
        view.show_flasks(flasks)
        if game_over(flasks):
            view.print_text('Game completed! You win!', 'ok')
            break


def game_over(flasks: list) -> bool:
    for flask in flasks:
        if flask != '':
            if len(flask.replace(flask[0], '')) > 0 or len(flask) < COLORS:
                break
    else:
        return True
    return False


def solve(num: str, **flasks):
    flasks[num].append(EMPTY_FLASK)
    flasks[num].append(EMPTY_FLASK)
    view.show_flasks(flasks[num])
    flasks[num] = list(i.strip() for i in flasks[num])
    _, steps, __, status = solving(flasks[num], {}, [], 'In')
    if status == 'Ok':
        view.show_steps(steps)
        loader.save_steps(steps, flasks[num], int(num))
    else:
        view.print_text('Cannot be resolved!', 'critical')


def solving(flasks: list, steps: dict, cases: list, status: str) -> (list, dict, list, str):
    if game_over(flasks):
        return flasks, steps, cases, 'Ok'

    for i in range(len(flasks)):
        flask_from = flasks[i]
        if flask_from != '':
            color = flask_from[-1]
            # check one color in two flasks
            if len(flask_from.replace(color, '')) == 0 and len(flask_from) < COLORS:
                for j in range(len(flasks)):
                    flask_to = flasks[j]
                    if j != i and flask_to != '' and len(flask_to.replace(color, '')) == 0:
                        new = list()
                        for k in range(len(flasks)):
                            if k == i:
                                new.append('')
                            elif k == j:
                                new.append(color * (len(flask_from) + len(flask_to)))
                            else:
                                new.append(flasks[k])
                        if new in cases:
                            continue
                        else:
                            last_step = 0 if steps == {} else max(steps.keys())
                            steps[last_step + 1] = [f'{i + 1} -> {j + 1}', new]
                            cases.append(new)
                            new, steps, cases, status = solving(new, steps, cases, 'In')
                            if status == 'Ok':
                                return new, steps, cases, 'Ok'
            # check full stack
            else:
                part = ''
                for k in range(len(flask_from) - 1, 0, -1):
                    if flask_from[k] == color:
                        part += color
                    else:
                        break
                for j in range(len(flasks)):
                    flask_to = flasks[j]
                    if j != i and flask_to != '' and len(flask_to.replace(color, '')) == 0 \
                            and len(flask_to) + len(part) == COLORS:
                        new = list()
                        for k in range(len(flasks)):
                            if k == i:
                                new.append(flask_from[:-len(part)])
                            elif k == j:
                                new.append(color * COLORS)
                            else:
                                new.append(flasks[k])
                        if new in cases:
                            continue
                        else:
                            last_step = 0 if steps == {} else max(steps.keys())
                            steps[last_step + 1] = [f'{i + 1} -> {j + 1}', new]
                            cases.append(new)
                            new, steps, cases, status = solving(new, steps, cases, 'In')
                            if status == 'Ok':
                                return new, steps, cases, 'Ok'

    # check other cases
    for i in range(len(flasks)):
        flask_from = flasks[i]
        if flask_from == '' or len(flask_from.replace(flask_from[0], '')) == 0 and len(flask_from) == COLORS:
            continue
        color = flask_from[-1]
        for j in range(len(flasks)):
            if j != i:
                flask_to = flasks[j]
                if flask_to == '' and len(flask_from.replace(flask_from[0], '')) == 0:
                    continue
                if flask_to == '' or flask_to[-1] == color and len(flask_to) < COLORS:
                    new = list()
                    for k in range(len(flasks)):
                        if k == i:
                            new.append(flasks[k][:-1])
                        elif k == j:
                            new.append(flasks[k] + color)
                        else:
                            new.append(flasks[k])
                    if new in cases:
                        continue
                    else:
                        last_step = 0 if steps == {} else max(steps.keys())
                        steps[last_step + 1] = [f'{i + 1} -> {j + 1}', new]
                        cases.append(new)
                        new, steps, cases, status = solving(new, steps, cases, 'In')
                        if status == 'Ok':
                            return new, steps, cases, 'Ok'
    if steps:
        del steps[max(steps.keys())]
    return flasks, steps, cases, 'Failed'


def generate_game(num='0', **flasks):
    view.show_colors()


def create_game(num='0', **kwargs):
    num = flask_number()
    symbols = list(chr(i) for i in range(ord('A'), ord('A') + num))
    symbols = ''.join(symbols)
    amount = '0' * num
    flasks = dict()
    flasks['0'] = list()
    view.print_text('Enter flasks:')
    for i in range(num):
        view.print_text(f'{view.color_string(symbols)}\n{amount}')
        flask = input(f'{i + 1}: ').upper()
        if check_flask(flask, symbols):
            if flasks['0']:
                flasks['0'].append(flask)
            else:
                flasks['0'] = [flask]
        while not check_flask(flask, symbols):
            view.print_text('Wrong input', 'critical')
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
    menu(loader.load_menu('create'), '0', **flasks)


def save_flask(num='0', **flasks):
    flask = flasks[num].copy()
    while EMPTY_FLASK in flask:
        flask.remove(EMPTY_FLASK)
    loader.save_flask(flask)


def check_flask(flask: str, symbols: str) -> int:
    if len(flask) != COLORS:
        return 0
    for char in flask:
        if char not in symbols:
            return 0
    return 1


def load_flask(num='z', **kwargs):
    flasks = loader.load_flasks()
    view.print_text(f'Total flasks: {len(flasks)}')
    flask = None
    while flask is None:
        num = input('Enter flask number: ')
        flask = flasks.get(num, None)
        if flask is None:
            view.print_text('Wrong number', 'critical')
    view.show_flasks(flasks[num])
    if flasks[num][-1] == 'test':
        flasks[num] = flasks[num][:-1]
    menu(loader.load_menu('load'), num, **flasks)


def flask_number() -> int:
    num = 'a'
    flask = 0
    while flask < 4 or flask > 15:
        while not num.isdigit():
            num = input('Number of flasks (4 - 15): ')
            if not num.isdigit():
                view.print_text('Please enter number of flasks', 'warning')
        flask = int(num)
        if 16 > flask > 3:
            break
        view.print_text('Wrong number of flask!', 'critical')
        num = 'a'
    return flask


def menu(menu_items: list, num='0', **kwargs):
    while True:
        for i in range(len(menu_items)):
            if i == len(menu_items) - 1:
                view.print_text(f'0 - {menu_items[i][0]}')
            else:
                view.print_text(f'{i + 1} - {menu_items[i][0]}')
        item = input('Your choice: ')
        if not item.isdigit():
            view.print_text('Please enter number from the list', 'warning')
        elif 0 < int(item) < len(menu_items):
            func = menu_items[int(item) - 1][1]
            if func == 'dummy':
                view.print_text('Under construction', 'warning')
            else:
                func = eval(func)
                func(num, **kwargs)
        elif item == '0':
            break
        else:
            view.print_text('Wrong number', 'critical')
        view.print_text('')


def main_menu():
    menu(loader.load_menu('main'))


if __name__ == '__main__':
    main_menu()
