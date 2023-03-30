from pyzbar import pyzbar as bar
import cv2

class BarCode:
    def __init__(self):
        self.decoded = []

    def img_from_file(self, path):    # Возвращает объект image из файла с картинкой
        img = cv2.imread(path)
        return img

    def decode (self, img):             # Возвращает объект сожержащий данные по декодированому штрихкоду
        self.decoded = bar.decode(img)
        return self.decoded

    def draw_rect_bars (self, img):     # возвращает картинку с обведеннымv штрихкодами 
        self.decoded = self.decode(img) # а так же записывает декодированый штрихкод в self.decoded 
        image = img.copy()
        for decoded in self.decoded:
            left = decoded.rect.left; top = decoded.rect.top
            left1 = decoded.rect.left + decoded.rect.width
            down = decoded.rect.top + decoded.rect.height             
            image = cv2.rectangle(image,(left,top),(left1,down), color=(0, 255, 0),thickness=3)
        return image
    
    def corp_rect_bar(self, img):
        self.decoded = self.decode(img)
        img = img[self.decoded.rect.left, self.decoded.rect.top : 
                  self.decoded.rect.left + self.decoded.rect.width, self.decoded.rect.top + self.decoded.rect.height]
        return img

