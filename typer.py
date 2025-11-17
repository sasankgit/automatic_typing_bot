import pyautogui
import time

def type_with_delay(text, delay=0.1):
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
    # Your paragraph here
    paragraph = """The only people for me are the mad ones, the ones who are mad to live, mad to talk, mad to be saved, desirous of everything at the same time, the ones who never yawn or say a commonplace thing, but burn, burn, burn, like fabulous yellow Roman candles exploding like spiders across the stars, and in the middle, you see the blue center-light pop, and everybody goes ahh..."""
    
    # Adjust delay as needed (in seconds)
    typing_delay = 0.05  # 50 milliseconds between each character
    
    type_with_delay(paragraph, typing_delay)