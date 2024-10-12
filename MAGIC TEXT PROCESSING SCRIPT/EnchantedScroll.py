import random
import re
from spellchecker import SpellChecker

# Initialize spell checker
spell = SpellChecker()

# List of magical adjectives and epic verbs
magic_adjectives = ['dragon', 'mystical', 'cosmic', 'enchanted', 'glowing', 'ancient', 'celestial', 'shadowy', 'radiant']
epic_verbs = ['conquer', 'vanquish', 'transcend', 'summon', 'unleash', 'command', 'enchant', 'travel', 'explore']

# Function to clean text (remove unnecessary characters and fix typos)
def clean_text(text):
    # Remove any non-alphabetic characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Correct spelling mistakes
    corrected_text = []
    for word in text.split():
        corrected_word = spell.correction(word)
        corrected_text.append(corrected_word)
        
    return ' '.join(corrected_text)

# Function to process text and add magical flair
def process_text(text):
    words = text.split()
    new_text = []
    
    for word in words:
        # Add magical adjective to nouns (randomly)
        if random.random() < 0.3:  # 30% chance to make any noun magical
            magic_word = random.choice(magic_adjectives) + ' ' + word
            new_text.append(magic_word)
        # Replace simple verbs with epic ones (randomly)
        elif word.lower() in ['go', 'want', 'see', 'do', 'get', 'buy']:
            epic_word = random.choice(epic_verbs)
            new_text.append(epic_word)
        else:
            new_text.append(word)
    
    return ' '.join(new_text)

# Main function to run the text processing
def main():
    # Input text from user
    input_text = input("Enter your sentence: ")
    
    # Clean the input text
    clean_input = clean_text(input_text)
    
    # Check if input is empty after cleaning
    if not clean_input:
        print("The input is invalid. Please enter a valid sentence.")
        return
    
    # Process the text and make it magical
    epic_text = process_text(clean_input)
    
    print("Original cleaned text:", clean_input)
    print("Epic magical text:", epic_text)

# Run the application
if __name__ == "__main__":
    main()
