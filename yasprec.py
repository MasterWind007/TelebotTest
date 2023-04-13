from yaauth import YaKeys, YaSession
import json
import os

class YaVoiceRc():
    def __init__(self):
      self.iam_token =''
      self.folder_id = ''
      self.audioout_json ='audioout.json'
    
    def __voice_to_json(self, voice_path, out_path) -> None:
        crl = 'curl -X POST -H "Authorization: Bearer '
        crl+= self.iam_token
        crl+='" -H "Transfer-Encoding: chunked" --data-binary "@'+voice_path.__str__()+'" "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?topic=general&folderId='
        crl+= self.folder_id
        crl+='" > '
        crl+= out_path.__str__()
        export_req = ''.join(('export IAM_TOKEN=', self.iam_token ))
        to_curl = ''.join(crl)
        os.system(export_req)
        os.system(to_curl)
    
    def __json_to_string(self,json_file) -> str:
        body = {}
        with open(json_file,'r') as json_out:
          try: body = json.load(json_out)
          except: return 'Ни чего не понял из того чтоты сказал!'  
        return body.get('result')

    def get_string(self, voice_path) -> str:
       self.__voice_to_json(voice_path, self.audioout_json)
       return self.__json_to_string(self.audioout_json)



class YaVoiceToText(YaVoiceRc):
    def __init__(self):
        ya_keys_obj = YaKeys()
        self.ya_keys = ya_keys_obj.get_keys()
        self.folder_id = self.ya_keys.get('folderid')

    def voice_to_string(self, voice_path, audioout_json = 'audioout.json')-> str: 
            '''
            Принимает:
            voice_path - путь к аудиофайлу *.ogg
            audioout_json - путь к выходному файлу *json по умолчанию audioout.json 
            в папке программы.
            Возвращает строку из файла audioout.json
            '''
            self.audioout_json = audioout_json
            sess_keys = YaSession().getsession(self.ya_keys.get('OAuth'),self.ya_keys.get('folderid'))
            self.iam_token = sess_keys.get('AIM')
            return self.get_string(voice_path)


# from pydub import AudioSegment

# # Преобразование mp3 в ogg                                                                       
# src = "transcript.mp3"
# dst = "test.ogg"

# # convert wav to mp3                                                            
# sound = AudioSegment.from_mp3(src)
# sound.export(dst, format="ogg")






