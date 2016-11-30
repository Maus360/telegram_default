from telegram.ext import ConversationHandler, Filters
from telegram.ext import MessageHandler
from telegram.ext import RegexHandler
from telegram.ext import Updater, CommandHandler
import telegram

import logging
from selt import query


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

custom_keyboard = [['Неделя', 'День'],
                   ['Корпус', 'Время'],
                   ['Отправить'],]
markup = telegram.ReplyKeyboardMarkup(custom_keyboard)

CHOOSING,REPLY=1,2

def facts_to_str(user_data):
    facts = list()
    for key, value in user_data.items():
        facts.append('%s - %s' % (key, value))
    return "\n".join(facts)

def start(bot, update):
    update.message.reply_text('Поиск свободных аудиторий в БГУИРе\nЗаполните 4 поля',reply_markup=markup)
    return CHOOSING

def week_choice(bot,update,user_data):
    user_data['choice']=update.message.text
    ch_markup=telegram.ReplyKeyboardMarkup([['1','2','3','4']])
    update.message.reply_text('Неделя: ',reply_markup=ch_markup)
    return REPLY

def day_choice(bot,update,user_data):
    user_data['choice']=update.message.text
    ch_markup=telegram.ReplyKeyboardMarkup([['1','2','3'],
                                    ['4','5','6'],])
    update.message.reply_text('Выберите день: ',reply_markup=ch_markup)
    return REPLY

def corp_choice(bot,update,user_data):
    user_data['choice']=update.message.text
    ch_markup=telegram.ReplyKeyboardMarkup([['1','2','3'],
                                    ['4','5','7'],])
    update.message.reply_text('Выберите корпус: ',reply_markup=ch_markup)
    return REPLY

def time_choice(bot,update,user_data):
    user_data['choice']=update.message.text
    ch_markup=telegram.ReplyKeyboardMarkup([['08:00-09:35','09:45-11:20',"11:40-13:15"],
                                    ['13:25-15:00','15:20-16:55','17:05-18:40'],])
    update.message.reply_text('Время: ',reply_markup=ch_markup)
    return REPLY

def received_information(bot,update,user_data):
    category=user_data['choice']
    user_data[category]=update.message.text
    del user_data['choice']
    update.message.reply_text(facts_to_str(user_data),reply_markup=markup)
    return CHOOSING

def done(bot,update,user_data):
    valid=query(user_data['Неделя'],user_data['День'],user_data['Корпус'],user_data['Время'])
    response='Свободны:'+',  '.join(valid)
    update.message.reply_text(response,reply_markup = telegram.ReplyKeyboardHide())
    user_data.clear()
    return ConversationHandler.END

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    updater = Updater('192668401:AAEB7pGo4LTmGpx3-wjNNmIBBcKsqDDsBf8')
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [RegexHandler('^Неделя$',
                                    week_choice,
                                    pass_user_data=True),
                       RegexHandler('^День$',
                                    day_choice,
                                    pass_user_data=True),

                       RegexHandler('^Корпус$',
                                    corp_choice,
                                    pass_user_data=True),

                       RegexHandler('^Время$',
                                    time_choice,
                                    pass_user_data=True),
                       ],

            REPLY: [MessageHandler(Filters.text,
                                          received_information,
                                          pass_user_data=True),
                           ],
        },

        fallbacks=[RegexHandler('^Отправить$', done, pass_user_data=True)]
    )
    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    main()
