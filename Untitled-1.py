
# lst = {'a': 8,
#        'b': 4,
#        'c': 13,
#        'd': 10,
#        'e': 170,
#        'f': 30}

# def sort (list):
#     prev_key = ''
#     max_val = 0
#     max_key = ''
#     for i in list:
#         if list.get(i) > max_val: 
#             prev_key = max_key  
#             max_val = list.get(i)
#             max_key = i
#     return((prev_key, max_key))

# def sort_next(list):
#     prev_key = []
#     max_val = 0
#     max_key = ''
#     for i in list:
#         if list.get(i) >= max_val: 
#             prev_key.append(max_key)  
#             max_val = list.get(i)
#             max_key = i
#     return((prev_key[1:], max_key))
       

# print (sort (lst))
# # print (sort_next (lst))


# def ask(func):
#     def inner(*args):
#         val = func(*args)
#         text = 'Сумма чисел равна '+ str(val)
#         return text
#     return inner

# @ask
# def summ(a,b):
#     return a+b

# print(summ(2,2))
import os
from google.cloud import vision

# Укажите свой API-ключ
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'Comon/Res/ocr-projets002255-f3f7fba2d684.json'

# Инициализируем объект класса VisionClient
vision_client = vision.ImageAnnotatorClient()

# открываем изображение
with open(r'Comon\\Tmp\\ocrimg.jpg', 'rb') as image_file:
    image = vision.Image(content=image_file.read())

# получаем результат
response = vision_client.text_detection(image=image)
texts = response.text_annotations

# выводим текст из изображения
for text in texts:
    print(text.description)
