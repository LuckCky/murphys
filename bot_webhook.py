import time
import cherrypy

import telebot

import conf

from dbhelper import get_user_sign
from prediction import read_prediction
from sign_define import parse_date, check_date, sign_define


WEBHOOK_PORT = conf.webhook_port
WEBHOOK_LISTEN = conf.webhook_listen

# WEBHOOK_SSL_CERT = conf.webhook_ssl_cert
# WEBHOOK_SSL_PRIV = conf.webhook_ssl_priv

WEBHOOK_URL_BASE = conf.post_url
WEBHOOK_URL_PATH = "/{}/".format(conf.token)

bot = telebot.TeleBot(conf.token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome = 'Привет! Я гороскоп-бот Мерфи. Даю прогноз на день текущий по законам Мерфи. ' \
          'Команды /гороскоп или /horoscope для выдачи гороскопа и ' \
          '/change для смены знака зодиака'
    bot.reply_to(message, welcome)


@bot.message_handler(commands=['гороскоп', 'horoscope', 'horrorscope'])
def send_horoscope(message):
    sign = get_user_sign(message.from_user.id)
    if sign:
        prediction = read_prediction(sign)
        reply = sign[0] + '. Cегодня ваш день будет определять {0}, который гласит: {1}'.format(prediction[0],
                                                                                                prediction[1])
        # else:
        #     reply = 'Пожалуйста, напишите дату своего рождения в формате ДД/ММ'# или ДД.ММ'
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


# class WebhookServer(object):
#     @cherrypy.expose
#     def index(self):
#         if 'content-length' in cherrypy.request.headers and \
#                         'content-type' in cherrypy.request.headers and \
#                         cherrypy.request.headers['content-type'] == 'application/json':
#             length = int(cherrypy.request.headers['content-length'])
#             json_string = cherrypy.request.body.read(length).decode("utf-8")
#             update = telebot.types.Update.de_json(json_string)
#             bot.process_new_updates([update])
#             return ''
#         else:
#             raise cherrypy.HTTPError(403)


if __name__ == "__main__":
    bot.remove_webhook()
    time.sleep(3)
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

    # cherrypy.config.update({
    #     'engine.autoreload.on': False,
    #     'server.socket_host': WEBHOOK_LISTEN,
        # 'server.socket_port': WEBHOOK_PORT,
        # 'server.ssl_module': 'builtin',
        # 'server.ssl_certificate': WEBHOOK_SSL_CERT,
        # 'server.ssl_private_key': WEBHOOK_SSL_PRIV
    # })

    # RUN SERVER, RUN!
    # cherrypy.tree.mount(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})

    cherrypy.engine.start()
    cherrypy.engine.block()
    # bot.polling()

