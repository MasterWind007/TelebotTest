import telebot as tb
from telebot import types
import random
import ocrmodule
from io import BytesIO
import os
from barcode import BarCode
from gptai import GptChat
from yacloudviz import YandexOCR
from yasprec import YaVoiceToText
from yaspsyn import YaVoiceSyn
from pathlib import Path


ocr_exe_file = [Path('C:/','Program Files','Tesseract-OCR','tesseract.exe'),
                Path('D:/','Program Files','Tesseract-OCR','tesseract.exe')]
ocr_image_file = Path('Comon','Tmp','ocrimg.jpg')
bar_image_file = Path('Comon','Tmp','barcode.jpg')
com_res_path ={'audio': Path('Comon','Res','Audio'), 
               'docs': Path('Comon','Res','Docs'), 
               'pix': Path('Comon','Res','Pix'),
               'video': Path('Comon','Res','Video')}
tmp_path =    {'audio' : Path('Comon','Tmp','Audio'),
               'docs': Path('Comon','Tmp','Docs'),
               'pix': Path('Comon','Tmp','Pix'),
               'video': Path('Comon','Tmp','Video')} 
usr_root_path = Path('Users')
usr_part_path = {'audio':'Audio','docs':'Docs','pix':'Pix','video':'Video'} 
voice_path = Path('speech.ogg')
voice_out_json = Path('audioout.json')
syn_voice_path = Path('syn_voie.ogg')

ocr = YandexOCR()
voice = YaVoiceToText()
voice_syn = YaVoiceSyn(syn_voice_path)

# ocr = ocrmodule.OcrClass(ocr_exe_file[0]) # Инициализация объекта для распознавания текста teseract
gpt = GptChat() #Инициализация объекта работы с GPT4 чат
gpt.get_key()
barcode = BarCode() # Инициализация объекта для работы с штрих и QR кодами

class ChatBot:
    def __init__(self, bt):
        self.auth = False
        self.chat_mode = '' #gpt_keymode , barmode, ocrmode , gpt_voicemode
        self.ocr_image_file = ocr_image_file
        self.bar_image_file = bar_image_file 
        self.bot = tb.TeleBot(bt)

        self.com_res_path   = com_res_path # Пути к общим папкам ресурсов
        self.tmp_path       = tmp_path #Пути к временным папкам документов
        self.usr_root_path  = usr_root_path
        self.usr_part_path  = usr_part_path # Путь к папкам пользователя
        self.voice_path     = voice_path # путь к временному файлу голосового распознавания
        self.voice_out_json = voice_out_json # Путь к выходному файлу с текчтом json

        self.chat_answ     = {'mas_hello' :['Привет.', 'День добрый!', 'Добрый день!', 'Здравствуй!', 'Доброго дня!'],
                              'mas_del'   :['Заебок','Норм', 'Пойдет', 'Хорошо', 'Отлично', 'Лучше не бывает!', 'Лучше всех!', 'Как обычно'],
                              'mas_nastr' :['Прекрасное!', 'Замечательное!', 'Рабочее...', 'Вполне сносное...'],
                              'mas_noUnd' :['Не понял тебя ', 'Спроси что ни будь еще...', 'Ты о чем ?', 'Затрудняюсь ответить на это...', 'Акваланг...'],
                              'mas_Ok'    :['Ок', 'Хорошо.','Выполняю...' ,'Будет сделано!' ,'Как скажешь...' ,'Понял, сделаю.'],
                              'mas_sendf' :['Лови.', 'Получи распишись.', 'Готово.', 'Файл подготовлен.', 'Вот он...', 'Забирай.', 'То что просил...', 'Вот...'],
                              'mas_No'    :['Так не получится.' ,'Это так не работает.' ,'Нет!' ,'Не выйдет!' ,'Не в этот раз.' ,'Не сейчас.' ,'Я это делать не буду!', 'Я не стану этого делать!']
                            }
        self.chat_quest     = { 'say_hwy_list':['как ты', 'как сам', 'как дела', 'как жизнь', 'как твои дела','как поживаешь', 'как ты поживаешь', 'все норм', 'все хорошо'],
                                'say_hi_list'  :['привет', 'здравствуй', 'здравствуйте', 'доброго дня', 'день добрый', 'здорова', 'здоров', 'утро доброе', 'доброе утро', 'добрый вечер', 'добрый день', 'приветствую'],
                                'say_nst_list' :['как настроение', 'как твое настроение', 'как настрой', 'что с настроением', 'настроение как', 'что с настроем' ]
                              }
        self.chat_logon     = { 'acc_no': ['Пожалуйста авторизуйтесь!', 'У Вас нет доступа!', 'Я с Вами не знаком, автроизуйтесь пожалуйста.', 'Не разговариваю с назнакомцами, авторизуйтесь!', 'Вы не авторизованы!'],
                                'acc_yes':['Добро пожаловать!', 'Доступ разрешен!', 'Вы авторизованы!', 'Как Вам удалось угадать пароль ?', 'И снова здравствуйте!'] 
                              }

        self.main_cmd       = [types.BotCommand("start", "Запуск Бота"), types.BotCommand("menu", "Вызов меню")] # Элементы меню команд.
        self.main_btns      = {}
        self.inln_btns      = {'main_btns':[types.InlineKeyboardButton("Вызов меню 📖", callback_data='menu'), # Элементы кнопок инлайн клавиатур
                                # types.InlineKeyboardButton("Мои документы 📄", callback_data='mydoclist'),
                                # types.InlineKeyboardButton("Мои картинки 🏞", callback_data='mypixlist'),
                                types.InlineKeyboardButton("Распознать текст 🏞", callback_data='myocr'),
                                types.InlineKeyboardButton("Распознать Баркод 🪪", callback_data='mybarcode'),
                                types.InlineKeyboardButton(text='Наш сайт 🧻', web_app=types.WebAppInfo('https://ya.ru')),
                                types.InlineKeyboardButton(text='Перейти в чат 🪠', switch_inline_query="Telegram")]
                               }
        

    class CommandArgs:  #класс для хранения параметров кнопки пример команды: /getpix photo.jpg 
        def __init__(self, cd='', cmd=''):
            self.call_data = cd
            self.comm_data = cmd
        
        def is_exist(self, cd='', cmd=''): #  есть ли в данных такая команда
            self.call_data = cd
            self.comm_data = cmd+' '
            return self.call_data.startswith(cmd)#, 
        
        def arg_name(self):    #выделить из команды параметр
            tab = len(self.comm_data)
            return self.call_data[tab:]
        
    def autorization(self, message): # авторизация
            # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            # exit = types.KeyboardButton('Выход')
            # markup.add(exit)
            sent = self.bot.send_message(message.chat.id, 'Введите ключ для входа в систему')
            self.bot.register_next_step_handler( sent, self.login)

    def login(self, message): # Логин
            if message.text == 'Pass':
                self.del_last_msg(message)
                self.bot.send_message(message.chat.id, 'Вы успешно авторизованы!')
                self.welcome(message)
                self.auth = True
            else:
                self.auth = False
                self.del_last_msg(message)
                sent = self.bot.send_message(message.chat.id, 'Неправильный пароль! Прпробуйте еще раз.')
                self.bot.register_next_step_handler(sent, self.login)
 
    def build_menu(self, buttons, n_cols,  header_buttons=None, footer_buttons=None): #сборка инлайн клавиатуры главного меню
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, [header_buttons])
        if footer_buttons:
            menu.append([footer_buttons])
        return menu

    def build_smenu(self): #создает текстовое меню.
        self.bot.set_my_commands(self.main_cmd)

    def list_dir (self, dir, ext=''): # получает список файлов с указанным расширением из указаной папки 
        content = os.listdir(dir)
        f_list = []
        for file in content:
            if os.path.isfile(os.path.join(dir, file)) and file.endswith(ext):
                f_list.append(file)
        return  f_list     

    def rand_ansv(self, mas_ansv): # выдает рандомный вариант ответа из возможных ответов
        return random.choice(mas_ansv)

    def my_pixlist(self, message):#Отправка списка фото пользователя в виде кнопок
        pix_path = f'Users/{message.chat.first_name}_{message.chat.last_name}/Pix'
        pix_list = self.list_dir(pix_path,'.jpg')
        btn_list = []
        for file_nm in pix_list:
            btn_list.append(types.InlineKeyboardButton(file_nm, callback_data='getpix '+file_nm))
        btn_list.append(types.InlineKeyboardButton("Меню. 📖", callback_data='menu'))
        reply_markup = types.InlineKeyboardMarkup(self.build_menu(btn_list, n_cols=1),row_width=1)
        # pix_content = 'Список ваших сохраненных картинок:\n<b>'
        # for file_nm in pix_list:
        #     pix_content += file_nm+'\n'
        # pix_content+= '</b>'    
        txt='Список твоих картинок, как просил:'
        with open(Path(self.com_res_path["pix"],'M1.png'), 'rb') as img:
            self.bot.send_photo(message.chat.id, img, caption=txt ,reply_markup=reply_markup, parse_mode='HTML' )
        
    def my_doclist(self, message): # Отправка списка документов пользователя в виде кнопок
        path = f'Users/{message.chat.first_name}_{message.chat.last_name}/Docs'
        list = self.list_dir(path)
        btn_list = []
        for file_nm in list:
            btn_list.append(types.InlineKeyboardButton(file_nm, callback_data='getdoc '+file_nm))
        btn_list.append(types.InlineKeyboardButton("Меню. 📖", callback_data='menu'))
        reply_markup = types.InlineKeyboardMarkup(self.build_menu(btn_list, n_cols=1),row_width=1)
        txt='Список твоих документов, как просил:'
        with open(Path(self.com_res_path["pix"],'M1.png'), 'rb') as img:
            self.bot.send_photo(message.chat.id, img, caption=txt ,reply_markup=reply_markup, parse_mode='HTML' )

    def sendpix(self, message, fname): # отправить картинку в чат
        btn_list = []
        btn_list.append(types.InlineKeyboardButton("Меню. 📖", callback_data='menu'))
        reply_markup = types.InlineKeyboardMarkup(self.build_menu(btn_list, n_cols=1),row_width=1)
        path = Path(f'Users/{message.chat.first_name}_{message.chat.last_name}/Pix/')
        path = Path(path,fname)
        with open(path, 'rb') as img:
            self.bot.send_photo(message.chat.id, img, caption=self.rand_ansv(self.chat_answ['mas_sendf']),reply_markup=reply_markup)

       

    def sendfile(self, message, fname): # отправить файл в чат
        btn_list = []
        btn_list.append(types.InlineKeyboardButton("Меню. 📖", callback_data='menu'))
        reply_markup = types.InlineKeyboardMarkup(self.build_menu(btn_list, n_cols=1),row_width=1)
        path = f'Users/{message.chat.first_name}_{message.chat.last_name}/Docs/'
        path+=fname
        with open(path, 'rb') as tmp:
            obj = BytesIO(tmp.read())
            obj.name = fname
            self.bot.send_document(message.chat.id, document=obj, caption=self.rand_ansv(self.chat_answ['mas_sendf'],reply_markup=reply_markup))

    def welcome(self, message): # Приветствие
        txt=f'Привет { message.from_user.first_name}!\r\n\r\n\
Я учебный бот,\n\
на котором мой создатель\n\
отрабатывает навыки написания\n\
мне подобных.\n\n\
Мой функционал со временем\n\
будет расширяться, обрастая\n\
новыми интересными возможностями!\n\n\
Список доступных команд, можно\n\
вызвать набрав /menu  или выбрав \n\
эту команду в меню чата.\n\n\
<b>А еще со мной можно просто\n\
болтать на разные темы, так как\n\
я являюсь транслятором чата GPT4</b>' 
        with open(Path(self.com_res_path["pix"],'M4.png'), 'rb') as img:
            self.bot.send_photo(message.chat.id, img, caption=txt , parse_mode='HTML' )

    def main_menu(self, message): # Обработчик команды /start
        reply_markup = types.InlineKeyboardMarkup(self.build_menu(self.inln_btns['main_btns'], n_cols=2),row_width=1)
        self.bot.send_message(chat_id=message.chat.id, text='Список доступных команд:', reply_markup=reply_markup)

    def save_pix_file(self, message, path):
            file_info = self.bot.get_file(message.photo[len(message.photo) - 1].file_id)
            from_chat_file = self.bot.download_file(file_info.file_path)            
            with open(path, 'wb') as new_file:
                new_file.write(from_chat_file)
            self.del_last_msg(message)
            self.bot.send_message(chat_id=message.chat.id, text='...изображение принял!')
    
    def save_doc_file(self, message, path):
            file_info = self.bot.get_file(message.document.file_id)
            downloaded_file = self.bot.download_file(file_info.file_path)
            with open(path, 'wb') as new_file:
                new_file.write(downloaded_file)
            self.del_last_msg(message)
            self.bot.send_message(chat_id=message.chat.id, text='...документ сохранил!')

    def save_voice_file(self, message, path): #Сохраняет на диск голосовое сообщение
            file_info = self.bot.get_file(message.voice.file_id)
            downloaded_file = self.bot.download_file(file_info.file_path)        
            with open(path, 'wb') as new_file:
              new_file.write(downloaded_file)        
                     

    def handler_file(self, message): # Обработчик файлов , присланых пользователем в чат
        if message.content_type == 'photo':
            if self.chat_mode == 'ocrmode':
                path = self.ocr_image_file
                self.save_pix_file(message, path)
                self.bot.send_message(chat_id=message.chat.id, text='Пытаюсь обработать...')
                self.ocr_to_str(message)
                self.chat_mode = ''                    
                return
            elif self.chat_mode =='barmode':
                path = self.bar_image_file
                self.save_pix_file(message, path)
                self.bar_to_str(message)
                self.chat_mode = ''
                return
            elif self.chat_mode == 'gpt_keymode':
                if gpt.new_key(key=message.text):
                    self.chat_mode = ''
                    self.del_last_msg(message)
                    self.bot.send_message(chat_id=message.chat.id, text='Ок')
                    return
                else:
                    self.chat_mode = ''
                    self.del_last_msg(message)
                    self.bot.send_message(chat_id=message.chat.id, text='Ошибка!')
            else:
                file_info = self.bot.get_file(message.photo[len(message.photo) - 1].file_id)
                Path(f'Users/{message.from_user.first_name}_{message.from_user.last_name}/Pix/').mkdir(parents=True, exist_ok=True)
                path = Path(f'Users/{message.from_user.first_name}_{message.from_user.last_name}/Pix/{message.chat.id}_' + file_info.file_path.replace('photos/', ''))
                self.save_pix_file(message, path)
        elif message.content_type == 'document':
            Path(f'Users/{message.from_user.first_name}_{message.from_user.last_name}/Docs/').mkdir(parents=True, exist_ok=True)
            path = Path(f'Users/{message.from_user.first_name}_{message.from_user.last_name}/Docs/' + message.document.file_name)
            self.save_doc_file(self, message, path)
        elif message.content_type == 'voice':
            if self.chat_mode == 'voice_rec':
                Path(f'Users/{message.from_user.first_name}_{message.from_user.last_name}/Voice/').mkdir(parents=True, exist_ok=True)
                path = Path(f'Users/{message.from_user.first_name}_{message.from_user.last_name}/Voice/' + message.voice.file_name)
                self.save_voice_file(message, path)
            else:
                self.save_voice_file(message, self.voice_path)
                text = voice.voice_to_string(self.voice_path, self.voice_out_json)
                self.chat_mode = ''
                self.bot.send_message(message.chat.id, gpt.answer(text))
        elif message.content_type == 'text':
            if self.chat_mode == 'text_syn':
                voice_syn.text_to_voice(message.text)
                self.bot.sendVoice(message.chat.id, syn_voice_path)
                self.chat_mode = ''

  
    def swchat(self, message): # Перейти в другой чат
        markup = types.InlineKeyboardMarkup()
        switch_button = types.InlineKeyboardButton(text='Жми сюда!', switch_inline_query="Telegram")
        markup.add(switch_button)
        self.bot.send_message(message.chat.id, "Перейти в наш чат", reply_markup = markup)

    def url(self, message): #Отправка Url в чат
        # markup = types.InlineKeyboardMarkup()
        # btn_my_site= types.InlineKeyboardButton(text='Наш сайт', url='https://ya.ru')
        # markup.add(btn_my_site)
        txt = "Вот необходимые вам ссылки:\n\
    <a href='https://yndex.ru/'>Яндекс</a>\n\
    <a href='https://coogle.com/'>Google</a>"
        self.bot.send_message(message.chat.id, text=txt, parse_mode="HTML")#, reply_markup = markup)    
    
    def ocr_mode_on(self, message):
        self.chat_mode = 'ocrmode'
        self.bot.send_message(message.chat.id, text='Ожидаю фото или картинку с текстом.')


    def bar_mode_on(self, message):
        self.chat_mode = 'barmode' 
        self.bot.send_message(message.chat.id, text='Ожидаю фото или картинку с баркодом.')
    
    def gptk_mode_on(self, message):
          self.chat_mode = 'gpt_keymode'
          self.bot.send_message(message.chat.id, text='Ожидаю ввода API Key...')
    
    def voice_rec(self, message):
          self.chat_mode ='voice_save' 
          self.bot.send_message(message.chat.id, text='Для записи сообщения нажмите на микрофон.')

    def text_syn (self, message):
          self.chat_mode ='text_syn'
          self.bot.send_message(message.chat.id, text='Напиши или вставь текст, который надо озвучить.') 

    
    def bar_to_str(self, message):
        text  = ''
        path = self.bar_image_file
        img = barcode.img_from_file(path)
        # img = barcode.draw_rect_bars(img)
        for item in barcode.decode(img):
            text += str(item.data,'utf-8') +'\n'
        # self.bot.send_photo(message.chat.id, img , caption= text)
        if text == '':
            self.bot.send_message(message.chat.id, text = 'К сожалению не удалось распознать изображение.')
        self.bot.send_message(message.chat.id, text = text)

    def ocr_to_str(self,message): 
        txt = ocr.image_to_string() #для яндекс
        # txt = ocr.image_to_string(self.ocr_image_file) для tesseract
        self.bot.send_message(message.chat.id, text=txt)
        

    def say(self, message): #     отправка ответа на распространенные вопросы  при отключенном или ошибке GPT чата
        mess = message.text.lower() 
        if not mess.startswith('/'):
            answ = gpt.answer(message.text)
            if answ.startswith('GptErr!'):
                for i in self.chat_quest['say_hwy_list']:
                    if mess.startswith(i):
                        self.bot.send_message(message.chat.id, self.rand_ansv(self.chat_answ['mas_del']))
                        return
                for i in self.chat_quest['say_hi_list']:
                    if mess.startswith(i):
                        self.bot.send_message(message.chat.id, self.rand_ansv(self.chat_answ['mas_hello']))
                        return
                for i in self.chat_quest['say_nst_list']:
                    if mess.startswith(i):
                        self.bot.send_message(message.chat.id, self.rand_ansv(self.chat_answ['mas_nastr']))
                        return
                    else:
                        self.bot.reply_to(message, self.chat_answ['mas_noUnd'])
                        return
            self.bot.send_message(message.chat.id, gpt.answer(message.text))
            return 

            
    def del_last_msg(self, message): #  Удаление последнего сообщения
        self.bot.delete_message(message.chat.id, message.message_id)

    def cmd_hand_btn(self, call): # Обработка комманд от нажатых кнопок
        mess = call.data
        message = call.message
        c_arg = self.CommandArgs() # определили объект получающий аргументы из строки команд чата 
        if   mess == "mypixlist": self.my_pixlist(message)
        elif mess == "mydoclist": self.my_doclist(message)
        elif mess == "myocr": self.ocr_mode_on(message)
        elif mess == "mybarcode": self.bar_mode_on(message)
        elif c_arg.is_exist(mess, "getpix"): self.sendpix(message,c_arg.arg_name()) # получение команд и их аргументов от кнопок
        elif c_arg.is_exist(mess, "getdoc"): self.sendfile(message,c_arg.arg_name())# получение команд и их аргументов от кнопок
        elif mess == 'menu': self.main_menu(message)
        # bot.answer_callback_query(call.id, show_alert=True, text="вызвано меню")
    # class  ChatBot ------