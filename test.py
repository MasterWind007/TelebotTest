from  yacloudviz import YandexOCR


ocr = YandexOCR()
text = ocr.image_to_string()

print(text)