# List of meat cuts in Turkish
yemek_isimleri = """


"""

# Path to the file where meat cuts will be stored
dosya_adi = ".txt" # Write the path to the file name where the list will be stored

# Attempt to read the existing file or create a new one if it does not exist
try:
    # Open the file in read+write mode
    with open(dosya_adi, "r+", encoding="utf-8") as dosya:
        existing_content = dosya.read()
        existing_items = existing_content.split('\n')
        
        # Identify new items that are not in the existing content
        new_items = [kelime for kelime in yemek_isimleri.strip().split('\n') if kelime not in existing_content]

        # Combine, sort alphabetically, and remove duplicates
        combined_items = sorted(set(existing_items + new_items), key=str.casefold)

        # Rewrite the file with sorted items
        dosya.seek(0)  # Move cursor to the start of the file
        dosya.write('\n'.join(combined_items))
        dosya.truncate()  # Remove any trailing old content after current position
        
        # Feedback about the operation
        if new_items:
            print(f"Added new items: {', '.join(new_items)}")
        else:
            print("No new words added.")
except FileNotFoundError:
    # If the file does not exist, create a new one and write the initial list
    with open(dosya_adi, "w", encoding="utf-8") as dosya:
        sorted_items = sorted(yemek_isimleri.strip().split('\n'), key=str.casefold)
        dosya.write('\n'.join(sorted_items))
    print("New file created and content written.")
