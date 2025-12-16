import pyautogui
import time

def type_with_delay(text, delay=0.01):
    """
    Types text one character at a time with a delay between each character.
    
    Args:
        text (str): The text to type
        delay (float): Delay in seconds between each character (default: 0.1)
    """
    # Give you time to click where you want to type
    print("You have 5 seconds to click where you want to type...")
    time.sleep(5)
    
    # Type each character with delay
    for char in text:
        pyautogui.write(char, interval=0)  # Write without pyautogui's interval
        time.sleep(delay)
    
    print("\nTyping completed!")

# Example usage
if __name__ == "__main__":
    # Read the text from the file
    with open('text.txt', 'r') as f:
        paragraph = f.read()
    
    # Adjust delay as needed (in seconds)
    typing_delay = 0.05  # 50 milliseconds between each character
    
    type_with_delay(paragraph, typing_delay)