import yaauth
from pydub import AudioSegment
import urllib.request
import json
import os


ya_keys = yaauth.YaKeys().get_keys()
sess_keys = yaauth.YaSession().getsession(ya_keys.get('OAuth'),ya_keys.get('folderid'))


FOLDER_ID = sess_keys.get('folderid') # Идентификатор каталога
IAM_TOKEN = sess_keys.get('AIM') # IAM-токен

crl = 'curl -X POST -H "Authorization: Bearer '+IAM_TOKEN+'" -H "Transfer-Encoding: chunked" --data-binary "@speech.ogg" "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?topic=general&folderId='+FOLDER_ID+'" > audioout.json'
export_req = ''.join(('export IAM_TOKEN=', IAM_TOKEN ))
to_curl = ''.join(crl)
os.system(export_req)
os.system(to_curl)






# # files                                                                         
# src = "transcript.mp3"
# dst = "test.ogg"

# # convert wav to mp3                                                            
# sound = AudioSegment.from_mp3(src)
# sound.export(dst, format="ogg")
