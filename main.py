#import argparse
import charbot as cb
   
TB_KEY = '6140511617:AAG5Nk3kfedflop46XBKrKWQJFUcH9li7Yo' # тут должен быть ключ, но  я его не дам )))

chat = cb.ChatBot(TB_KEY)

@chat.bot.message_handler(content_types=['photo', 'document', 'audio', 'video'])  #обработчик получаемого контента
def exec(call):
    chat.cmd_hand_btn(call)

@chat.bot.message_handler() #Отправка меню
def exec(message):
    print(message)
    if message.text=='/start'     : chat.autorization(message)
    elif message.text=='/menu'    : chat.main_menu(message) # Вызов главного меню
    elif message.text=='/swchat'  : chat.swchat(message)   # Перенаравление в чат
    elif message.text=='/url'     : chat.url(message)      # Выдача ссылки
    else  : chat.say(message)      # Анализ и обработака текстовых сообщений     

@chat.bot.callback_query_handler(func=lambda call: True) #обработчик команд кнопок
def exec(call):
    chat.cmd_hand_btn(call)


if __name__ == '__main__':
    chat.bot.polling(none_stop=True)



