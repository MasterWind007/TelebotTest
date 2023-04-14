from yaauth import YaKeys, YaSession
from pydub import AudioSegment
import os




class YaVoiceSynPrep():
    def __init_(self):
        self.iam_token =''
        self.folder_id = ''
        self.raw_file =''
        self.out_file = ''
        self.text = ''



    def text_to_ogg(self, text, ogg_file)-> None:
        crl  = 'curl -X POST '
        crl += '-H "Authorization: Bearer '+self.iam_token+'" '
        crl+=  '-o '+ogg_file.__str__() 
        crl+=  ' --data-urlencode "text='+text+'"'
        crl+=  ' -d "lang=ru-RU&voice=filipp&folderId='+self.folder_id+'&sampleRateHertz=48000"'
        crl+=  ' https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
        export_req = ''.join(('export IAM_TOKEN=', self.iam_token ))
        to_curl = ''.join(crl)
        os.system(export_req)
        os.system(to_curl)





class YaVoiceSyn(YaVoiceSynPrep):
    def __init__(self, out_file):
        ya_keys_obj = YaKeys()
        self.ya_keys = ya_keys_obj.get_keys()
        self.folder_id = self.ya_keys.get('folderid')
        self.out_file = out_file
    
    def text_to_voice(self, text):
        sess_keys = YaSession().getsession(self.ya_keys.get('OAuth'),self.ya_keys.get('folderid'))
        self.iam_token = sess_keys.get('IAM')
        self.text_to_ogg(text, self.out_file)





















