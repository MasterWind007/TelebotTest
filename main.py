#import argparse
import charbot as cb


with open(f'Comon\Res\Key') as key:  
    tb_key = key.read() # тут должен быть ключ, но  я его не дам )))

chat = cb.ChatBot(tb_key)


@chat.bot.message_handler(content_types=['photo', 'document', 'audio', 'video'])  #обработчик получаемого контента
def exec(call):
    if chat.auth == True:
        chat.handler_file(call)
    else: 
        chat.del_last_msg(call)
        chat.bot.send_message(call.chat.id, chat.rand_ansv(chat.chat_logon['acc_no']))         


@chat.bot.message_handler() #Отправка меню
def exec(message):
    if message.text=='/start'     : chat.autorization(message); return 
    if chat.auth == True:
        if message.text=='/menu'    : chat.main_menu(message) # Вызов главного меню
        elif message.text=='/swchat'  : chat.swchat(message)   # Перенаравление в чат
        elif message.text=='/url'     : chat.url(message)      # Выдача ссылки
        elif message.text=='/ocr'     : pass
        else  : chat.say(message)      # Анализ и обработака текстовых сообщений
    else: 
        chat.bot.send_message(message.chat.id, chat.rand_ansv(chat.chat_logon['acc_no']))         


@chat.bot.callback_query_handler(func=lambda call: True) #обработчик команд кнопок
def exec(call):
    if chat.auth == True:
        chat.cmd_hand_btn(call)
 



if __name__ == '__main__':
    chat.bot.polling(none_stop=True)



