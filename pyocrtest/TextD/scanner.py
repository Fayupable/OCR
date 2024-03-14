import cv2 as cv
import easyocr
import numpy as np
import re

# Read the image
image_path = '/Users/pc/Desktop/code/pyocrtest/photo/img1.jpeg'
img = cv.imread(image_path)

# Create a white image as a canvas for text
white_canvas = np.ones_like(img) * 255  # Creating a white image of the same size as the input image

# Combine original image and white canvas horizontally
combined_img = np.hstack((img, white_canvas))

# Create an instance of text reader
reader = easyocr.Reader(['en'], gpu=False)

# Define regex pattern to extract product name, VAT rate, and price
product_pattern = re.compile(r'(.+)\s+(\d+)%\s+(-?\d+\.\d+)')  # Product Name VAT_rate Price

# Detect text
try:
    result = reader.readtext(image_path)

    thres = 0.01

    # Draw text and box
    previous_bottom = 0
    for detection in result:
        bbox, text, score = detection
        print(detection)

        if score > thres:
            try:
                cv.rectangle(combined_img, (bbox[0][0], bbox[0][1]), (bbox[2][0], bbox[2][1]), (0, 255, 0), 2)
                
                # Check if the current text matches the product pattern
                match = re.match(product_pattern, text)
                if match:
                    product_name = match.group(1)
                    vat_rate = match.group(2)
                    price = match.group(3)
                    formatted_text = f'{product_name} - {vat_rate}% - {price}'
                    text_position = (bbox[0][0] + img.shape[1], previous_bottom)  # Adjust the space here
                    cv.putText(combined_img, formatted_text, text_position, cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    text_position = (bbox[0][0] + img.shape[1], previous_bottom)  # Adjust the space here
                    cv.putText(combined_img, text, text_position, cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Update previous bottom for the next text
                previous_bottom = text_position[1] + 20  # Adjust the space here
                print("Previous Bottom:", previous_bottom)  # Debugging: Print the previous bottom value
            except Exception as e:
                print("Error while drawing bounding box:", e)
    # Show the image
    cv.imshow('Detected Text', combined_img)
    cv.waitKey(0)
    cv.destroyAllWindows()

except Exception as e:
    print("An error occurred:", e)
