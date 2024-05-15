import cv2 as cv
import easyocr
import numpy as np
import re

# Read the image
image_path = '/Users/pc/Documents/GitHub/OCR/pyocrtest/processed_photos/25.jpg'
img = cv.imread(image_path)

# Convert the image to grayscale
gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# Create a white image as a canvas for text
white_canvas = np.ones_like(gray_img) * 255  # Creating a white image of the same size as the input image

# Combine original image and white canvas horizontally
combined_img = np.hstack((gray_img, white_canvas))

# Create an instance of text reader
reader = easyocr.Reader(['en'], gpu=False)

# Define regex pattern to check if text is a price
#(.+)\s+%([0-9,.]+)\s+\*([0-9,.]+) other regex
price_pattern = re.compile(r'(.+)\s+\*([0-9,.]+)')


# Detect text
try:
    result = reader.readtext(image_path)

    thres = 0.01

    # Draw text and box
    previous_bottom = 0
    for detection in result:
        bbox, text, score = detection

        if score > thres:
            try:
                cv.rectangle(combined_img, (bbox[0][0], bbox[0][1]), (bbox[2][0], bbox[2][1]), (0, 255, 0), 2)
                
                # Check if the current text matches the price pattern
                if re.match(price_pattern, text) and previous_bottom != 0:
                    text_position = (bbox[0][0] + gray_img.shape[1], previous_bottom)
                    
                else:
                    text_position = (bbox[0][0] + gray_img.shape[1], previous_bottom)  # Adjust the space here
                cv.putText(combined_img, text, text_position, cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Update previous bottom for the next text
                previous_bottom = text_position[1] + 20  # Adjust the space here
                print(text)

            
            except Exception as e:
                print("Error while drawing bounding box:", e)
    # Show the image
    cv.imshow('Detected Text', combined_img)    
    cv.waitKey(0)
    cv.destroyAllWindows()


except Exception as e:
    print("An error occurred:", e)
