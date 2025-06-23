from utils.explainer import get_blockwise_explanation, get_full_explanation, _remove_markdown
from utils.renderer import CodeRenderer
from utils.tts import generate_audio_for_explanation
from utils.video import create_explanation_video, concatenate_videos
import sys
import os
import shutil

def save_explanation_to_file(code_file_path, explanation_type, content):
    base_path = code_file_path.rsplit('.', 1)[0]  
    base_path = base_path.replace('/', '_').replace('\\', '_')  
    output_file = f"./output/text/{base_path}_{explanation_type}.txt"
    
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return output_file

def cleanup_temp_frames():
    temp_frames_dir = "./temp/frames"
    if os.path.exists(temp_frames_dir):
        shutil.rmtree(temp_frames_dir)
        os.makedirs(temp_frames_dir)

def cleanup_temp_audio():
    temp_audio_dir = "./temp/audio"
    if os.path.exists(temp_audio_dir):
        shutil.rmtree(temp_audio_dir)
        os.makedirs(temp_audio_dir)

def cleanup_temp_videos():
    temp_video_dir = "./temp/video"
    if os.path.exists(temp_video_dir):
        shutil.rmtree(temp_video_dir)
        os.makedirs(temp_video_dir)

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <code_file_path> <explanation_type>")
        print("explanation_type: 'summary', 'blockwise', or 'full' (combines summary and blockwise)")
        sys.exit(1)

    code_file_path = sys.argv[1]
    explanation_type = sys.argv[2].lower()

    try:
        with open(code_file_path, 'r', encoding='utf-8') as file:
            code = file.read()
    except FileNotFoundError:
        print(f"Error: File '{code_file_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    cleanup_temp_frames()
    cleanup_temp_audio()
    cleanup_temp_videos()
    
    renderer = CodeRenderer()
    temp_frames_dir = "./temp/frames"
    base_name = os.path.splitext(os.path.basename(code_file_path))[0]
    
    if explanation_type == 'summary':
        explanation = get_full_explanation(code)
        clean_explanation = _remove_markdown(explanation)
        output_file = save_explanation_to_file(code_file_path, 'summary', clean_explanation)
        print(f"\nFull code summary saved to: {output_file}")
        
        print("\nGenerating video frames...")
        num_frames = renderer.render_code_blocks(code, temp_frames_dir, mode='summary')
        print(f"Generated {num_frames} frames")
        
        print("\nGenerating audio narration...")
        audio_files = generate_audio_for_explanation(clean_explanation, r"temp\audio")
        print(f"Generated {len(audio_files)} audio segments")

        video_output_path = f"./output/video/{base_name}_summary.mp4"
        if os.path.exists(video_output_path):
            print(f"Warning: Video file '{video_output_path}' already exists. It will be overwritten.")
            os.remove(video_output_path)
        os.makedirs(os.path.dirname(video_output_path), exist_ok=True)
        
        print("\nCreating video...")
        success = create_explanation_video(temp_frames_dir, audio_files, video_output_path)
        if success:
            print(f"Video successfully created and saved to: {video_output_path}")
        else:
            print("Error: Failed to create video")
            sys.exit(1)
        
    elif explanation_type == 'blockwise':
        explanations = get_blockwise_explanation(code)
        formatted_content = []
        
        for block_type, blocks in explanations.items():
            formatted_content.append(f"\n{block_type.upper()}:")
            formatted_content.append("-" * 30)
            for block in blocks:
                formatted_content.append(f"\n{block['header']}")
                formatted_content.append(_remove_markdown(block['explanation']))
                formatted_content.append("-" * 20)
        
        formatted_text = '\n'.join(formatted_content)
        output_file = save_explanation_to_file(code_file_path, 'blockwise', formatted_text)
        print(f"\nBlockwise code explanation saved to: {output_file}")
        
        print("\nGenerating video frames...")
        num_frames = renderer.render_code_blocks(code, temp_frames_dir, mode='blockwise')
        print(f"Generated {num_frames} frames")
        
        print("\nGenerating audio narration...")
        audio_files = generate_audio_for_explanation(formatted_text, r"temp\audio")
        print(f"Generated {len(audio_files)} audio segments")        
        video_output_path = f"./output/video/{base_name}_blockwise.mp4"
        os.makedirs(os.path.dirname(video_output_path), exist_ok=True)
        
        print("\nCreating video...")
        success = create_explanation_video(temp_frames_dir, audio_files, video_output_path)
        if success:
            print(f"Video successfully created and saved to: {video_output_path}")
        else:
            print("Error: Failed to create video")
            sys.exit(1)
        
    elif explanation_type == 'full':
        summary_explanation = get_full_explanation(code)
        clean_summary = _remove_markdown(summary_explanation)
        
        blockwise_explanations = get_blockwise_explanation(code)
        formatted_content = []
        for block_type, blocks in blockwise_explanations.items():
            formatted_content.append(f"\n{block_type.upper()}:")
            formatted_content.append("-" * 30)
            for block in blocks:
                formatted_content.append(f"\n{block['header']}")
                formatted_content.append(_remove_markdown(block['explanation']))
                formatted_content.append("-" * 20)
        formatted_blockwise = '\n'.join(formatted_content)
        
        full_explanation = f"Code Summary:\n{'-' * 30}\n{clean_summary}\n\nDetailed Breakdown:\n{'-' * 30}\n{formatted_blockwise}"
        output_file = save_explanation_to_file(code_file_path, 'full', full_explanation)
        print(f"\nFull code explanation saved to: {output_file}")
        
        print("\nCreating summary video...")
        summary_frames_dir = "./temp/frames_summary"
        cleanup_temp_frames()
        os.makedirs(summary_frames_dir, exist_ok=True)
        
        print("Generating summary video frames...")
        num_summary_frames = renderer.render_code_blocks(code, summary_frames_dir, mode='summary')
        print(f"Generated {num_summary_frames} summary frames")
        
        print("Generating summary audio narration...")
        summary_audio_dir = "./temp/audio_summary"
        os.makedirs(summary_audio_dir, exist_ok=True)
        summary_audio_files = generate_audio_for_explanation(clean_summary, summary_audio_dir)
        print(f"Generated {len(summary_audio_files)} summary audio segments")
        
        summary_video_path = f"./temp/video/{base_name}_summary_temp.mp4"
        os.makedirs(os.path.dirname(summary_video_path), exist_ok=True)
        
        success_summary = create_explanation_video(summary_frames_dir, summary_audio_files, summary_video_path)
        if not success_summary:
            print("Error: Failed to create summary video")
            sys.exit(1)
        print("Summary video created successfully")
        
        print("\nCreating blockwise video...")
        blockwise_frames_dir = "./temp/frames_blockwise"
        if os.path.exists(blockwise_frames_dir):
            shutil.rmtree(blockwise_frames_dir)
        os.makedirs(blockwise_frames_dir, exist_ok=True)
        
        print("Generating blockwise video frames...")
        num_blockwise_frames = renderer.render_code_blocks(code, blockwise_frames_dir, mode='blockwise')
        print(f"Generated {num_blockwise_frames} blockwise frames")
        
        print("Generating blockwise audio narration...")
        blockwise_audio_dir = "./temp/audio_blockwise"
        if os.path.exists(blockwise_audio_dir):
            shutil.rmtree(blockwise_audio_dir)
        os.makedirs(blockwise_audio_dir, exist_ok=True)
        blockwise_audio_files = generate_audio_for_explanation(formatted_blockwise, blockwise_audio_dir)
        print(f"Generated {len(blockwise_audio_files)} blockwise audio segments")
        
        blockwise_video_path = f"./temp/video/{base_name}_blockwise_temp.mp4"
        
        success_blockwise = create_explanation_video(blockwise_frames_dir, blockwise_audio_files, blockwise_video_path)
        if not success_blockwise:
            print("Error: Failed to create blockwise video")
            sys.exit(1)
        print("Blockwise video created successfully")

        print("\nConcatenating videos...")
        video_output_path = f"./output/video/{base_name}_full.mp4"
        if os.path.exists(video_output_path):
            print(f"Warning: Video file '{video_output_path}' already exists. It will be overwritten.")
            os.remove(video_output_path)
        os.makedirs(os.path.dirname(video_output_path), exist_ok=True)
        
        success_concat = concatenate_videos([summary_video_path, blockwise_video_path], video_output_path)
        if success_concat:
            print(f"Full video successfully created and saved to: {video_output_path}")
            try:
                if os.path.exists(summary_video_path):
                    os.remove(summary_video_path)
                if os.path.exists(blockwise_video_path):
                    os.remove(blockwise_video_path)
                if os.path.exists(summary_frames_dir):
                    shutil.rmtree(summary_frames_dir)
                if os.path.exists(blockwise_frames_dir):
                    shutil.rmtree(blockwise_frames_dir)
                if os.path.exists(summary_audio_dir):
                    shutil.rmtree(summary_audio_dir)
                if os.path.exists(blockwise_audio_dir):
                    shutil.rmtree(blockwise_audio_dir)
            except Exception as e:
                print(f"Warning: Could not clean up temporary files: {e}")
        else:
            print("Error: Failed to concatenate videos")
            sys.exit(1)
        
    else:
        print("Error: explanation_type must be either 'summary', 'blockwise', or 'full'")
        sys.exit(1)

    cleanup_temp_frames()
    cleanup_temp_audio()

if __name__ == "__main__":
    main()
