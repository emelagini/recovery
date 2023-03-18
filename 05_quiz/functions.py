import csv
from telegram.ext import CallbackContext, ConversationHandler
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
import random

GO = 'Поехали'
GAME = 1
OUESTIONS_ON_ROUND = 2

def start(update: Update, context: CallbackContext):
    mark_up = [[GO]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=f'Нажми на кнопку "{GO}", поиграем!'
    )
    # update.message.reply_sticker(START_STICKER)
    update.message.reply_text(
        'Добро пожаловать в викторину! Выбирайте правильный ответ')
    update.message.reply_text(
        f'Чтобы начать, нажми на "{GO}"', reply_markup=keyboard)
    questions = read_csv() # берем все вопросы
    random.shuffle(questions)
    questions = questions[OUESTIONS_ON_ROUND:]#срез
    context.user_data['вопросы'] = questions
    return GAME


def game(update: Update, context: CallbackContext):
    questions = context.user_data['вопросы']#берём из рюкзака вопросы
    answers = questions.pop()#достаём последний вопрос из списка
    questions_text = answers.pop(0)#взяли текст вопроса
    right_answers = answers[0]# первый ответ - правильный
    random.shuffle(answers)# перемешиваем 
    mark_up = [answers[2:],answers[:2]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True  
    )
    update.message.reply_text(questions_text, reply_markup=keyboard)
    user_answer = update.message.text
    if user_answer == right_answers:
        update.message.reply_photo("https://www.meme-arsenal.com/memes/9e394124c3c8d3718bbc3d565ddd436e.jpg")
    elif user_answer  == GO:
        pass
    else:
        update.message.reply_photo("https://www.google.com/url?sa=i&url=http%3A%2F%2Frisovach.ru%2Fmemy%2Fvy-samoe-slaboe-zveno_346838%2Fall%2F27&psig=AOvVaw0JNrFJ94SYoKUWqQqiYJWD&ust=1679243311365000&source=images&cd=vfe&ved=0CA0QjRxqFwoTCJjQ7Zjz5f0CFQAAAAAdAAAAABAD")
    return ConversationHandler.END

def end(update: Update, context: CallbackContext):  # точка выхода
    name = context.user_data['имя']
    update.message.reply_text(f"Значит, ты выбрал конец, {name}. Если хотите начать заново, нажмите /start")
    return ConversationHandler.END


def read_csv():
    with open('05_quiz\вопросы.csv', 'r', encoding='utf-8') as file:
        quest = list(csv.reader(file, delimiter='|'))
        return quest

    


def write_csv():
    with open('05_quiz\вопросы.csv', 'a', encoding='utf-8') as file:
        worker = csv.writer(file, delimiter='|',lineterminator='\n')  # \n - это перенос
        worker.writerow(['Какая столица Татарстана?',
                        'Казань', 'Астана', 'Елабуга', 'Челны'])