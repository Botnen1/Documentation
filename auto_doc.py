import os
import ast
import re

def extract_definitions(source_code):
    definitions = {'class': [], 'function': [], 'variable': []}

    try:
        tree = ast.parse(source_code)

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                docstring = ast.get_docstring(node)
                if docstring:
                    definitions['class'].append((node.name, docstring))

            elif isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node)
                if docstring:
                    definitions['function'].append((node.name, docstring))

            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        definitions['variable'].append(target.id)

    except Exception as e:
        print(f"Error extracting definitions: {e}")
        definitions = None

    return definitions

def generate_documentation():
    folder_path = os.getcwd() # Get the current directory
    output_folder = folder_path # Set the output folder to the current directory
    all_docs_file_path = os.path.join(output_folder, 'generated_documentation.txt')

    with open(all_docs_file_path, 'w') as all_docs_file:
        all_docs_file.write('# All functions and variables\n\n')

        for filename in os.listdir(folder_path):
            if filename != 'auto_doc.py':
                if filename.endswith('.py'):
                    file_path = os.path.join(folder_path, filename)
                    try:
                        with open(file_path, 'r') as file:
                            source_code = file.read()
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
                        continue

                    try:
                        definitions = extract_definitions(source_code)
                    except SyntaxError as e:
                        print(f"Syntax error in {file_path}: {e}")
                        continue

                    all_docs_file.write(f"## {filename}\n\n")
                    for def_type, names in definitions.items():
                        if names:
                            all_docs_file.write(f"### **{def_type}**\n\n")
                            for name in names:
                                all_docs_file.write(f"- {name}\n")
                            all_docs_file.write("\n")
                        
generate_documentation()