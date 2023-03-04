from telegram.ext import CallbackContext, ConversationHandler
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
import random
import pymorphy2
from stickers import *

morp = pymorphy2.MorphAnalyzer()

NAME,BEGIN, LEVEL, GAME = range(4)#остаётся 1234
GO = "Вперед"
SKIP = "Пропустить"
EASY, MEDIUM, HARD = "Простой", "Средний", "Сложный"


def start(update: Update, context: CallbackContext):
    mark_up = [[GO]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=f'Нажми на кнопку "{GO}", поиграем!'
    )
    update.message.reply_sticker(START_STICER)
    update.message.reply_text(
        'В этой игре компьютер загадывает слово, и говорит тебе, сколько в нем букв')
    update.message.reply_text('Ты говоришь слово из такого же количества букв')
    update.message.reply_text(
        'Если у какой-то из букв твоего совпадает позиция с буквой из загаданного слова - это бык')
    update.message.reply_text(
        'Если просто такая буква есть в слове - это корова')
    update.message.reply_text("Твоя цель - отгадать загаданное слово")
    update.message.reply_text(
        f'Чтобы начать, нажми на "{GO}"', reply_markup=keyboard)
    return NAME


def get_name(update: Update, context: CallbackContext):
    update.message.reply_sticker(NAME_STICER)
    full_name = update.effective_chat.full_name
    mark_up = [[SKIP]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True)
    update.message.reply_text(f"можно называть вас{full_name}? Если нет,то назовите своё имя,иначе - нажмите {SKIP}",reply_markup=keyboard)

    return BEGIN


def begin(update: Update, context: CallbackContext):
    name = update.message.text
    if name == SKIP:
        name = update.effective_chat.full_name
    context.user_data["имя"] = name
    mark_up = [[EASY, MEDIUM, HARD]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=f'{EASY} - 3 буквы, {MEDIUM} - 4 буквы, {HARD} 45- 5 букв'
    )
    update.message.reply_text('Выбери уровень сложности или нажми /end!', reply_markup=keyboard)
    
    
    # если ключа "секретное число" нет в рюкзаке
    # secret_number = random.randint(1000, 9999)
    # context.user_data['секретное число'] = secret_number
    # update.message.reply_text('Я загадал число, отгадай или нажми /end!')
    # создается "секретное число" в рюкзаке
    return LEVEL

def level(update: Update, context: CallbackContext):
    level_storage = update.message.text
    name = context.user_data["имя"]
    if level_storage == EASY:
        with open(f"02_cows_and_bulls/easy.txt",encoding='utf-8') as file:
            words = file.read().split("\n")
    elif level_storage == MEDIUM:
        with open(f"02_cows_and_bulls\medium.txt",encoding='utf-8') as file:
            words = file.read().split("\n")
    elif level_storage == HARD:
        with open(f"02_cows_and_bulls\hard.txt",encoding='utf-8') as file:
            words = file.read().split("\n")
    else:
      update.message.reply_text("Недоступен файл")
    word = random.choice(words) 
    context.user_data["word"] = word
    update.message.reply_text(f"{word},отгадайте моё слово .Количество букв  в нём{len(word)} ")
    return GAME

def game(update: Update, context: CallbackContext):  # callback'
    my_word = update.message.text.lower()
    tag = morph.parse(my_word)[0] #набор грамем(число падеж род и тд)
    secret_word = context.user_data['word']  # достаем из рюкзака

    if len(my_word) != len(secret_word):  # не число
        update.message.reply_text(f"Нужно вводить слова из {len(secret_word)} букв")
        return  # выход из функции
    elif my_word !=tag.normal_form or tag.tag.POS != 'NOUN' or 'DictionaryAnalyzer()' not in str (tag.methods_stack):
        update.message.reply_text(f'Нужно вводить нормальные слова из{len(secret_word)}')
        return  # выход из функции
    cows = 0
    bulls = 0
    for mesto, letter in enumerate(my_word): # проходимся по буквам и её месту слова
        if letter in secret_word: # если буква в секретном слове
            if my_word[mesto] == secret_word[mesto]:# если местоположение букв в моём слове и секретном слове совпадает
                bulls += 1 # добавляем быка
            else: # если местоположение не совпадает
                cows += 1 # добавляем одну корову
    update.message.reply_text(f'В вашем слове {cows} коров и {bulls} быков')
    if bulls == len(secret_word):
        update.message.reply_text('Вы угадали! Вы красавчик.Если хотите начать заново нажмите /start')
        del context.user_data['word']

def end(update: Update, context: CallbackContext):  # точка выхода
    name =  context.user_data["имя"]
    update.message.reply_text(f"Значит, ты выбрал конец, {name}")
    return ConversationHandler.END