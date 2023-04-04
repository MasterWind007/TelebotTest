import openai

class GptChat:
    def __init__(self, key=''):
        openai.api_key = key
        self.engine = "text-davinci-003"
        self.temperature = 0.8
        self.max_tokens=1000

    def get_key(self, file = f'Comon\Res\gpt_Key'):
        with open(file) as key:  
            ip_key = key.read()  
        openai.api_key = ip_key

    def set_engine(self, eng):
        self.engine = eng

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
        except: return 'GptErr!'

