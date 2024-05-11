import subprocess

def clean_text_image(input_path, output_path):
    # Simplified ImageMagick command to adjust saturation and background
    command = [
        'convert', input_path,
        '-modulate', '100,150,100',  # Adjusts brightness, saturation, and hue
        '-background', 'gray',  # Sets background color
        '-flatten',  # Merges layers
        output_path
    ]

    # Execute the command
    try:
        subprocess.run(command, check=True)
        print("Görüntü başarıyla işlendi.")
    except subprocess.CalledProcessError as e:
        print("Bir hata oluştu: ", e)

# Example usage
input_image_path = '/Users/pc/Documents/GitHub/OCR/pyocrtest/photo/DDC877D1-D353-4AA0-972E-6E56251A8EC9_1_105_c.jpg'
output_image_path = '/Users/pc/Documents/GitHub/OCR/pyocrtest/photo/DDC877D1-D353-4AA0-972E-6E56251A8EC9_1_105_c1.jpg'

clean_text_image(input_image_path, output_image_path)
