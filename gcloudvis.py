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
