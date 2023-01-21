from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update, ReplyKeyboardMarkup

GO = "Вперед" # то, что написано на кнопке
BEGIN = 1 # 1 шаг разговора

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

def end(update: Update, context: CallbackContext):
    update.message.reply_text('Значит, ты выбрал конец')
    return ConversationHandler.END

def begin(update: Update, context: CallbackContext):
    update.message.reply_text('Первый шаг диалога')
    return ConversationHandler.END