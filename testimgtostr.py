import ocrmodule
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

file = r'Comon\Tmp\ocrimg.png'
oc = ocrmodule.OcrClass(file)
#print(pytesseract.image_to_string(file))

print(oc.image_to_string())