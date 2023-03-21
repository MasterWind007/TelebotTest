#import argparse
import charbot as cb
   
TB_KEY = '6140511617:AAG5Nk3kfedflop46XBKrKWQJFUcH9li7Yo'

chat = cb.ChatBot(TB_KEY)

@chat.bot.message_handler(content_types=['photo', 'document', 'audio', 'video'])  #обработчик получаемого контента
def exec(call):
    chat.cmd_hand_btn(call)

@chat.bot.message_handler(commands=['menu', 'start']) #Отправка меню
def exec(message):
    chat.main_menu(message)

@chat.bot.message_handler(commands=['swchat']) #пример перенаравления в чат
def exec(message):
    chat.swchat(message)

@chat.bot.message_handler(commands = ['url']) #Выдача ссылки
def exec(message):
    chat.url(message)
    
@chat.bot.message_handler() # Анализ и обработака текстовых сообщений
def exec(message):
    chat.say(message)

@chat.bot.callback_query_handler(func=lambda call: True) #обработчик команд кнопок
def exec(call):
    chat.cmd_hand_btn(call)


if __name__ == '__main__':
    chat.bot.polling(none_stop=True)



