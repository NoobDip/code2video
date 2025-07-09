import os
import pyttsx3
import time
from pydub import AudioSegment

class TextToSpeech:
    def __init__(self, speed_factor=1.2):
        self.speed_factor = speed_factor
        try:
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if "english" in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    print(f"Selected voice: {voice.name}")
                    break
            base_rate = 175
            self.engine.setProperty('rate', int(base_rate))
            self.engine.setProperty('volume', 0.9)  
        except Exception as e:
            print(f"Error: Could not initialize TTS engine: {e}")
            raise e
    
    def create_audio(self, text, output_path):
        try:
            output_path = output_path.replace('.mp3', '.wav')
            
            text = text.replace('\n\n', '. ').replace('\n', ', ')
            
            self.engine.save_to_file(text, output_path)
            self.engine.runAndWait()
            
            if not os.path.exists(output_path):
                print(f"Error: Output file was not created: {output_path}")
                return False
                
            if os.path.getsize(output_path) == 0:
                print(f"Error: Output file is empty: {output_path}")
                os.remove(output_path)
                return False
                
            return True
        except Exception as e:
            print(f"Error: TTS failed: {e}")
            if os.path.exists(output_path):
                os.remove(output_path)
            return False

import os
from gtts import gTTS

def generate_audio_for_explanation(text, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "output.mp3")
    tts = gTTS(text)
    tts.save(output_path)
    return [output_path]

def split_into_chunks(text, max_chunk_size=500):
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = []
    current_size = 0
    
    for paragraph in paragraphs:
        lines = paragraph.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            line_size = len(line)
            
            if current_size + line_size > max_chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_size = 0
            
            current_chunk.append(line)
            current_size += line_size + 1  
            if line == lines[-1]:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = []
                    current_size = 0
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return [chunk.strip() for chunk in chunks if chunk.strip()]