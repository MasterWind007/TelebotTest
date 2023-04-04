import pytesseract
from pytesseract import pytesseract as Pt
import cv2


class OcrClass:
    def __init__(self, file_path , exe_path):
        self.teceract_exe_path = exe_path 
        Pt.tesseract_cmd = self.teceract_exe_path[0]
        self.img = cv2.imread(file_path)
        self.img_copy = None
        self.t_conf = u"--psm 12"
        """
            conf = u"--psm 11"
            text = Pt.image_to_string(self.img, lang ='rus+eng', config=conf)
            psm - Режимы сегментации страницы:
            0 Только ориентация и обнаружение скриптом (OSD).
            1 Автоматическая сегментация страницы с OSD.
            2 Автоматическая сегментация страницы но без OSD или OCR.
            3 Полностью автоматическая сегментация страницы, но без OSD. (По умолчанию)
            4 Предполагается единичная колонка текста переменной длины.
            5 Предполагается единый унифицированный блок вертикально выравненного текста.
            6 Предполагается единый унифицированный блок текста.
            7 Обрабатывать изображение как единичную текстовую строку.
            8 Обрабатывать изображение как единичное слово.
            9 Обрабатывать изображение как единичное слово в круге.
            10 Обрабатывать изображение как единичный символ.
            11 Разреженный текст. Найти столько текста, сколько возможно без особого порядка.
            12 Разреженный текст с OSD.
            13 Сырая строка. Обрабатывать изображение как единичную текстовую строку, обход специфичных для Tesseract 
        """

    def  set_tesseract_path(self, path):
        Pt.tesseract_cmd = path
        
    def img_from_file(self, file_path):
        self.img = cv2.imread(file_path)

    def image_to_string(self):
        try:
            return Pt.image_to_string(self.img, lang ='rus+eng', config = self.t_conf)
        except: 
           self.set_tesseract_path(self.teceract_exe_path[1])
           return Pt.image_to_string(self.img, lang ='rus+eng', config = self.t_conf)
 
    def image_to_data(self):
        return Pt.image_to_data(self.img, lang='rus+eng', output_type=Pt.Output.DICT)
    
    def emphasize_from_img(self, tg_word = ''):
        img_copy = self.img.copy()
        data = Pt.image_to_data(self.img, output_type=Pt.Output.DICT)
        word_rects = [i for i, word in enumerate(data["text"]) if word.lower().startswith(tg_word)]
        for rects in word_rects:
            w = data["width"][rects]
            h = data["height"][rects]
            l = data["left"][rects]
            t = data["top"][rects]
            p1 = (l, t)
            p2 = (l, t + h)
            img_copy = cv2.rectangle(img_copy, p1, p2, color=(255,0,0), thickness=2)
        return img_copy       




    
        
           