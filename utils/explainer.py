import os
from .parser import PythonCodeParser
from langchain_google_genai import ChatGoogleGenerativeAI
import time
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
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
    print("Extracted logical blocks:", blocks)
    explanations = {}
    for block_type, block_list in blocks.items():
        explanations[block_type] = []
        for block in block_list:
            if block_type == 'imports':
                block_desc = f"{block.get('type', '')} import: {block.get('module', '')} {block.get('names', '')}"
                code_snippet = ''
            elif 'name' in block:
                block_desc = f"{block_type[:-1].capitalize()} '{block['name']}' (lines {block['start_line']}-{block['end_line']})"
                code_snippet = block['code']
            elif 'start_line' in block and 'end_line' in block:
                block_desc = f"{block_type[:-1].capitalize()} (lines {block['start_line']}-{block['end_line']})"
                code_snippet = block['code']
            else:
                block_desc = str(block)
                code_snippet = ''
            prompt = (
                f"You are an expert Python instructor. Provide a detailed, structured, and line-by-line explanation for the following code block. "
                f"Format your answer as: \n1. Block Overview\n2. Line-by-line Explanation (with line numbers)\n3. Key Concepts.\n\nBlock: {block_desc}\n\nCode:\n{code_snippet}\n"
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
        "You are an expert Python instructor. Given the following code, provide a comprehensive, structured explanation that covers the overall purpose, how the blocks interact, and a summary of the logic. "
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
