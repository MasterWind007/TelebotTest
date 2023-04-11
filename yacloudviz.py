import base64
import json
import os
import subprocess
from pathlib import Path

# folderid = "b1g9m7ogbnpo0afrth9g"

class YandexOCR():
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
    
    def encode_file(file):
        with open(file, 'rb') as f:
            file_content = f.read()
        return base64.b64encode(file_content).decode('utf-8')
    
    def image_to_json(self, file_img =Path('Comon','Tmp','ocrimg.jpg')):
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
    

