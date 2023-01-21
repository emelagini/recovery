from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update, ReplyKeyboardMarkup,ReplyKeyboardRemove
import pymorphy2

morph = pymorphy2.MorphAnalyzer()
GO = "Вперед" # то, что написано на кнопке
BEGIN,GAME = 1,2 # 1,2 шаг разговора


def start(update: Update, context: CallbackContext):
    button = [[GO]]
    keyboard = ReplyKeyboardMarkup(button, resize_keyboard=True,
                                   one_time_keyboard=True,
                                   input_field_placeholder='Нажми на кнопку')
    update.message.reply_text(
        f"""Ты любишь придумывать сказки? 
        Я очень люблю. Ты знаешь сказку как посадил дед репку?
        А кто помогал деду репку тянуть? Чтобы начать, нажми на кнопку {GO}!""" , 
        reply_markup=keyboard)
    return BEGIN # переход к следующему шагу

def begin(update: Update, context: CallbackContext):
    heroes = [['дедку'], ['дедка', "репку"]] 
    update.message.reply_text('Посадил дед репку.Выросло ренка большая пребольшая.Стал дед репку из земли тянуть.Тянет потянет-вытянуть не может.Кого позвал дед')
    reply_markup=ReplyKeyboardRemove()
    return GAME

def game (update: Update, context: CallbackContext):
    text = update.message.text
    text = morph.parse(text)[0]
    nomn = text.inflect({'nomn'}).word # И.п
    accs = text.inflect({'accs'}).word # В.п
    update.message.reply_text(f'{nomn},{accs}')


def end(update: Update, context: CallbackContext):
    update.message.reply_text('Значит, ты выбрал конец')
    return ConversationHandler.END

