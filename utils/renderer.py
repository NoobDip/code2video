import os
from PIL import Image, ImageDraw, ImageFont
import pygments
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter
from pygments.styles.monokai import MonokaiStyle
import textwrap
from .parser import PythonCodeParser

class CodeRenderer:
    def __init__(self, width=1920, height=1080, font_size=32, 
                 bg_color=(40, 44, 52), font_color=(255, 255, 255)):
        self.width = width
        self.height = height
        self.font_size = font_size
        self.bg_color = bg_color
        self.font_color = font_color
        
        try:
            windows_fonts = "C:/Windows/Fonts"
            if os.path.exists(os.path.join(windows_fonts, "arial.ttf")):
                self.font = ImageFont.truetype(os.path.join(windows_fonts, "arial.ttf"), self.font_size)
            elif os.path.exists(os.path.join(windows_fonts, "segoeui.ttf")):
                self.font = ImageFont.truetype(os.path.join(windows_fonts, "segoeui.ttf"), self.font_size)
            else:
                self.font = ImageFont.load_default()
                
            if os.path.exists(os.path.join(windows_fonts, "consola.ttf")):
                self.code_font = ImageFont.truetype(os.path.join(windows_fonts, "consola.ttf"), self.font_size)
            elif os.path.exists(os.path.join(windows_fonts, "cour.ttf")):
                self.code_font = ImageFont.truetype(os.path.join(windows_fonts, "cour.ttf"), self.font_size)
            else:
                self.code_font = ImageFont.load_default()
        except Exception as e:
            print(f"Warning: Could not load system fonts, falling back to defaults. Error: {e}")
            self.font = ImageFont.load_default()
            self.code_font = ImageFont.load_default()
        
    def create_frame(self, text, code_snippet=None, highlight_lines=None):
        img = Image.new('RGB', (self.width, self.height), self.bg_color)
        draw = ImageDraw.Draw(img)
        
        if code_snippet:
            formatter = ImageFormatter(
                style=MonokaiStyle,
                line_numbers=True,
                line_pad=3,
                font_size=self.font_size,
                line_number_chars=4
            )
            highlighted = pygments.highlight(
                code_snippet,
                PythonLexer(),
                formatter
            )           
            temp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp")
            os.makedirs(temp_dir, exist_ok=True)
            temp_file = os.path.join(temp_dir, "temp_highlight.png")
            try:
                with open(temp_file, "wb") as f:
                    f.write(highlighted)
                code_img = Image.open(temp_file)
                code_img = code_img.convert('RGBA')
                code_img_copy = code_img.copy()
                code_img.close()
            finally:
                try:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                except Exception as e:
                    print(f"Warning: Could not remove temporary file: {e}")
            
            code_img = code_img_copy  
            code_x = (self.width - code_img.width) // 2
            code_y = (self.height - code_img.height) // 2
            
            img.paste(code_img, (code_x, code_y))
            
            if highlight_lines:
                line_height = self.font_size + 6  
                for line_num in highlight_lines:
                    y = code_y + (line_num - 1) * line_height
                    draw.rectangle(
                        [(code_x, y), (code_x + code_img.width, y + line_height)],
                        fill=(60, 64, 72),
                        outline=None
                    )
        
        if text:
            wrapped_text = textwrap.wrap(text, width=50)
            y = self.height - (len(wrapped_text) * (self.font_size + 10)) - 50
            for line in wrapped_text:
                text_bbox = draw.textbbox((0, 0), line, font=self.font)
                text_width = text_bbox[2] - text_bbox[0]
                x = (self.width - text_width) // 2
                draw.text((x, y), line, font=self.font, fill=self.font_color)
                y += self.font_size + 10
                
        return img

    def _get_block_content(self, block_type, block):
        if block_type == 'imports':
            module_name = block.get('module', '')
            names = block.get('names', '')
            text = f"Import statement: {module_name}"
            if isinstance(names, list):
                text += f" {', '.join(names)}"
            elif names:
                text += f" {names}"
            code_snippet = f"import {module_name}" if not names else f"from {module_name} import {names}"
        elif 'name' in block:
            text = f"Analyzing {block_type[:-1]}: {block['name']}"
            code_snippet = block.get('code', '')
        else:
            text = f"Analyzing {block_type[:-1]}"
            code_snippet = block.get('code', '')
            
        return text, code_snippet

    def render_summary_code(self, code, output_dir):
        lines = code.split('\n')
        chunks = []
        current_chunk = []
        
        for line in lines:
            current_chunk.append(line)
            if len(current_chunk) >= 10:  
                chunks.append('\n'.join(current_chunk))
                current_chunk = current_chunk[5:]  

        if current_chunk:
            chunks.append('\n'.join(current_chunk))
        
        frame_count = 0
        for i, chunk in enumerate(chunks):
            frame = self.create_frame(
                text=f"Code Walkthrough ({i+1}/{len(chunks)})",
                code_snippet=chunk
            )
            frame.save(os.path.join(output_dir, f'frame_{frame_count:04d}.png'))
            frame_count += 1
        
        return frame_count

    def render_code_blocks(self, code, output_dir, mode='blockwise', start_frame=0):
        if mode == 'summary':
            return self.render_summary_code(code, output_dir)
            
        parser = PythonCodeParser(code)
        blocks = parser.get_logical_parts()
        frame_count = start_frame

        if mode == 'blockwise':
            all_blocks = []
            for block_type, block_list in blocks.items():
                if not block_list:
                    continue
                
                for block in block_list:
                    if block_type == 'imports':
                        line_num = block.get('line', 0) if 'line' in block else 0
                    else:
                        line_num = block.get('start_line', 0)
                    
                    all_blocks.append({
                        'type': block_type,
                        'line_num': line_num,
                        'block': block
                    })
            
            all_blocks.sort(key=lambda x: x['line_num'])
            
            current_type = None
            code_lines = code.splitlines()
            
            for block_data in all_blocks:
                block_type = block_data['type']
                block = block_data['block']
                
                if current_type != block_type:
                    title_frame = self.create_frame(f"{block_type.upper()}", None)
                    title_frame.save(os.path.join(output_dir, f'frame_{frame_count:04d}.png'))
                    frame_count += 1
                    current_type = block_type
                
                if block_type == 'imports':
                    code_snippet = f"# {block.get('type', '')} import: {block.get('module', '')} {block.get('names', '')}"
                    text = "Import Statement"
                elif 'name' in block:
                    code_snippet = block.get('code', '').strip()
                    text = f"{block_type[:-1].capitalize()} '{block['name']}'"
                elif block.get('type') == 'expr':
                    code_snippet = block.get('code', '').strip()
                    
                    if not code_snippet and 'start_line' in block and 'end_line' in block:
                        start = block['start_line']
                        end = block['end_line']
                        if isinstance(start, int) and isinstance(end, int) and 0 < start <= end <= len(code_lines):
                            code_snippet = '\n'.join(code_lines[start-1:end]).strip()
                            text = f"Expression (lines {start}-{end})"
                    elif not code_snippet:
                        line_num = block.get('line', 'unknown')
                        if isinstance(line_num, int) and 0 < line_num <= len(code_lines):
                            code_snippet = code_lines[line_num - 1].strip()
                            text = f"Expression on line {line_num}"
                    else:
                        line_num = block.get('line', 'unknown')
                        text = f"Expression on line {line_num}"
                else:
                    code_snippet = block.get('code', '').strip()
                    text = f"{block_type[:-1].capitalize()}"
                
                if not code_snippet:
                    continue
                
                frame = self.create_frame(text, code_snippet)
                frame.save(os.path.join(output_dir, f'frame_{frame_count:04d}.png'))
                frame_count += 1
        
        return frame_count