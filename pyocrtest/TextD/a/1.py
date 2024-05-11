import re

def extract_receipt_details(text):
    # Time and date extraction
    time = re.search(r'SAAT :(\d{2}:\d{2})', text)
    date = re.search(r'TARIH: (\d{2}/\d{2}/\d{4})', text)
    
    # Products and prices extraction
    product_pattern = re.compile(r'(?P<product>.+?)\s*[\*\«\+\=]\s*(?P<price>\d{1,3}(?:,\d{2}))')
    products = product_pattern.findall(text)
    
    # Cleaning product names
    cleaned_products = []
    for product, price in products:
        product = re.sub(r'\s*[a-zA-Z0-9]+$', '', product)  # Simplified to remove trailing characters
        cleaned_products.append((product.strip(), price))

    return {
        "date": date.group(1) if date else "Date not found",
        "time": time.group(1) if time else "Time not found",
        "products": cleaned_products
    }

# Sample text from your receipt
receipt_text = """
TARIH: 29/02/2024 SAAT :09:42
Fis No :0075

MIGROS KABUK.Y .FIST. w1 *59,50
BARILLA GNOCHETTI a *33,50
BARILLA CONCHIGLIE ~ #1 «33,50
ICIM SEF KREMA bal *39,95
ICIM SEF KREMA a1 «39,95
MIGROS KREM PEYNIR aa +62,50
DURANLAR RULO KAYMAK = #1 «52,50
ICIM LABNE PEYNIR a *79,90
MIGROS PUDRA SEKERI al *13,75 .
"""

# Extract details
receipt_details = extract_receipt_details(receipt_text)

# Print the extracted information
print("Date:", receipt_details["date"])
print("Time:", receipt_details["time"])
print("Products and Prices:")
for product, price in receipt_details["products"]:
    print(f"Product: {product}, Price: {price}")



'''
import pytesseract
from PIL import Image
import tkinter as tk
import re
import os

def clean_product_name(product_name):
    # Remove unwanted patterns more accurately
    product_name = re.sub(r'\s*(w1|bal|a|a1|al|aa)\s*', '', product_name)
    return product_name

def extract_details(text):
    # Extract date and time
    date_search = re.search(r'TARIH: (\d{2}/\d{2}/\d{4})', text)
    time_search = re.search(r'SAAT :(\d{2}:\d{2})', text)
    date = date_search.group(1) if date_search else "Date not found"
    time = time_search.group(1) if time_search else "Time not found"
    
    # Extract products and prices
    pattern = re.compile(r'(.+?)\s*[\*\«\+\=]\s*(\d{1,3}(?:,\d{2}))')
    matches = pattern.findall(text)
    
    products_and_prices = []
    for match in matches:
        product_name = clean_product_name(match[0])
        product_and_price = {"Product": product_name.strip(), "Price": match[1]}
        products_and_prices.append(product_and_price)

    return date, time, products_and_prices

def ocr_image(image_path):
    # Open the image file
    image = Image.open(image_path)

    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(image)

    # Extract date, time, product names, and prices
    date, time, products_and_prices = extract_details(text)
    
    return date, time, products_and_prices, text

def is_receipt_already_saved(text, file_path="output.txt"):
    try:
        with open(file_path, "r") as file:
            existing_content = file.read()
            if text.strip() in existing_content:
                return True
    except FileNotFoundError:
        return False
    return False

def save_to_file(text):
    # Check if the receipt is already saved
    if not is_receipt_already_saved(text):
        # Append mode 'a' to add the text to the end of the file
        with open("output.txt", "a") as file:
            file.write("\n-----------------------------\n")  # Add a separator before new content
            file.write(text)  # Append the new OCR text
            file.write("\n-----------------------------\n")

    else:
        print("Receipt already saved. Not duplicating.")

def display_and_save_output(date, time, products_and_prices, original_text):
    # Create a Tkinter window
    window = tk.Tk()

    # Create a text widget
    text_widget = tk.Text(window, height=30, width=70)

    # Add date and time
    text_widget.insert(tk.END, f"Date: {date}\nTime: {time}\n\n")

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
    date, time, products_and_prices, ocr_text = ocr_image('/Users/pc/Documents/GitHub/OCR/pyocrtest/photo/img2.png')

    # Display the output in a Tkinter window and save to a file
    display_and_save_output(date, time, products_and_prices, ocr_text)
    
if __name__ == '__main__':
    test()

'''