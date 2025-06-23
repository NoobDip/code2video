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

def generate_audio_for_explanation(explanation_text, temp_dir=r"temp\audio", speed_factor=1.2):
    os.makedirs(temp_dir, exist_ok=True)
    
    for file in os.listdir(temp_dir):
        if file.endswith((".mp3", ".wav")):
            os.remove(os.path.join(temp_dir, file))
    
    print(f"Generating audio with speed factor: {speed_factor}")
    tts = TextToSpeech(speed_factor=speed_factor)
    chunks = split_into_chunks(explanation_text)
    print(f"Split text into {len(chunks)} chunks")
    
    audio_files = []
    for i, chunk in enumerate(chunks):
        output_path = os.path.join(temp_dir, f'audio_{i:04d}.wav')
        max_retries = 3
        for attempt in range(max_retries):
            if tts.create_audio(chunk, output_path):
                audio_files.append(output_path)
                break
            elif attempt < max_retries - 1:
                print(f"Retry {attempt + 1} for chunk {i}...")
                time.sleep(2)
        else:
            print(f"Warning: Failed to generate audio for chunk {i} after {max_retries} attempts")
    
    if not audio_files:
        raise Exception("No audio files were generated successfully")
    
    print(f"Successfully generated {len(audio_files)} audio files")
    return audio_files

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