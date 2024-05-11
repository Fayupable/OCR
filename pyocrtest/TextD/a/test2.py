import cv2 as cv
import easyocr
import numpy as np
import re

def preprocess_image(image_path):
    """Resmi okur ve beyaz bir tuval oluşturur."""
    img = cv.imread(image_path)
    white_canvas = np.ones_like(img) * 255
    combined_img = np.hstack((img, white_canvas))
    return combined_img, img.shape[1]

def detect_and_draw_text(image, reader, product_pattern, img_width):
    """Metni tespit eder ve çizer."""
    try:
        result = reader.readtext(image)
        thres = 0.01
        previous_bottom = 0
        for detection in result:
            bbox, text, score = detection
            if score > thres:
                try:
                    cv.rectangle(image, (bbox[0][0], bbox[0][1]), (bbox[2][0], bbox[2][1]), (0, 255, 0), 2)
                    match = re.match(product_pattern, text)
                    if match:
                        product_name = match.group(1)
                        vat_rate = match.group(2)
                        price = match.group(3)
                        formatted_text = f'{product_name} - {vat_rate}% - {price}'
                        text_position = (bbox[0][0] + img_width, previous_bottom)
                        cv.putText(image, formatted_text, text_position, cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    else:
                        text_position = (bbox[0][0] + img_width, previous_bottom)
                        cv.putText(image, text, text_position, cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    previous_bottom = text_position[1] + 20
                except Exception as e:
                    print("Error while drawing bounding box:", e)
        return image  # Düzenlenmiş görüntüyü döndür
    except Exception as e:
        print("An error occurred:", e)

def main():
    """Ana işlem fonksiyonu."""
    try:
        image_path = '/Users/pc/Desktop/code/pyocrtest/photo/img1.jpeg'
        reader = easyocr.Reader(['en'], gpu=False)
        product_pattern = re.compile(r'(.+)\s+(\d+)%\s+(-?\d+\.\d+)')
        combined_img, img_width = preprocess_image(image_path)
        result_img = detect_and_draw_text(combined_img.copy(), reader, product_pattern, img_width)
        
        # Görüntüyü göster
        cv.imshow('Detected Text', result_img)
        cv.waitKey(0)
        cv.destroyAllWindows()
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
