import pytesseract
from PIL import Image
import tkinter as tk
import re
import os

def clean_product_name(product_name):
    # Remove unwanted patterns
    product_name = re.sub(r'\s*a\s*', '', product_name)
    product_name = re.sub(r'\s*w1\s*', '', product_name)
    product_name = re.sub(r'\s*bal\s*', '', product_name)
    return product_name

def extract_product_and_price(text):
    pattern = re.compile(r'(.+)\*\s*([0-9,.]+)')
    matches = pattern.findall(text)
    return matches

def ocr_image(image_path):
    # Open the image file
    image = Image.open(image_path)

    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(image)

    # Extract product and price
    matches = extract_product_and_price(text)
    
    # Create a list to store the products and prices
    products_and_prices = []

    for match in matches:
        # Clean the product name
        product_name = clean_product_name(match[0])

        # Create a dictionary for the product and price
        product_and_price = {"Product": product_name, "Price": match[1]}
        
        # Add the dictionary to the list
        products_and_prices.append(product_and_price)

    # Return the list of products and prices and the original OCR text
    return products_and_prices, text

def save_to_file(text):
    with open("output.txt", "w") as file:
        file.write(text)

def display_and_save_output(products_and_prices, original_text):
    # Create a Tkinter window
    window = tk.Tk()

    # Create a text widget
    text_widget = tk.Text(window, height=10, width=50)

    # Add the products and prices to the text widget
    for product_and_price in products_and_prices:
        formatted_text = f"Product: {product_and_price['Product']}\tPrice: {product_and_price['Price']}\n"
        text_widget.insert(tk.END, formatted_text)

    # Add the text widget to the window
    text_widget.pack()

    # Run the Tkinter event loop
    window.mainloop()

    # Save OCR text to a file
    save_to_file(original_text)

def test():
    # Replace 'image_path' with the path to your image file
    products_and_prices, ocr_text = ocr_image('/Users/pc/Documents/GitHub/OCR/pyocrtest/processed_photos/35.jpeg')

    # Display the output in a Tkinter window and save to a file
    display_and_save_output(products_and_prices, ocr_text)
    
if __name__ == '__main__':
    test()


# def process_directory(directory):
#     # Iterate over all files in the directory
#     for filename in os.listdir(directory):
#         # Check if the file is an image
#         if filename.endswith(".png") or filename.endswith(".jpg"):
#             # Construct the full path to the image file
#             image_path = os.path.join(directory, filename)

#             # Perform OCR on the image
#             ocr_image(image_path)

# # Replace 'directory_path' with the path to your directory containing the images
# # process_directory('path/to/your/directory')