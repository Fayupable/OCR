import cv2 as cv
import easyocr
import numpy as np
import re

def read_and_preprocess_image(image_path):
    """Resmi okur ve işler."""
    img = cv.imread(image_path)
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    white_canvas = np.ones_like(gray_img) * 255
    combined_img = np.hstack((gray_img, white_canvas))
    return combined_img, gray_img.shape[1]

def detect_text(image, reader, price_pattern, img_width):
    """Metni tespit eder ve çizer."""
    try:
        result = reader.readtext(image_path)
        thres = 0.01
        previous_bottom = 0
        for detection in result:
            bbox, text, score = detection
            if score > thres:
                try:
                    cv.rectangle(image, (bbox[0][0], bbox[0][1]), (bbox[2][0], bbox[2][1]), (0, 255, 0), 2)
                    if re.match(price_pattern, text) and previous_bottom != 0:
                        text_position = (bbox[0][0] + img_width, previous_bottom)
                    else:
                        text_position = (bbox[0][0] + img_width, previous_bottom)
                    cv.putText(image, text, text_position, cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    previous_bottom = text_position[1] + 20
                except Exception as e:
                    print("Error while drawing bounding box:", e)
        return image
    except Exception as e:
        print("An error occurred:", e)

def show_image(image):
    """Görüntüyü gösterir."""
    cv.imshow('Detected Text', image)
    cv.waitKey(0)
    cv.destroyAllWindows()

def process_image(image_path):
    """Ana işlem fonksiyonu."""
    try:
        reader = easyocr.Reader(['en'], gpu=False)
        price_pattern = re.compile(r'(.+)\s+\*([0-9,.]+)')
        combined_img, img_width = read_and_preprocess_image(image_path)
        detected_image = detect_text(combined_img.copy(), reader, price_pattern, img_width)
        show_image(detected_image)
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    image_path = '/Users/pc/Desktop/code/pyocrtest/photo/img1.jpeg'
    process_image(image_path)
