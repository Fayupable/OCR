import os
from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
import re

class OcrImage:
    def __init__(self, ocr_text):
        self.ocr_text = ocr_text

    def extract_product_info(self):
        product_info = {}
        lines = self.ocr_text.split('\n')
        for line in lines:
            # Assuming product names are capitalized and prices are in the format of $xx.xx
            match = re.search(r'([A-Z][a-z]+)\s+\$(\d+\.\d+)', line)
            if match:
                product_name = match.group(1)
                price = float(match.group(2))
                product_info[product_name] = price
        return product_info

class TextComparer:
    def __init__(self, text_file, ocr_text):
        self.text_file = text_file
        self.ocr_text = ocr_text.split()

    def levelshtein_distance(self,s1,s2):
        if len(s1) > len(s2):
            s1,s2 = s2,s1
        distances = range(len(s1) + 1)
        for index2,char2 in enumerate(s2):
            newDistances = [index2+1]
            for index1,char1 in enumerate(s1):
                if char1 == char2:
                    newDistances.append(distances[index1])
                else:
                    newDistances.append(1 + min((distances[index1], distances[index1 + 1], newDistances[-1])))
            distances = newDistances
        return distances[-1]
    def normalized_levenshtein_distance(self,s1,s2):
        return self.levelshtein_distance(s1,s2) / max(len(s1), len(s2))
    
    def correct_ocred_text(self,threshold=0.8):
        with open(self.text_file, 'r') as f:
            text = f.read()
        text = text.split()
        for word in text:
            for ocr_word in self.ocr_text:
                
                if self.normalized_levenshtein_distance(word,ocr_word) < threshold:
                    return ocr_word
        return None






class PhotoPaths:
    def __init__(self, directory):
        self.directory = directory

    def get_photo_paths(self):
        photo_paths = {}
        for entry in os.listdir(self.directory):
            full_path = os.path.join(self.directory, entry)
            if os.path.isfile(full_path) and full_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                photo_paths[entry] = full_path
        return photo_paths


class PreprocessImg:
    def __init__(self, image_path):
        self.image_path = image_path

    def preprocess_image(self):
        # Open the image file
        image = Image.open(self.image_path)
        
        # Convert image to grayscale
        image = image.convert('L')
        
        # Enhance the image's contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2)  # Increase contrast
        
        # Sharpen the image
        image = image.filter(ImageFilter.SHARPEN)
        
        return image


# Get the list of photo paths
photo_paths = PhotoPaths('/Users/pc/Documents/GitHub/OCR/pyocrtest/processed_photos').get_photo_paths()
word_file_path = '/Users/pc/Documents/GitHub/OCR/pyocrtest/TextD/b/words.txt'

# Read the existing content of the output text file
with open('output.txt', 'r') as f:
    existing_content = f.read()

with open('output.txt', 'a') as f:
    # Process each photo for OCR without saving
    for photo_name, photo_path in photo_paths.items():
        # Create a PreprocessImg instance for the photo
        preprocessor = PreprocessImg(photo_path)
        
        # Preprocess the image in memory
        processed_image = preprocessor.preprocess_image()
        
        # Directly use the preprocessed image for OCR
        ocr_result = pytesseract.image_to_string(processed_image)
        
        # Check if the OCR result is already in the file
        if ocr_result not in existing_content:
            # Write the OCR result to the text file
            f.write(f'OCR Result for {photo_name}:\n')
            f.write(ocr_result)
            f.write('\n----------------\n')

        # Extract product info from the OCR result
        ocr_image = OcrImage(ocr_result)
        product_info = ocr_image.extract_product_info()
        print(product_info)