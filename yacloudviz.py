import base64
import json
import os
import subprocess
from abc import ABCMeta, abstractmethod, abstractproperty


class OCRif():
    __metaclass__ = ABCMeta

    @abstractmethod
    def init():
        ...

    @abstractmethod
    def read_from_file():
        ...

    @abstractmethod
    def image_to_data():
        ...

    @abstractmethod
    def image_to_string():
        ...

class YandexOCRinit():
    def __init(self, OAuth=''):
        self.o_auth= OAuth
        self.out = { #распознавание текста
                        "folderId": folderid ,
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
        



def encode_file(file):
    with open(file, 'rb') as f:
        file_content = f.read()
    return base64.b64encode(file_content).decode('utf-8')
folderid = "b1g9m7ogbnpo0afrth9g"
outfile = encode_file('Comon\Tmp\ocrimg.jpg') #my image file 

out = {     #распознавание текста
    "folderId": folderid ,
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

# out = {  #  поиск морды лица
#     "folderId": folderid,
#     "analyze_specs": [{
#         "content": outfile,
#         "features": [{
#             "type": "CLASSIFICATION",
#             "classificationConfig": {
#                 "model": "quality"
#             }
# },
#         {
#             "type": "CLASSIFICATION",
#             "classificationConfig": {
#                 "model": "moderation"
#             }
#         },
#             {
#             "type": "FACE_DETECTION"
#         }]
#     }]
# }
    
#Готовим запрос
with open('body.json', 'w') as f:
    json.dump(out, f)
    
cloud_id = {"yandexPassportOauthToken": "y0_AgAAAAA2GPPIAATuwQAAAADeYXG_MunkevKMS_GIRQsbKNqepm-n3wg"}
get_token = ''.join(("curl -X POST -H 'Content-Type: application/json' -d \"", str(cloud_id), "\" ",\
                     "https://iam.api.cloud.yandex.net/iam/v1/tokens"))

IAM_TOKEN = subprocess.check_output(get_token,  shell=True)
IAM_TOKEN = str(IAM_TOKEN[16:-49])[2:-5] 
crl = 'curl -X POST  -H "Content-Type: application/json" -H "Authorization: Bearer '+IAM_TOKEN+'" -d @body.json https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze > output.json'
export_req = ''.join(('export IAM_TOKEN=', IAM_TOKEN ))
to_curl = ''.join(crl)

# Получаем ответ
os.system(export_req)
os.system(to_curl)