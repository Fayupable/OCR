import os
from PIL import Image

class PhotoProcessor:
    def __init__(self, directory='/Users/pc/Documents/GitHub/OCR/pyocrtest/photo'):
        self.directory = directory
        self.photos = self.get_photos()

    def get_photos(self):
        photo_files = []
        for filename in os.listdir(self.directory):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                photo_files.append(os.path.join(self.directory, filename))
        return photo_files

    def process_photos(self):
        for photo_file in self.photos:
            self.process_photo(photo_file)

    def process_photo(self, photo_file):
        # Open the image file
        image = Image.open(photo_file)
        # Add your photo processing code here
        # For example, you can convert the image to grayscale
        # image = image.convert('L')
        # Save the processed image
        # image.save('processed_' + photo_file)


PhotoProcessor().process_photos()
