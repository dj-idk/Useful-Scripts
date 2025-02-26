import sys
import re

def convert_to_qa_format(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        content = infile.read().strip()
        entries = re.findall(r"(\w+):\s(.+?)\n*(?=\w+:|$)", content, re.DOTALL)
        
        for term, definition in entries:
            question = f"Q: What's {term} ?\n"
            answer = f"A: {definition.strip()}\n\n"
            outfile.write(question + answer)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input.txt output.txt")
        sys.exit(1)
    
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    convert_to_qa_format(input_filename, output_filename)
