import os
from .parser import PythonCodeParser
from langchain_google_genai import ChatGoogleGenerativeAI
import time
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)


def _explain_with_retry(prompt, max_retries=5, delay=10):
    retries = 0
    while retries < max_retries:
        try:
            response = llm.invoke(prompt)
            if hasattr(response, 'content'):
                return response.content
            return str(response)
        except Exception as e:
            print(f"Error during explanation: {e}")
            if 'rate limit' in str(e).lower() or '429' in str(e):
                time.sleep(delay)
            else:
                time.sleep(2)
            retries += 1
    return 'Explanation could not be generated due to repeated errors.'


def get_blockwise_explanation(code):
    parser = PythonCodeParser(code)
    blocks = parser.get_logical_parts()
    
    # Split the input code into lines for extracting snippets later
    code_lines = code.splitlines()
    
    all_blocks = []
    for block_type, block_list in blocks.items():
        if not block_list:
            continue
        
        for block in block_list:
            if block_type == 'imports':
                line_num = block.get('line', 0) if 'line' in block else 0
            else:
                line_num = block.get('start_line', 0) or block.get('line', 0)
            
            all_blocks.append({
                'type': block_type,
                'line_num': line_num,
                'block': block
            })
    
    all_blocks.sort(key=lambda x: x['line_num'])
    
    explanations = {}
    for block_data in all_blocks:
        block_type = block_data['type']
        block = block_data['block']
        
        if block_type not in explanations:
            explanations[block_type] = []
            
        if block_type == 'imports':
            module = block.get('module', '')
            names = block.get('names', '')
            block_desc = f"Importing {module}" + (f" with {names}" if names else "")
            code_snippet = block.get('code', '')
        elif 'name' in block and block.get('code', '').strip():
            block_desc = f"{block_type[:-1].capitalize()} '{block['name']}' (lines {block['start_line']}-{block['end_line']})"
            code_snippet = block['code']
        elif block.get('type') == 'expr':
            code_snippet = block.get('code', '').strip()
            
            if not code_snippet and 'start_line' in block and 'end_line' in block:
                start = block['start_line']
                end = block['end_line']
                if isinstance(start, int) and isinstance(end, int) and 0 < start <= end <= len(code_lines):
                    code_snippet = '\n'.join(code_lines[start-1:end]).strip()
                    block_desc = f"Expression (lines {start}-{end})"
            elif not code_snippet:
                line_num = block.get('line', 'unknown')
                if isinstance(line_num, int) and 0 < line_num <= len(code_lines):
                    code_snippet = code_lines[line_num - 1].strip()
                    block_desc = f"Expression on line {line_num}"
            else:
                line_num = block.get('line', 'unknown')
                block_desc = f"Expression on line {line_num}"
            
            if not code_snippet:
                continue
                
        elif 'start_line' in block and 'end_line' in block and block.get('code', '').strip():
            block_desc = f"{block_type[:-1].capitalize()} (lines {block['start_line']}-{block['end_line']})"
            code_snippet = block['code']
        else:
            continue

        prompt = (
            f"You are an expert Python instructor. Provide a detailed, structured explanation for the following code block. "
            f"Do not include any code snippets or markdown formatting in your explanation."
            f"Do not criticize the code or its quality, just explain its purpose and functionality."
            f"Format your answer as: \n1. Block Overview\n2. Line-by-line Explanation\n\nBlock: {block_desc}\n\nCode:\n{code_snippet}\n"
        )
        explanation = _explain_with_retry(prompt)
        explanations[block_type].append({'header': block_desc, 'explanation': explanation})
        print(f"Generated explanation for {block_type}: {block_desc}")
    
    return explanations


def get_full_explanation(code):
    parser = PythonCodeParser(code)
    blocks = parser.get_logical_parts()
    context = ''
    for block_type, block_list in blocks.items():
        for block in block_list:
            if block_type == 'imports':
                context += f"{block.get('type', '')} import: {block.get('module', '')} {block.get('names', '')}\n"
            elif 'name' in block:
                context += f"{block_type[:-1].capitalize()} '{block['name']}' (lines {block['start_line']}-{block['end_line']}):\n{block['code']}\n\n"
            elif 'start_line' in block and 'end_line' in block:
                context += f"{block_type[:-1].capitalize()} (lines {block['start_line']}-{block['end_line']}):\n{block['code']}\n\n"
            else:
                context += str(block) + '\n'
    prompt = (
        "You are an expert Python instructor. Given the following code, provide a comprehensive, structured explanation that covers the overall purpose, how the blocks interact, and a summary of the logic."
        f"Do not include any code snippets or markdown formatting in your explanation."
        "Do not criticize the code or its quality, just explain its purpose and functionality."
        "Format your answer as: \n1. High-level Overview\n2. Block Interactions\n3. Step-by-step Logic\n4. Key Takeaways.\n\nFull Code Context:\n" + context 
    )
    explanation = _explain_with_retry(prompt)
    return explanation


def _remove_markdown(text):
    lines = []
    for line in text.split('\n'):
        if line.strip().startswith('#'):
            lines.append(line.lstrip('#').strip())
        else:
            lines.append(line)
    
    text = '\n'.join(lines)
    text = text.replace('**', '').replace('*', '')
    text = text.replace('__', '').replace('_', '')
    text = text.replace('`', '')
    
    lines = []
    for line in text.split('\n'):
        if line.strip() and line[0].isdigit() and '. ' in line:
            line = line.replace('. ', ') ', 1)
        lines.append(line)
    
    return '\n'.join(lines)
