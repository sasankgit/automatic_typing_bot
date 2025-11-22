import pyaudio
import wave
import json
import urllib.request
import urllib.error

def record_audio(filename="temp_audio.wav", duration=5, sample_rate=16000):
    """Record audio from microphone"""
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    
    p = pyaudio.PyAudio()
    
    print("Recording... Speak now!")
    
    stream = p.open(format=format,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk)
    
    frames = []
    
    for i in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    
    print("Recording finished!")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # Save audio to file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    return filename

def speech_to_text_google(audio_file):
    """Convert speech to text using Google Speech API"""
    try:
        # Read audio file
        with open(audio_file, 'rb') as f:
            audio_data = f.read()
        
        # Google Speech API endpoint
        url = "http://www.google.com/speech-api/v2/recognize?output=json&lang=en-us&key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"
        
        headers = {'Content-Type': 'audio/l16; rate=16000;'}
        
        request = urllib.request.Request(url, data=audio_data, headers=headers)
        response = urllib.request.urlopen(request)
        
        response_text = response.read().decode('utf-8')
        
        # Parse response (may contain multiple JSON objects)
        for line in response_text.split('\n'):
            if line.strip():
                try:
                    result = json.loads(line)
                    if 'result' in result and len(result['result']) > 0:
                        if 'alternative' in result['result'][0]:
                            transcript = result['result'][0]['alternative'][0]['transcript']
                            return transcript
                except json.JSONDecodeError:
                    continue
        
        return None
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("=== Speech to Text Converter ===\n")
    
    while True:
        try:
            # Record audio
            audio_file = record_audio(duration=5)
            
            print("Processing speech...")
            
            # Convert to text
            text = speech_to_text_google(audio_file)
            
            if text:
                print(f"\nYou said: {text}")
            else:
                print("Could not understand the audio or no speech detected.")
            
        except Exception as e:
            print(f"Error occurred: {e}")
        
        # Ask if user wants to continue
        print("\nPress Enter to speak again, or type 'quit' to exit: ")
        user_input = input().strip().lower()
        
        if user_input == 'quit':
            print("Goodbye!")
            break
        print("\n" + "="*40 + "\n")