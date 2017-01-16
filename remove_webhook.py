import telebot

import conf

bot = telebot.TeleBot(conf.token)

bot.remove_webhook()
