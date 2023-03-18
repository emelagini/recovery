from config import TOKEN
from telegram.ext import (
    Updater,
    Filters,
    MessageHandler,
    ConversationHandler,
    CommandHandler
    )

from functions import *


dialog_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        GAME: [MessageHandler(Filters.text & ~Filters.command,game)]
    },
    fallbacks=[CommandHandler('end',end)]
    
)

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(dialog_handler)



print('Приложение запущено')
updater.start_polling()
updater.idle()  # ctrl + C
