import os

class TextComparer:
    def __init__(self, word_folder_path, ocr_file_path):
        self.word_folder_path = word_folder_path
        self.ocr_file_path = ocr_file_path
        self.load_ocr_text()
        self.corrections = []  # To store correction logs

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
        # Process each txt file in the word folder
        for filename in os.listdir(self.word_folder_path):
            if filename.endswith('.txt'):
                with open(os.path.join(self.word_folder_path, filename), 'r') as f:
                    txt_words = f.read().split()

                    for i, ocr_word in enumerate(self.ocr_words):
                        for txt_word in txt_words:
                            similarity = self.normalized_levenshtein_distance(ocr_word, txt_word)
                            if similarity > threshold and ocr_word != txt_word:
                                self.corrections.append((ocr_word, txt_word))  # Log correction
                                self.ocr_words[i] = txt_word  # Replace the word
        return ' '.join(self.ocr_words)

    def update_ocr_file(self):
        corrected_text = self.correct_ocred_text()
        if corrected_text:  # only update if there were corrections
            with open(self.ocr_file_path, 'w') as file:
                file.write(corrected_text)
        return self.corrections  # Return the list of corrections

# Example Usage
word_directory = '/Users/pc/Documents/GitHub/OCR/pyocrtest/word'
ocr_file_path = '/Users/pc/Documents/GitHub/OCR/output.txt'
comparer = TextComparer(word_directory, ocr_file_path)
corrections = comparer.update_ocr_file()
print("Corrections made:")
for original, corrected in corrections:
    print(f"Original: '{original}' -> Corrected: '{corrected}'")
