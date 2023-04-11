import base64
import json
import os
import subprocess
from pathlib import Path



class yaOCR():
    def __init__(self, OAuth='', folder_id=''):
        self.outfile=''
        self.o_auth = OAuth
        self.folder_id = folder_id

    def get_aim(self, OAuth=''):
        cloud_id = {"yandexPassportOauthToken": OAuth}
        get_token = ''.join(("curl -X POST -H 'Content-Type: application/json' -d \"", str(cloud_id), "\" ",\
                     "https://iam.api.cloud.yandex.net/iam/v1/tokens")) 
        IAM_TOKEN = subprocess.check_output(get_token,  shell=True)
        return str(IAM_TOKEN[16:-49])[2:-5]
    
    def encode_file(self, file):
        with open(file, 'rb') as f:
            file_content = f.read()
        return base64.b64encode(file_content).decode('utf-8')
    
    def image_to_string(self, file_img =Path('Comon','Tmp','ocrimg.jpg')):
        output_json = Path('Comon','Tmp','output.json')
        outfile = self.encode_file(file_img)
        out = {     #распознавание текста
            "folderId": self.folder_id,
            "analyze_specs": [{
                "content": outfile,
                "features": [{
                    "type": "TEXT_DETECTION",
                    "text_detection_config": {
                        "language_codes": ["*"]
                    }
                }]
            }]
        }
        with open('body.json', 'w') as f:
            json.dump(out, f)
        IAM_TOKEN = self.get_aim(self.o_auth)
        crl = 'curl -X POST  -H "Content-Type: application/json" -H "Authorization: Bearer '+IAM_TOKEN+'" -d @body.json https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze > output.json'
        export_req = ''.join(('export IAM_TOKEN=', IAM_TOKEN ))
        to_curl = ''.join(crl)
        os.system(export_req)
        os.system(to_curl)
        data = ''
        with open('output.json', 'r') as f:
            data_l = [row.strip() for row in f]
        for line in data_l:
            if line.startswith('"lines"'): data +='\n'
            if line.startswith('"text"'): data+=line[9:-2]+' '
        return data

    
class YaKeys():
    def __init__(self, key_path=Path('Comon','Res','yaKEY.json')):
        self.path = key_path

    def set_key_path(self, path):
         self.path = path

    def get_keys(self, path):
                with open(path) as f:
                    keys = json.load(f)
                return keys
    
    def set_keys(self, OAuth, folderid):
         yandexKey = {'OAuth': OAuth,'folderid':folderid}
         with open(self.path,'w') as f:
            json.dump(yandexKey, f,  sort_keys=True, indent=2)     

class YandexOCR(YaKeys, yaOCR):
        def __init__(self, key_path=Path('Comon', 'Res', 'yaKEY.json')):
             super().__init__(key_path)
             ya_keys = self.get_keys(key_path)
             self.o_auth = ya_keys.get('OAuth')
             self.folder_id = ya_keys.get('folderid')
            

