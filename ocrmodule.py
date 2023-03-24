import pytesseract
import cv2

class OcrClass:
    def __init__(self, file_path):
        self.teceract_exe_path = ''
        pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        self.img = cv2.imread(file_path)
        self.img_copy = None

    def img_from_file(self, file_path):
        self.img = cv2.imread(file_path)

    def image_to_string(self):
        return pytesseract.image_to_string(self.img)
 
    def image_to_data(self):
        return pytesseract.image_to_data(self.img, output_type=pytesseract.Output.DICT)
    
    def emphasize_from_img(self, tg_word = ''):
        img_copy = self.img.copy()
        data = pytesseract.image_to_data(self.img, output_type=pytesseract.Output.DICT)
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




    
        
           