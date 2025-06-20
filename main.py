from utils.explainer import get_blockwise_explanation, get_full_explanation, _remove_markdown
import sys
import os

def save_explanation_to_file(code_file_path, explanation_type, content):
    base_path = code_file_path.rsplit('.', 1)[0]  
    base_path = base_path.replace('/', '_').replace('\\', '_')  
    output_file = f"./temp/text/{base_path}_{explanation_type}.txt"
    
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return output_file

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <code_file_path> <explanation_type>")
        print("explanation_type: 'full' or 'blockwise'")
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

    if explanation_type == 'full':
        explanation = get_full_explanation(code)
        clean_explanation = _remove_markdown(explanation)
        output_file = save_explanation_to_file(code_file_path, 'full', clean_explanation)
        print(f"\nFull code explanation saved to: {output_file}")
        
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
        
        output_file = save_explanation_to_file(code_file_path, 'blockwise', '\n'.join(formatted_content))
        print(f"\nBlockwise code explanation saved to: {output_file}")
        
    else:
        print("Error: explanation_type must be either 'full' or 'blockwise'")
        sys.exit(1)

if __name__ == "__main__":
    main()
