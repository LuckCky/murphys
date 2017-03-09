# -*- coding: utf-8 -*-

# Shelve database file name
storage_name = "messages"

# Your own chat id. Ask https://telegram.me/my_id_bot to tell you yours
my_id = ''

# cherrypy server params
webhook_listen = '0.0.0.0'

post_url = 'https://serene-tundra-30217.herokuapp.com/'

# phrases for bot
welcome = ('Привет! Я гороскоп-бот Мерфи. Даю прогноз на день текущий по '
           'законам Мерфи. Команда /horoscope для выдачи гороскопа и /change '
           'для смены знака зодиака')
prediction = '. Cегодня ваш день будет определять {0}, который гласит: {1}'
ask_date = 'Пожалуйста, напишите дату своего рождения в формате ДД/ММ'
wrong_date = 'Вы ошиблись с датой. Пожалуйста, перепроверьте'
confused = ('Что-то я вас не понимаю, но понимаю команды /horoscope для выдачи '
            'гороскопа и /change для смены знака зодиака')
