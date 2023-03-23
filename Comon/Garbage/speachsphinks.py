# Оффлайн распознаватель речи
#  перед использованием необходимо установить
#  swig  и pocketsphinx 
#  pip install swig
#  pip install pocketsphinx
#  так же нажноскачать руские словари по ссылке
#  https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/Russian/zero_ru_cont_8k_v3.tar.gz/download
#  и из архива достать папку zero_ru_cont_8k_v3 и из нее скопировать следующие файлы и папку:
#  ru.dic
#  ru.lm
#  zero_ru.cd_cont_4000
#  в папку
#  C:\Users\%USERPROFILE%\AppData\Local\Programs\Python\Python311\Lib\site-packages\pocketsphinx\model
#  примпрно так:
#  copy ru.dic C:\Users\%USERPROFILE%\AppData\Local\Programs\Python\Python311\Lib\site-packages\pocketsphinx\model
#  copy ru.lm C:\Users\%USERPROFILE%\AppData\Local\Programs\Python\Python311\Lib\site-packages\pocketsphinx\model
#  copy zero_ru.cd_cont_4000 C:\Users\%USERPROFILE%\AppData\Local\Programs\Python\Python311\Lib\site-packages\pocketsphinx\model
# ----------------------------------------------------------------------------------------------------------------------------------

import os
from pocketsphinx import LiveSpeech, get_model_path

model_path = get_model_path() # микрофон должен быть подключен

speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    hmm=os.path.join(model_path, 'zero_ru.cd_cont_4000'),
    lm=os.path.join(model_path, 'ru.lm'),
    dic=os.path.join(model_path, 'ru.dic')
)

print("Say something!")  #  когда в консоли появиться сообщение "Say something!"  можно распознавать речь

for phrase in speech:
    print(phrase)