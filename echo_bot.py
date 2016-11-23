import telebot

from conf import token
from dbhelper import get_user_sign
from prediction import read_prediction
from sign_define import parse_date, check_date, sign_define

bot = telebot.TeleBot(token)

welcome = 'Привет! Я гороскоп-бот Мерфи. Даю прогноз на день текущий по законам Мерфи. ' \
          'Команды /гороскоп или /horoscope для выдачи гороскопа и ' \
          '/change для смены знака зодиака'

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome = welcome
    bot.reply_to(message, welcome)

@bot.message_handler(commands=['гороскоп', 'horoscope', 'horrorscope'])
def send_horoscope(message):
    sign = get_user_sign(message.from_user.id)
    if sign:
        prediction = read_prediction(sign)
        reply = sign[0] + '. Cегодня ваш день будет определять {0}'.format(prediction[0]) \
                + ', который гласит: {0}'.format(prediction[1])
    else:
        reply = 'Пожалуйста, напишите дату своего рождения в формате ДД/ММ'# или ДД.ММ'
    bot.reply_to(message, reply)

@bot.message_handler(regexp='ороскоп | oroscope')
def send_horoscope(message):
    sign = get_user_sign(message.from_user.id)
    if sign:
        prediction = read_prediction(sign)
        reply = sign[0] + '. Cегодня ваш день будет определять {0}'.format(prediction[0]) \
                + ', который гласит: {0}'.format(prediction[1])
    else:
        reply = 'Пожалуйста, напишите дату своего рождения в формате ДД/ММ'# или ДД.ММ'
    bot.reply_to(message, reply)

@bot.message_handler(regexp='[0-9][0-9]/[0-9][0-9]')# | [0-9][0-9].[0-9][0-9] | [0-9][0-9],[0-9][0-9]')
def send_day(message):
    day, month = parse_date(message.text)
    if check_date(day, month):
        sign = sign_define(message.from_user.id, day, month)
        try:
            prediction = read_prediction(sign)
            reply = sign + '. Cегодня ваш день будет определять {0}'.format(prediction[0]) \
                + ', который гласит: {0}'.format(prediction[1])
        except TypeError:
            reply = 'Я запутался, пожалуйста, повторите команду'
    else:
        reply = 'Вы ошиблись с датой. Пожалуйста, перепроверьте'
    bot.reply_to(message, reply)

@bot.message_handler(commands=['change'])
def change_sign(message):
    reply = 'Пожалуйста, напишите дату своего рождения в формате ДД/ММ'# или ДД.ММ'
    bot.reply_to(message, reply)

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()
