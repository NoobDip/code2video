from parser import PythonCodeParser
from langchain.chat_models import ChatGoogleGenerativeAI
import time

llm = ChatGoogleGenerativeAI(temperature=0)


def _explain_with_retry(prompt, max_retries=5, delay=10):
    retries = 0
    while retries < max_retries:
        try:
            response = llm([{ 'role': 'user', 'content': prompt }])
            if isinstance(response, list) and response and 'content' in response[0]:
                return response[0]['content']
            if isinstance(response, str):
                return response
            retries += 1
        except Exception as e:
            if 'rate limit' in str(e).lower() or '429' in str(e):
                time.sleep(delay)
                retries += 1
            else:
                time.sleep(2)
                retries += 1
    return 'Explanation could not be generated due to repeated errors.'


def get_blockwise_explanation(code):
    parser = PythonCodeParser(code)
    blocks = parser.get_logical_parts()
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
