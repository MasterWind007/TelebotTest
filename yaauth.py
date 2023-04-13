import json
import subprocess
from pathlib import Path

class YaKeys():
    def __init__(self, key_path=Path('Comon','Res','yaKEY.json')):
        '''
        Принимает key_path - Путь к файлу *.json
        '''
        self.path = key_path

    def set_key_path(self, path):
         '''
         path - Путь к файлу
         Устанавливает путь к файлу хранения ключей 
         в формате json
         '''
         self.path = path

    def get_keys(self)-> dict:
        '''
        Возвращает словарь со структурой {'OAuth': '...', 'folderid':'...'}
        '''
        with open(self.path) as f:
            keys = json.load(f)
            return keys
    
    def set_keys(self, OAuth, folderid):
         '''
         Создает файл хранения OAuth KEY и folder ID 
         в файл формата json
         '''
         yandexKey = {'OAuth': OAuth,'folderid':folderid}
         with open(self.path,'w') as f:
            json.dump(yandexKey, f,  sort_keys=True, indent=2) 

class YaSession():
     def __init__(self):
        self.o_auth = ''
        self.folder_id = ''
     
     def __getaim(self,o_auth) -> str:
        cloud_id = {"yandexPassportOauthToken": o_auth}
        get_token = ''.join(("curl -X POST -H 'Content-Type: application/json' -d \"", str(cloud_id), "\" ",\
                     "https://iam.api.cloud.yandex.net/iam/v1/tokens")) 
        IAM_TOKEN = subprocess.check_output(get_token,  shell=True)
        return str(IAM_TOKEN[16:-49])[2:-5]          
    
     def getsession(self, o_auth, folder_id):
        '''
        Принимает строковые параметры:
        o_auth - Ключ Yandex OAuth Key
        folderid - идентификатор каталога
        Возвращает словаь со структурой {'AIM': '...', 'folderid':'...'} 
        '''
        aim = self.__getaim(o_auth)
        return {'AIM': aim, 'folderid':folder_id}
