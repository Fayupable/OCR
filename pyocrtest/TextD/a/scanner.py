import pytesseract
from PIL import Image

class SimpleOCR:
    def __init__(self, image_path):
        self.image_path = image_path

    def ocr_image(self):
        # Open the image file
        image = Image.open(self.image_path)

        # Perform OCR using Tesseract
        text = pytesseract.image_to_string(image)
        return text

    def display_text(self):
        # Extract text from the image and display it
        extracted_text = self.ocr_image()
        print("Extracted Text from Image:\n", extracted_text)

def test():
    # Specify the path to your image
    image_path = '/Users/pc/Documents/GitHub/OCR/pyocrtest/photo/DDC877D1-D353-4AA0-972E-6E56251A8EC9_1_105_c.jpg'
    ocr = SimpleOCR(image_path)
    ocr.display_text()

if __name__ == '__main__':
    test()
