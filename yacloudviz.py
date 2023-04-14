import base64
import json
import os
from pathlib import Path
from yaauth import YaKeys, YaSession


class yaOCR():
    def __init__(self):
        self.aim_key = ''
        self.folder_id = ''

    def __encode_file(self, file):
        with open(file, 'rb') as f:
            file_content = f.read()
        return base64.b64encode(file_content).decode('utf-8')
    
    def image_to_str(self, file_img =Path('Comon','Tmp','ocrimg.jpg')):
        outfile = self.__encode_file(file_img)
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
        IAM_TOKEN = self.aim_key
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

    
class YandexOCR(yaOCR):
    def __init__(self):
        yakeys_obj = YaKeys()
        self.yakeys = yakeys_obj.get_keys()
        self.session = YaSession()

    def image_to_string (self):
        aim_dict = self.session.getsession(self.yakeys.get('OAuth'),self.yakeys.get('folderid'))
        self.aim_key = aim_dict.get('IAM')
        self.folder_id = aim_dict.get('folderid') 
        return self.image_to_str()

            

