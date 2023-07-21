import pytesseract
from PIL import Image
from docx import Document


import os
os.environ['PATH'] += r';C:\Program Files\Tesseract-OCR;'


def image_to_word(image_path, output_path):
    # Открываем изображение
    image = Image.open(image_path)

    # Используем pytesseract для распознавания текста
    text = pytesseract.image_to_string(image, lang='rus')

    # Создаем новый документ Word
    doc = Document()
    doc.add_paragraph(text)
    doc.save(output_path)


if __name__ == "__main__":
    # Путь к изображени
    image_path = r"C:\Users\ikvict\Downloads\im.jpg"

    # Путь для сохранения документа Word с распознанным текстом
    output_word_path = "output.docx"

    image_to_word(image_path, output_word_path)
    print(output_word_path)
