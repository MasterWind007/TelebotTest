class UsersDialogs:
    '''
    Класс описывающий структуру пользовательских диалогов с Chat GPT4
    Его назначение хранить и выдавать чату GPT4  последние max_msg (8) сообщений между
    конкретным  пользователем и чатом
    '''
    def __init__(self, max_msg = 6) -> None:
        self.usr_msg_sequence = {} # последовательность диалога польователя
        self.max_msg = max_msg
    
    def add_chat(self,chat_id) -> None:
        '''
        Добавляет пустое хранилище истории диалогов для пользователя
        '''
        self.usr_msg_sequence[chat_id] = []

    def add_msg(self, chat_id, msg) -> None:
        '''
            Добавляет сообщение в историю диалогов пользователя
            и удаляет самое старое сообщение, если клоичество
            сообщений превысило max_msg
        '''
        self.usr_msg_sequence[chat_id].append(msg)
        if len(self.usr_msg_sequence[chat_id]) > self.max_msg:
            self.usr_msg_sequence[chat_id].pop(0)
    
    def get_msg(self, chat_id) -> str:
        '''
        Возвращает историю диалогов пользователя в виде строки
        '''
        usr_chat = ''
        for chat_line in self.usr_msg_sequence[chat_id]:
            usr_chat += chat_line + '\n'
        return usr_chat
    
    def set_max_msg(self, max_msg) -> None:
        '''
        Устанавливает максимальное к-во хранимых сообщений диалога
        '''
        self.max_msg = max_msg
    
    def del_msg(self, chat_id) -> None:
        '''
        Удаляет сохраненный диалог пользователя
        '''
        self.usr_msg_sequence[chat_id].clear()  
    #----------                 