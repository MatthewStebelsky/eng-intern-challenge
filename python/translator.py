"""
Run this script with Python 3.

For Windows:
    Command: python translator.py <text>
    
For Linux/macOS:
    Command: python3 translator.py <text>
"""


braille_map = {
    # Braille letters mapping
    'a': 'O.....', 'b': 'O.O...', 'c': 'OO....', 'd': 'OO.O..', 'e': 'O..O..',
    'f': 'OOO...', 'g': 'OOOO..', 'h': 'O.OO..', 'i': '.OO...', 'j': '.OOO..',
    'k': 'O...O.', 'l': 'O.O.O.', 'm': 'OO..O.', 'n': 'OO.OO.', 'o': 'O..OO.',
    'p': 'OOO.O.', 'q': 'OOOOO.', 'r': 'O.OOO.', 's': '.OO.O.', 't': '.OOOO.',
    'u': 'O...OO', 'v': 'O.O.OO', 'w': '.OOO.O', 'x': 'OO..OO', 'y': 'OO.OOO', 'z': 'O..OOO',

    # Special Braille symbols
    'capital': '.....O',  # Capital letter indicator
    'number': '.O.OOO',   # Number indicator
    ' ': '......',        # Space
    '.': '..OO.O', ',': '..O...', '?': '..O.OO', '!': '..OOO.', ':': '..OO..',
    ';': '..O.O.', '-': '....OO', '/': '.O..O.', '(': 'O.O..O', ')': '.O.OO.'
}

# Braille digit mappings
digit_map = {
    '1': 'O.....', '2': 'O.O...', '3': 'OO....', '4': 'OO.O..', '5': 'O..O..',
    '6': 'OOO...', '7': 'OOOO..', '8': 'O.OO..', '9': '.OO...', '0': '.OOO..',
}

# Inverse mappings for decoding Braille
letter_english_map = {v: k for k, v in braille_map.items() if k.isalpha()}
digit_english_map = {v: k for k, v in digit_map.items()}
special_english_map = {v: k for k, v in braille_map.items() if k in ['capital', 'number', ' ']}

# Detect if input is Braille or English based on character set
def detect_input_type(input_str):
    if all(c in ['O', '.'] for c in input_str.replace(' ', '')):
        return 'braille'
    else:
        return 'english'

# Convert English text to Braille
def english_to_braille(text):
    braille_output = []
    is_number = False  # Track number mode
    for char in text:
        if char.isdigit():
            if not is_number:
                braille_output.append(braille_map['number'])  # Add number indicator
                is_number = True
            braille_output.append(digit_map[char])
        else:
            if is_number:
                is_number = False  # Exit number mode
            if char.isupper():
                braille_output.append(braille_map['capital'])  # Add capital indicator
                braille_output.append(braille_map[char.lower()])
            elif char == ' ':
                braille_output.append(braille_map[' '])  # Add space
            else:
                braille_output.append(braille_map[char])
    return ''.join(braille_output)

# Convert Braille text to English
def braille_to_english(braille_text):
    english_output = []
    is_capital = False  # Track capital letters
    is_number = False   # Track number mode
    i = 0
    length = len(braille_text)

    while i < length:
        braille_char = braille_text[i:i+6]

        if braille_char == braille_map['capital']:
            is_capital = True  # Activate capital letter mode
            i += 6
            continue
        elif braille_char == braille_map['number']:
            is_number = True  # Activate number mode
            i += 6
            continue
        elif braille_char == braille_map[' ']:
            english_output.append(' ')  # Add space
            is_number = False  # Reset number mode after space
            i += 6
            continue
        else:
            if is_number:
                char = digit_english_map.get(braille_char, '')  # Translate digits
                if not char:
                    is_number = False  # End number mode if no match
                    char = letter_english_map.get(braille_char, '')
            else:
                char = letter_english_map.get(braille_char, '')  # Translate letters

            if is_capital and char:
                char = char.upper()  # Capitalize the letter
                is_capital = False

            if char:
                english_output.append(char)
            else:
                english_output.append('?')  # Handle unknown Braille patterns
            i += 6
    return ''.join(english_output)

import sys

# Main function to handle command line input
def main():
    if len(sys.argv) < 2:
        print("Error: Please provide a string to translate.")
        print("Usage: python translator.py <text> for Windows or python3 translator.py <text> for Linux/macOS")
        return

    # Concatenate input arguments to handle spaces in input
    input_text = ' '.join(sys.argv[1:])

    input_type = detect_input_type(input_text)

    if input_type == 'english':
        print(english_to_braille(input_text))
    elif input_type == 'braille':
        print(braille_to_english(input_text))
    else:
        print("Invalid input.")

if __name__ == "__main__":
    main()
