import pyautogui
import time

def type_with_delay(text, delay=0.05):
    """
    Types text one character at a time with a delay between each character.
    Handles special characters properly to avoid unwanted spaces.
    
    Args:
        text (str): The text to type
        delay (float): Delay in seconds between each character (default: 0.05)
    """
    # Give you time to click where you want to type
    print("You have 5 seconds to click where you want to type...")
    time.sleep(5)
    
    print("Starting to type...")
    
    # Special key mappings
    special_keys = {
        '\n': 'enter',
        '\t': 'tab',
    }
    
    # Type each character with delay
    for char in text:
        if char in special_keys:
            # Handle special keys
            pyautogui.press(special_keys[char])
        elif char == ' ':
            # Handle space explicitly
            pyautogui.press('space')
        else:
            # For regular characters, use press with the character
            try:
                pyautogui.press(char)
            except:
                # If press fails, try typewrite as fallback
                pyautogui.typewrite(char)
        
        time.sleep(delay)
    
    print("\nTyping completed!")

# Example usage
if __name__ == "__main__":
    # Read the text from the file
    with open('text.txt', 'r', encoding='utf-8') as f:
        paragraph = f.read()
    
    # Adjust delay as needed (in seconds)
    typing_delay = 0.03  # 30 milliseconds between each character
    
    type_with_delay(paragraph, typing_delay)