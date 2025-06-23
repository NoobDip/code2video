import os
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy import concatenate_audioclips, concatenate_videoclips
from pydub import AudioSegment
import numpy as np

class VideoCreator:
    def __init__(self, frame_duration=5.0):
        self.frame_duration = frame_duration

    def get_audio_duration(self, audio_path):
        try:
            audio = AudioSegment.from_file(audio_path)
            return len(audio) / 1000.0
        except Exception as e:
            print(f"Error getting audio duration for {audio_path}: {e}")
            return None

    def create_video(self, frames_dir, audio_files, output_path):
        try:
            frames = sorted([os.path.join(frames_dir, f) for f in os.listdir(frames_dir) 
                           if f.endswith(('.png', '.jpg', '.jpeg'))])
            audio_files = sorted(audio_files)

            if not frames:
                raise ValueError("No frames found in the specified directory")

            total_audio_duration = sum(self.get_audio_duration(audio) for audio in audio_files)

            print("\nCreating video from frames...")
            if len(frames) == 1:
                frame_duration = total_audio_duration
                video_clip = ImageSequenceClip([frames[0]], durations=[frame_duration])
            else:
                frame_duration = total_audio_duration / len(frames)
                video_clip = ImageSequenceClip(frames, durations=[frame_duration] * len(frames))

            print("Processing audio files...")
            if len(audio_files) > 1:
                print("Concatenating multiple audio files...")
                combined = AudioSegment.empty()
                for audio_file in audio_files:
                    segment = AudioSegment.from_file(audio_file)
                    combined += segment
                
                temp_audio = os.path.join("temp", "audio", "temp_combined_audio.wav")
                combined.export(temp_audio, format='wav',
                              parameters=["-ar", "44100", "-ac", "1", "-acodec", "pcm_s16le"])
                  
                final_audio = AudioFileClip(temp_audio)
            else:
                final_audio = AudioFileClip(audio_files[0])
                temp_audio = None 
            print("Combining video and audio...")
            video_clip.audio = final_audio
            final_video = video_clip
            print("Writing final video file...")
            final_video.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio_codec='aac',
                preset='medium',
                audio_bitrate='192k',
                threads=4,
                logger=None
            )            
            video_clip.close()
            final_audio.close()
            
            if temp_audio and os.path.exists(temp_audio):
                try:
                    os.remove(temp_audio)
                except Exception as e:
                    print(f"Warning: Could not remove temporary audio file: {e}")
            
            return True

        except Exception as e:
            print(f"Error creating video: {e}")
            import traceback
            traceback.print_exc()
            return False

def create_explanation_video(frames_dir, audio_files, output_path, frame_duration=5.0):
    creator = VideoCreator(frame_duration=frame_duration)
    return creator.create_video(frames_dir, audio_files, output_path)