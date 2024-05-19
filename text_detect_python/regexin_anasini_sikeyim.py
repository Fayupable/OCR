import cv2 as cv
import easyocr
import re

def is_valid_product_name(product_name):
    if len(product_name) < 3:
        return False
    if re.search(r'^\d+$', product_name):  # If the product name is only numbers
        return False
    if re.search(r'\b(KDV|TOPLAM|TOTAL|GENEL|TOPKDV|Sabit|@|ul|#|#l|%|MIGROS|A101|SOK|NO|INDIRIM|iND|iNDiRiMLER|#|TOPKIV|FIS|TARİH|SAAT)\b', product_name, re.IGNORECASE):
        return False
    return True

def extract_product_and_price(text):
    # Regex to match products sold by weight
    pattern_by_weight = re.compile(r'(\d+[.,\s]?\d{0,3})\s*K[CG]?\s*[xX\s]\s*(\d+[.,\s]?\d{0,2})\s*TL\s*[\/I]?[KG]?\s*(.+?)\s*\*\s*([0-9,]+)')
    matches_by_weight = pattern_by_weight.findall(text)
    
    # Regex to match products sold by quantity
    pattern_by_quantity = re.compile(r'(\d+)\s*AD\s*[xX\s]\s*(\d+[.,]?\d{0,2})\s*TL\s*[\/]?\s*AD\s*(.+?)\s*\*\s*([0-9,]+)')
    matches_by_quantity = pattern_by_quantity.findall(text)

    # Regex to match products not sold by weight or quantity
    pattern = re.compile(r'(.+?)\s*\*\s*([0-9,.]+)')
    matches = pattern.findall(text)
    
    # Combine all matches
    combined_matches = matches_by_weight + matches_by_quantity + matches
    return combined_matches

def extract_date(text):
    # Regex to match dates in format xx/xx/xxxx or xx.xx.xxxx
    date_pattern = re.compile(r'\b\d{2}[./]\d{2}[./]\d{4}\b')
    dates = date_pattern.findall(text)
    
    if dates:
        return dates[-1]  # Return the last date found as it's likely to be the most relevant
    else:
        return None

def extract_store_name(text):
    # List of known store names
    store_names = ['MIGROS', 'A101', 'SOK', 'BIM', 'CARREFOURSA', 'TESCO', 'METRO', 'GROSPER', 'BICEN', 'KIPA', 'TARIM KREDI KOOPERATIFLERI', 'MACROCENTER', 'EKOMINI', 'HAKMAR', 'MIGROS JET', 'FILE MARKET']
    store_pattern = re.compile(r'\b(' + '|'.join(store_names) + r')\b', re.IGNORECASE)
    
    stores = store_pattern.findall(text)
    
    if stores:
        return stores[0].upper()  # Return the first matching store name found
    else:
        return "Unknown Store"

def process_receipt(text):
    # Extract date
    date = extract_date(text)
    
    # Extract store name
    store_name = extract_store_name(text)
    
    # Extract product and price
    matches = extract_product_and_price(text)
    
    # Create a list to store the products and prices
    products_and_prices = []
    processed_products = set()  # To keep track of products to avoid duplicates

    for match in matches:
        if len(match) == 5:  # For products sold by weight
            weight = match[0]
            price_per_kg = match[1]
            product_name = match[2].strip()
            total_price = match[3]
            product_key = (product_name, weight, price_per_kg, total_price)
            if is_valid_product_name(product_name) and product_key not in processed_products:
                product_and_price = {"Product": product_name, "Weight": weight, "Price per KG": price_per_kg, "Total Price": total_price}
                products_and_prices.append(product_and_price)
                processed_products.add(product_key)  # Add to set
        elif len(match) == 4:  # For products sold by quantity
            quantity = match[0]
            price_per_unit = match[1]
            product_name = match[2].strip()
            total_price = match[3]
            product_key = (product_name, quantity, price_per_unit, total_price)
            if is_valid_product_name(product_name) and product_key not in processed_products:
                product_and_price = {"Product": product_name, "Quantity": quantity, "Price per Unit": price_per_unit, "Total Price": total_price}
                products_and_prices.append(product_and_price)
                processed_products.add(product_key)  # Add to set
        else:  # For products not sold by weight or quantity
            product_name = match[0].strip()
            total_price = match[1]
            product_key = (product_name, total_price)
            if is_valid_product_name(product_name) and product_key not in processed_products:
                product_and_price = {"Product": product_name, "Price": total_price}
                products_and_prices.append(product_and_price)
                processed_products.add(product_key)  # Add to set

    return date, store_name, products_and_prices

def ocr_image(image_path, gpu):
    # Read the image
    img = cv.imread(image_path)

    # Convert the image to grayscale
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Create an instance of text reader
    reader = easyocr.Reader(['en'], gpu=gpu)

    # Detect text
    result = reader.readtext(gray_img)

    # Extract text from the detection results
    text = " ".join([detection[1] for detection in result])

    return text

def main(image_path):
    # Perform OCR on the image
    ocr_text = ocr_image(image_path, False)

    # Process the OCR text
    date, store_name, products_and_prices = process_receipt(ocr_text)

    # Print store name
    print(f"Store Name: {store_name}")

    # Print date
    if date:
        print(f"Date found in the receipt: {date}")
    else:
        print("No date found in the receipt.")

    # Convert list of dictionaries to set of tuples to remove duplicates
    products_and_prices = set(tuple(product.items()) for product in products_and_prices)

    # Print organized product information
    for product in products_and_prices:
        product = dict(product)  # Convert tuple back to dictionary
        if "Weight" in product:
            print(f"Product: {product['Product']}, Weight: {product['Weight']} KG, Price per KG: {product['Price per KG']}, Total Price: {product['Total Price']}")
        elif "Quantity" in product:
            print(f"Product: {product['Product']}, Quantity: {product['Quantity']}, Price per Unit: {product['Price per Unit']}, Total Price: {product['Total Price']}")
        else:
            print(f"Product: {product['Product']}, Price: {product['Price']}")

if __name__ == '__main__':
    # Replace 'image_path' with the path to your image file
    image_path = '/Users/pc/Documents/GitHub/OCR/pyocrtest/processed_photos/62.png'
    main(image_path)
