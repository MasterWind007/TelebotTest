import argparse
import telebot as tb
from telebot import types
import random
from io import BytesIO

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
               types.InlineKeyboardButton("Получить файл 📄", callback_data='getdoc'),
               types.InlineKeyboardButton(text='Чат 🪠', switch_inline_query="Telegram"),
               types.InlineKeyboardButton(text='Наш сайт 🧻', web_app=types.WebAppInfo('https://ya.ru')),
               types.InlineKeyboardButton("Получить картинку 🏞", callback_data='getpix')]
com_res_path = ['Comon/Res/Audio/', 'Comon/Res/Docs/', 'Comon/Res/Pix/', 'Comon/Res/Video/']
com_tmp_path = ['Comon/temp/Audio/', 'Comon/temp/Docs/', 'Comon/temp/Pix/', 'Comon/temp/Video/']
usr_root_path ='Users/'
usr_part_path = ['/Audio/','/Docs/','/Pix/','/Video/']

def build_menu(buttons, n_cols,  header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def rand_ansv(mas_ansv):
    return random.choice(mas_ansv)

def build_smenu():
    bot.set_my_commands(mas_bmenu)

@bot.message_handler(commands=['start'])
def main(message):
    build_smenu()
    reply_markup = types.InlineKeyboardMarkup(build_menu(button_list, n_cols=2),row_width=1)
    txt=f'Привет { message.from_user.first_name},  вот список команд которые тебе доступны:'
    img = open(f'{com_res_path[2]}Photo.png', 'rb')
    bot.send_photo(message.chat.id, img, caption=txt ,reply_markup=reply_markup)
    # bot.send_message(chat_id=message.chat.id, text=f'Привет { message.from_user.first_name},  вот список команд которые тебе доступны:', reply_markup=reply_markup )

# content_type= text, audio, document, photo, sticker, video, video_note,
#  voice, location, contact, new_chat_members, left_chat_member, new_chat_title,
#  new_chat_photo, delete_chat_photo, group_chat_created, supergroup_chat_created,
#  channel_chat_created, migrate_to_chat_id, migrate_from_chat_id, pinned_message,
#  web_app_data.

@bot.message_handler(content_types=['photo', 'document', 'audio', 'video'])
def handler_file(message):
    from pathlib import Path
    if message.content_type == 'photo':
        Path(f'Users/Pix/{message.from_user.first_name}_{message.from_user.last_name}/').mkdir(parents=True, exist_ok=True)
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = f'Users/{message.from_user.first_name}_{message.from_user.last_name}/{message.chat.id}_' + file_info.file_path.replace('photos/', '')
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
    elif message.content_type == 'document':
        Path(f'Users/Docs/{message.from_user.first_name}_{message.from_user.last_name}/').mkdir(parents=True, exist_ok=True)
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = f'Users/{message.from_user.first_name}_{message.from_user.last_name}/{message.chat.id}_' + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

@bot.message_handler(commands=['getpix'])
def send_pix(message):
    with open('Photo.PNG', 'rb') as img:
        bot.send_photo(message.chat.id, img)
    

@bot.message_handler(commands=['menu'])
def send_menu(message):
    build_smenu()
    reply_markup = types.InlineKeyboardMarkup(build_menu(button_list, n_cols=2),row_width=1)
    bot.send_message(chat_id=message.chat.id, text='Список команд:', reply_markup=reply_markup)


@bot.message_handler(commands=['getfile'])
def sendfile(message):
    with open('1.txt', 'rb') as tmp:
        obj = BytesIO(tmp.read())
        obj.name = '1.txt'
        bot.send_document(message.from_user.id, document=obj, caption=rand_ansv(mas_sendf))

@bot.message_handler(commands = ['swchat'])
def swchat(message):
    markup = types.InlineKeyboardMarkup()
    switch_button = types.InlineKeyboardButton(text='Жми сюда!', switch_inline_query="Telegram")
    markup.add(switch_button)
    bot.send_message(message.chat.id, "Перейти в наш чат", reply_markup = markup)

@bot.message_handler(commands = ['url'])
def url(message):
    markup = types.InlineKeyboardMarkup()
    btn_my_site= types.InlineKeyboardButton(text='Наш сайт', url='https://ya.ru')
    markup.add(btn_my_site)
    bot.send_message(message.chat.id, "Нажми на кнопку и перейди на наш сайт.", reply_markup = markup)    


@bot.message_handler()
def info(message):
    mess = message.text.lower() 
    if mess.startswith("как ты"):
        bot.send_message(message.chat.id, rand_ansv(mas_del))
    elif mess.startswith("привет"):
        bot.send_message(message.chat.id, rand_ansv(mas_hello))
    elif mess.startswith("как дела"):
        bot.send_message(message.chat.id, rand_ansv(mas_del))
    elif mess.startswith("как настроение"):
        bot.send_message(message.chat.id, rand_ansv(mas_nastr))
    else:
        bot.reply_to(message, rand_ansv(mas_noUnd))
       
@bot.callback_query_handler(func=lambda call: True)
def commandshandlebtn(call):
    mess = call.data
    message = call.message
    if   mess == "getpix": send_pix(message)
    elif mess == 'getdoc': sendfile(message)
    elif mess == 'menu': send_menu(message)
        # bot.answer_callback_query(call.id, show_alert=True, text="вызвано меню")


if __name__ == '__main__':
    bot.polling(none_stop=True)



