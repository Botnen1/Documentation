import os
import ast

def extract_definitions(source_code):
    definitions = {'class': [], 'function': [], 'variable': []}

    try:
        tree = ast.parse(source_code)

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = {'name': node.name, 'docstring': ast.get_docstring(node), 'bases': [base.id for base in node.bases if isinstance(base, ast.Name)], 'attributes': [], 'lineno': node.lineno}
                for body_item in node.body:
                    if isinstance(body_item, ast.Assign):
                        for target in body_item.targets:
                            if isinstance(target, ast.Name):
                                class_info['attributes'].append(target.id)
                definitions['class'].append(class_info)

            elif isinstance(node, ast.FunctionDef):
                func_info = {'name': node.name, 'docstring': ast.get_docstring(node), 'params': [], 'lineno': node.lineno}
                for arg in node.args.args:
                    if arg.annotation:
                        param = f"{arg.arg}: {ast.unparse(arg.annotation)}"
                    else:
                        param = arg.arg
                    if arg.default:
                        param += f" = {ast.unparse(arg.default)}"
                    func_info['params'].append(param)
                definitions['function'].append(func_info)

            elif isinstance(node, ast.Assign):
                # Variables may be assigned on multiple lines, so we take the first occurrence.
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id not in definitions['variable']:
                        definitions['variable'].append({'name': target.id, 'lineno': target.lineno})

    except Exception as e:
        print(f"Error extracting definitions: {e}")
        definitions = None

    return definitions

def generate_documentation():
    folder_path = os.getcwd()
    output_folder = folder_path
    all_docs_file_path = os.path.join(output_folder, 'generated_documentation.md')

    with open(all_docs_file_path, 'w') as all_docs_file:
        all_docs_file.write('# All Functions, Classes, and Variables\n\n')

        for filename in os.listdir(folder_path):
            if filename.endswith('.py') and filename != 'auto_doc.py':
                file_path = os.path.join(folder_path, filename)
                try:
                    with open(file_path, 'r') as file:
                        source_code = file.read()
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    continue

                definitions = extract_definitions(source_code)
                if definitions:
                    all_docs_file.write(f"## {filename}\n\n")
                    for def_type, items in definitions.items():
                        if items:
                            all_docs_file.write(f"### {def_type.capitalize()}\n\n")
                            for item in items:
                                if def_type == 'class':
                                    all_docs_file.write(f"- **Class:** {item['name']} (Line {item['lineno']})\n  - **Attributes:** {', '.join(item['attributes'])}\n  - **Docstring:** {item['docstring']}\n\n")
                                elif def_type == 'function':
                                    all_docs_file.write(f"- **Function:** {item['name']} (Line {item['lineno']})\n  - **Parameters:** {', '.join(item['params'])}\n  - **Docstring:** {item['docstring']}\n\n")
                                else:
                                    all_docs_file.write(f"- **Variable:** {item['name']} (Line {item['lineno']})\n")
                            all_docs_file.write("\n")

generate_documentation()
