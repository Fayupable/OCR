import pytesseract
from PIL import Image
import tkinter as tk
import re
import os

def is_valid_product_name(product_name):
    # Check if the product name is valid
    if len(product_name) < 3:
        return False
    if re.search(r'^\d+$', product_name):  # If the product name is only numbers
        return False
    if re.search(r'\b(KDV|TOPLAM|TOTAL|GENEL|TOPKDV|Sabit|@|ul|#|#l|%|MIGROS|A101|SOK|NO)\b', product_name, re.IGNORECASE):
        return False
    if re.search(r'\b(AD|SOYAD|FİRMA|TARİH|FATURA|FATURASI|FATURANIN|ALICI|VERGİ|VERGİSİZ|VERGİLİ)\b', product_name, re.IGNORECASE):
        return False
    if re.search(r'\b(TUTARI|TUTAR|TUTARI|TUTARIN|TUTARLARI|TUTARLAR|TUTARLARIN|TUTARLARININ|TUTARININ)\b', product_name, re.IGNORECASE):
        return False
    

    return True

def extract_product_and_price(text):
    # Regex to match products sold by weight
    pattern_by_weight = re.compile(r'(\d+,\d+)\s*KG\s*x\s*(\d+,\d+)\s*TL/KG\s*(.+?)\s*\*\s*([0-9,]+)')
    matches_by_weight = pattern_by_weight.findall(text)
    
    # Regex to match products not sold by weight
    pattern = re.compile(r'(.+?)\s*\*\s*([0-9,.]+)')
    matches = pattern.findall(text)
    
    # Combine both matches
    combined_matches = matches_by_weight + matches
    return combined_matches

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
        if len(match) == 4:  # For products sold by weight
            weight = match[0]
            price_per_kg = match[1]
            product_name = match[2].strip()
            total_price = match[3]
            if is_valid_product_name(product_name):
                product_and_price = {"Product": product_name, "Weight": weight, "Price per KG": price_per_kg, "Total Price": total_price}
                products_and_prices.append(product_and_price)
        else:  # For products not sold by weight
            product_name = match[0].strip()
            total_price = match[1]
            if is_valid_product_name(product_name):
                product_and_price = {"Product": product_name, "Price": total_price}
                products_and_prices.append(product_and_price)

    # Return the list of products and prices and the original OCR text
    return products_and_prices, text

def save_to_file(text):
    with open("output.txt", "w", encoding='utf-8') as file:
        file.write(text)

def display_and_save_output(products_and_prices, original_text):
    # Create a Tkinter window
    window = tk.Tk()

    # Create a text widget
    text_widget = tk.Text(window, height=20, width=70)

    # Add the products and prices to the text widget
    for product_and_price in products_and_prices:
        if "Weight" in product_and_price:
            formatted_text = f"Product: {product_and_price['Product']}\tWeight: {product_and_price['Weight']} KG\tPrice per KG: {product_and_price['Price per KG']} TL/KG\tTotal Price: {product_and_price['Total Price']}\n"
        else:
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
    products_and_prices, ocr_text = ocr_image('/Users/pc/Documents/GitHub/OCR/pyocrtest/processed_photos/22.png')

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
