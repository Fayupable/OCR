import os
from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
import fuzz # type: ignore




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


class OCRProcessor:
    def __init__(self, photo_paths, output_file, word_directory):
        self.photo_paths = photo_paths
        self.output_file = output_file
        self.word_directory = word_directory
        self.words = self.get_words_from_txt_files()

    def get_words_from_txt_files(self):
        words = []
        for filename in os.listdir(self.word_directory):
            if filename.endswith('.txt'):
                with open(os.path.join(self.word_directory, filename), 'r') as f:
                    words.extend(f.read().split())
        return words

    def get_best_match(self, ocr_result):
        best_match = None
        best_ratio = 0
        for word in self.words:
            ratio = fuzz.ratio(ocr_result.lower(), word.lower())
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = word
        return best_match if best_ratio > 85 else ocr_result

    def process_photos(self):
        # Read the existing content of the output text file
        with open(self.output_file, 'r') as f:
            existing_content = f.read()

        # Open the output text file in append mode
        with open(self.output_file, 'a') as f:
            # Process each photo for OCR without saving
            for photo_name, photo_path in self.photo_paths.items():
                # Create a PreprocessImg instance for the photo
                preprocessor = PreprocessImg(photo_path)
                
                # Preprocess the image in memory
                processed_image = preprocessor.preprocess_image()
                
                # Directly use the preprocessed image for OCR
                ocr_result = pytesseract.image_to_string(processed_image)
                best_match = self.get_best_match(ocr_result)
                
                # Check if the OCR result is already in the file
                if best_match not in existing_content:
                    # Write the OCR result to the text file
                    f.write(f'OCR Result for {photo_name}:\n')
                    f.write(best_match)
                    f.write('\n----------------\n')

# Get the list of photo paths
photo_paths = PhotoPaths('/Users/pc/Documents/GitHub/OCR/pyocrtest/processed_photos').get_photo_paths()

# Create an OCRProcessor instance
ocr_processor = OCRProcessor(photo_paths, 'output.txt', '/path/to/your/txt/files')

# Process the photos
ocr_processor.process_photos()