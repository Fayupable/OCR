import re

def clean_product_name(product_name):
    product_name = re.sub(r'\s*a\s*', '', product_name)
    product_name = re.sub(r'\s*w1\s*', '', product_name)
    product_name = re.sub(r'\s*bal\s*', '', product_name)
    return product_name

def extract_product_and_price(text):
    pattern = re.compile(r'(.+)\*\s*([0-9,.]+)')
    matches = pattern.findall(text)
    return matches

# ...
def extract_product_info_from_file(file_path):
    product_info = {}
    with open(file_path, 'r') as f:
        text = f.read()
        matches = extract_product_and_price(text)
        for match in matches:
            product_name = clean_product_name(match[0])
            price_str = match[1].replace(',', '.')
            price_str = re.sub(r'\.{2,}', '.', price_str)  # replace multiple dots with a single dot
            price = float(price_str)
            product_info[product_name] = price
    return product_info

# Usage
file_path = '/Users/pc/Documents/GitHub/OCR/output.txt'
product_info = extract_product_info_from_file(file_path)

# Print each product info on a new line
for product, price in product_info.items():
    print(f'Product: {product}, Price: {price}')