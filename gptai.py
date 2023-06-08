import openai
from pathlib import Path

class GptChat:
    def __init__(self, key=''):
        openai.api_key = key
        self.engine = "text-davinci-003"
        self.temperature = 0.8
        self.max_tokens=1000

    def get_key(self, file = Path('Comon','Res','gpt_Key')):
        '''
        Читает ключ из файла
        file - полный путь к файлу м ключем
        '''
        with open(file) as key:  
            ip_key = key.read()  
        openai.api_key = ip_key

    def set_engine(self, eng):
        '''
        Устанавливает движок для чата
        eng - имя движка например: "text-davinci-003"
        '''
        self.engine = eng

    def new_key(self, file = Path('Comon','Res','gpt_Key'), key=''):
        '''
        Заменяет API Key
        file - Путь к файлу с ключем
        key - Ключ
        '''    
        with open(file, 'w') as fil:
            try:
                fil.write(key)
                return True
            except: return False
            


    def set_temperature(self, temp):
        self.temperature = temp

    def set_max_tokens(self, tkn):
        self.max_tokens = tkn

    def answer(self, ask):
        try:
            ansv = openai.Completion.create(engine=self.engine, prompt=ask,
                                            temperature=self.temperature,
                                            max_tokens=self.max_tokens)
            return ansv.choices[0]['text']
        except: 
            print("Error GPT API!")
            return 'GptErr!'

