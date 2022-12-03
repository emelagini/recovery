# По кругу стоят n человек.
# Ведущий посчитал m человек по кругу, начиная с первого.
# При этом каждый из тех, кто участвовал в этом счете, получил по одной монете,
# остальные получили по две монеты. Далее человек, на котором остановился счет,
# отдает все свои монеты следующему по счету человеку, а сам выбывает из круга.
# Процесс продолжается с места остановки аналогичным образом до последнего человека в круге.
# Составьте алгоритм, который проводит эту игру.
# Если хотите делать паузы, то импортируйте библиотеку time и используйте оттуда функцию sleep.
# Определите номер этого человека и количество монет, которые оказались у него в конце игры.

from typing import Optional, List
import time
import random


def print_log(text):
    with open('journal.log', 'a', encoding='utf-8') as file:
        print(text)
        file.write(f'{text}\n')


def give_int(input_string: str,
             min_num: Optional[int] = None,
             max_num: Optional[int] = None) -> int:
    """
    Выпытывает у пользователя число

    Args:
        input_string - предложение ввода
    Returns:
        int - число
    """
    while True:
        try:
            num = int(input(input_string))
            print_log(f'Введено {num}')
            if min_num and num < min_num:
                print(f'Введите больше {min_num}')
                continue
            if max_num and num > max_num:
                print(f'Введите больше, чем {max_num}')
                continue
            return num
        except ValueError:
            print('Вы ввели не число')


def get_people_money_lists():
    people_count = give_int(
        'Сколько людей всего в кругу?\n', min_num=1, max_num=10)
    all_people_list = []
    all_money_list = []
    for i in range(people_count):
        all_people_list.append(i)
        all_money_list.append(0)
    return all_people_list, all_money_list


def show_results(people_list: List[int], money_list: List[int]):
    print_log('Распределение монеток следующее: ')
    for i in range(len(people_list)):
        print_log(f'У человека под номером {people_list[i]} - {money_list[i]} монет')


def game(people_list: List[int], money_list: List[int]):
    print_log('Ведущий делает выбор...')
    time.sleep(1)
    count = random.randint(0, len(people_list) - 1)
    print_log(f'Ведущий выбрал {count}!')
    time.sleep(1)
    for person in range(len(people_list)):
        if person < count:
            money_list[person] += 1
        elif person == count:
            next_person = (person + 1) % len(people_list)
            print_log(
                f'Счастливец {people_list[next_person]}! У тебя было {money_list[next_person] + 1}, а станет на {money_list[person]} больше!')
            time.sleep(1)
            money_list[next_person] += money_list[person] + 1
        else:
            money_list[person] += 2

    print_log(f'Выбыл человек под номером {people_list[count]}')
    time.sleep(1)

    people_list.remove(people_list[count])
    money_list.remove(money_list[count])
    people_list = people_list[count:] + people_list[:count]
    money_list = money_list[count:] + money_list[:count]
    return people_list, money_list


def run_until_game_stop(people_list: List[int]):
    stopper = input(f'Продолжаем c человека под номером {people_list[0]}?')
    print_log(f'Продолжаем c человека под номером {people_list[0]}?')
    if stopper in "нет, хватит, стоп, прекрати".split(', '):
        return False
    return True


all_people, all_money = get_people_money_lists()
stop_word = ""
while len(all_people) != 1 and run_until_game_stop(all_people):
    all_people, all_money = game(all_people, all_money)
    show_results(all_people, all_money)
    input('Для продолжения нажмите Enter')

if len(all_people) == 1:
    print_log(f'Победителем вышел {all_people.pop()}')
else:
    print_log('Игра прекращена до объявления победителя')
