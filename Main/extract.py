
from PIL import Image
import pytesseract
import csv
from pathlib import Path

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files (x86)\Tesseract-OCR\Tesseract.exe'

def converter(image_name):
    folder = Path('Main/uploads/')
    file = r'uploads/'+image_name
    r = Image.open(file)
    r.load()
    #Converting inmage to text with preserving interline spaces
    text = pytesseract.image_to_string(r, config='-c preserve_interword_spaces=1x1 --psm 6 --oem 3' )

    data = [i.split() for i in text.split('\n')]


    print(data)

    with open('CSVs/'+image_name[:-4]+'.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)