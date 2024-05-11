import get_photo as gp
from PIL import Image, ImageFilter, ImageEnhance

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

    def save_preprocessed_image(self, output_path):
        # Preprocess the image
        image = self.preprocess_image()
        
        # Save the preprocessed image to the specified output path
        image.save(output_path)

