#import argparse
import telebot as tb
from telebot import types
import random
from io import BytesIO
import os

bot = tb.TeleBot('6140511617:AAG5Nk3kfedflop46XBKrKWQJFUcH9li7Yo')
mas_hello =   ['Привет.', 'День добрый!', 'Добрый день!', 'Здравствуй!', 'Доброго дня!']
mas_del =     ['Заебок','Норм', 'Пойдет', 'Хорошо', 'Отлично', 'Лучше не бывает!', 'Лучше всех!', 'Как обычно']
mas_nastr =   ['Прекрасное!', 'Замечательное!', 'Рабочее...', 'Вполне сносное...']
mas_noUnd =   ['Не понял тебя ', 'Спроси что ни будь еще...', 'Ты о чем ?', 'Затрудняюсь ответить на это...', 'Акваланг...']
mas_Ok =      ['Ок', 'Хорошо.','Выполняю...' ,'Будет сделано!' ,'Как скажешь...' ,'Понял, сделаю.']
mas_sendf =   ['Лови.', 'Получи распишись.', 'Готово.', 'Файл подготовлен.', 'Вот он...', 'Забирай.', 'То что просил...', 'Вот...']
mas_No =      ['Так не получится.' ,'Это так не работает.' ,'Нет!' ,'Не выйдет!' ,'Не в этот раз.' ,'Не сейчас.' ,'Я это делать не буду!', 'Я не стану этого делать!']
mas_bmenu =   [types.BotCommand("start", "Запуск Бота"), types.BotCommand("menu", "Вызов меню")]
button_list = [types.InlineKeyboardButton("Вызов меню 📖", callback_data='menu'),
               types.InlineKeyboardButton("Мои документы 📄", callback_data='getdoc'),
               types.InlineKeyboardButton(text='Перейти в чат 🪠', switch_inline_query="Telegram"),
               types.InlineKeyboardButton(text='Наш сайт 🧻', web_app=types.WebAppInfo('https://ya.ru')),
               types.InlineKeyboardButton("Мои картинки 🏞", callback_data='mypixlist')]
com_res_path = ['Comon/Res/Audio/', 'Comon/Res/Docs/', 'Comon/Res/Pix/', 'Comon/Res/Video/']
com_tmp_path = ['Comon/temp/Audio/', 'Comon/temp/Docs/', 'Comon/temp/Pix/', 'Comon/temp/Video/']
usr_root_path ='Users/'
usr_part_path = ['/Audio/','/Docs/','/Pix/','/Video/']
say_hwy_list  = ['как ты', 'как сам', 'как дела', 'как жизнь', 'как твои дела','как поживаешь', 'как ты поживаешь', 'все норм', 'все хорошо']
say_hi_list =   ['привет', 'здравствуй', 'здравствуйте', 'доброго дня', 'день добрый', 'здорова', 'здоров', 'утро доброе', 'доброе утро', 'добрый вечер', 'добрый день', 'приветствую']
say_nst_list =  ['как настроение', 'как твое настроение', 'как настрой', 'что с настроением', 'настроение как', 'что с настроем' ]

curr_usr_msg = []

def build_menu(buttons, n_cols,  header_buttons=None, footer_buttons=None): #сборка инлайн клавиатуры 
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu

def list_dir (dir, ext='.txt'): # получает список файлов с указанным расширением из указаной папки 
    content = os.listdir(dir)
    f_list = []
    for file in content:
        if os.path.isfile(os.path.join(dir, file)) and file.endswith(ext):
            f_list.append(file)
    return  f_list     

def rand_ansv(mas_ansv): # выдает рандомный вариант ответа из возможных
    return random.choice(mas_ansv)

def build_smenu(): #показывает меню
    bot.set_my_commands(mas_bmenu)

def get_arg(call_data, cmd): # получить аргумент команды
     cmd +=' ' 
     tab = len(cmd)
     return [call_data.startswith(cmd), call_data[tab:]]

def sendpix(message, fname): # отправить картинку в чат
    pix_path = f'Users/{message.chat.first_name}_{message.chat.last_name}/Pix/'
    pix_path+=fname
    with open(pix_path, 'rb') as img:
        bot.send_photo(message.chat.id, img)

@bot.message_handler(commands=['start']) #Стартовое меню
def main(message):
    build_smenu()
    reply_markup = types.InlineKeyboardMarkup(build_menu(button_list, n_cols=2),row_width=1)
    txt=f'Привет { message.from_user.first_name}!\r\n\r\nЗдесь список команд \r\nкоторые тебе доступны:'
    img = open(f'{com_res_path[2]}M4.png', 'rb')
    bot.send_photo(message.chat.id, img, caption=txt ,reply_markup=reply_markup, parse_mode='HTML' )

# content_type= text, audio, document, photo, sticker, video, video_note,
#  voice, location, contact, new_chat_members, left_chat_member, new_chat_title,
#  new_chat_photo, delete_chat_photo, group_chat_created, supergroup_chat_created,
#  channel_chat_created, migrate_to_chat_id, migrate_from_chat_id, pinned_message,
#  web_app_data.

@bot.message_handler(content_types=['photo', 'document', 'audio', 'video']) #обработчик получаемого контента
def handler_file(message):
    curr_usr_msg = message 
    from pathlib import Path
    if message.content_type == 'photo':
        Path(f'Users/{message.from_user.first_name}_{message.from_user.last_name}/Pix/').mkdir(parents=True, exist_ok=True)
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = f'Users/{message.from_user.first_name}_{message.from_user.last_name}/Pix/{message.chat.id}_' + file_info.file_path.replace('photos/', '')
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
    elif message.content_type == 'document':
        Path(f'Users/{message.from_user.first_name}_{message.from_user.last_name}/Docs/').mkdir(parents=True, exist_ok=True)
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = f'Users/{message.from_user.first_name}_{message.from_user.last_name}/Docs/{message.chat.id}_' + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

@bot.message_handler(commands=['mypixlist']) #Отправка списка фото пользователя
def my_pixlist(message):
    pix_path = f'Users/{message.chat.first_name}_{message.chat.last_name}/Pix'
    pix_list = list_dir(pix_path,'.jpg')
    btn_list = []
    for file_nm in pix_list:
        btn_list.append(types.InlineKeyboardButton(file_nm, callback_data='getpix '+file_nm))
    reply_markup = types.InlineKeyboardMarkup(build_menu(btn_list, n_cols=1),row_width=1)
    # pix_content = 'Список ваших сохраненных картинок:\b\n<b>'
    # for file_nm in pix_list:
    #     pix_content += file_nm+'\b\n'
    # pix_content+= '</b>'    
    bot.send_message(chat_id=message.chat.id, text='Список картинок, как вы просили:\b\n'
                     , parse_mode='HTML',reply_markup=reply_markup)
    

@bot.message_handler(commands=['menu']) #Отправка меню
def send_menu(message):
    build_smenu()
    reply_markup = types.InlineKeyboardMarkup(build_menu(button_list, n_cols=2),row_width=1)
    bot.send_message(chat_id=message.chat.id, text='Список доступных команд:', reply_markup=reply_markup)


@bot.message_handler(commands=['getfile']) #пример отправки файла
def sendfile(message):
    with open('1.txt', 'rb') as tmp:
        obj = BytesIO(tmp.read())
        obj.name = '1.txt'
        bot.send_document(message.from_user.id, document=obj, caption=rand_ansv(mas_sendf))

@bot.message_handler(commands = ['swchat']) #пример перенаравления в чат
def swchat(message):
    markup = types.InlineKeyboardMarkup()
    switch_button = types.InlineKeyboardButton(text='Жми сюда!', switch_inline_query="Telegram")
    markup.add(switch_button)
    bot.send_message(message.chat.id, "Перейти в наш чат", reply_markup = markup)

@bot.message_handler(commands = ['url']) #Выдача ссылки
def url(message):
    # markup = types.InlineKeyboardMarkup()
    # btn_my_site= types.InlineKeyboardButton(text='Наш сайт', url='https://ya.ru')
    # markup.add(btn_my_site)
    txt = "Вот необходимые вам ссылки:\b\n\
 <a href='https://yndex.ru/'>Яндекс</a>\b\n\
 <a href='https://coogle.com/'>Google</a>"
    bot.send_message(message.chat.id, text=txt, parse_mode="HTML")#, reply_markup = markup)    


@bot.message_handler() # Анализ и обработака текстовых сообщений
def info(message):
    mess = message.text.lower() 
    for i in say_hwy_list:
        if mess.startswith(i):
            bot.send_message(message.chat.id, rand_ansv(mas_del))
            return
    for i in say_hi_list:
        if mess.startswith(i):
            bot.send_message(message.chat.id, rand_ansv(mas_hello))
            return
    for i in say_nst_list:
        if mess.startswith(i):
            bot.send_message(message.chat.id, rand_ansv(mas_nastr))
            return
        else:
            bot.reply_to(message, rand_ansv(mas_noUnd))
            return

       
@bot.callback_query_handler(func=lambda call: True) #обработчик команд 
def commandshandlebtn(call):
    mess = call.data
    message = call.message
    if   mess == "mypixlist": my_pixlist(message)
    elif get_arg(mess, "getpix")[0]: sendpix(message, get_arg(mess, "getpix")[1])
    elif mess == 'getdoc': sendfile(message)
    elif mess == 'menu': send_menu(message)
    # bot.answer_callback_query(call.id, show_alert=True, text="вызвано меню")


if __name__ == '__main__':
    bot.polling(none_stop=True)



