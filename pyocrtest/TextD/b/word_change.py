import os

class TextComparer:
    def __init__(self, word_folder_path, ocr_file_path):
        self.word_folder_path = word_folder_path
        self.ocr_file_path = ocr_file_path
        self.load_ocr_text()

    def load_ocr_text(self):
        with open(self.ocr_file_path, 'r') as file:
            self.ocr_words = file.read().split()

    def levenshtein_distance(self, s1, s2):
        if len(s1) > len(s2):
            s1, s2 = s2, s1
        distances = range(len(s1) + 1)
        for index2, char2 in enumerate(s2):
            newDistances = [index2 + 1]
            for index1, char1 in enumerate(s1):
                if char1 == char2:
                    newDistances.append(distances[index1])
                else:
                    newDistances.append(1 + min((distances[index1], distances[index1 + 1], newDistances[-1])))
            distances = newDistances
        return distances[-1]

    def normalized_levenshtein_distance(self, s1, s2):
        return self.levenshtein_distance(s1, s2) / max(len(s1), len(s2))

    def correct_ocred_text(self, threshold=0.8):
        corrected = False
        # Process each txt file in the word folder
        for filename in os.listdir(self.word_folder_path):
            if filename.endswith('.txt'):
                with open(os.path.join(self.word_folder_path, filename), 'r') as f:
                    txt_words = f.read().split()

                    # Compare each word in the OCR text with each word in the txt file
                    for i, ocr_word in enumerate(self.ocr_words):
                        for txt_word in txt_words:
                            similarity = self.normalized_levenshtein_distance(ocr_word, txt_word)
                            # If the similarity is above the threshold and the word is different, replace the word in the OCR text
                            if similarity > threshold and ocr_word != txt_word:
                                self.ocr_words[i] = txt_word
                                corrected = True
                                break
                        if corrected:
                            break
        return ' '.join(self.ocr_words)

    def update_ocr_file(self):
        corrected_text = self.correct_ocred_text()
        if corrected_text:  # only update if there were corrections
            with open(self.ocr_file_path, 'w') as file:
                file.write(corrected_text)

# Example Usage
word_directory = '/Users/pc/Documents/GitHub/OCR/pyocrtest/word'
ocr_file_path = '/Users/pc/Documents/GitHub/OCR/output.txt'
comparer = TextComparer(word_directory, ocr_file_path)
comparer.update_ocr_file()

##sikiyim boyle kodu da ocri da