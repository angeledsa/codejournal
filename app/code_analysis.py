import os

def parse_codebase(repo_path):
    code_structure = {}
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py'):  # or other relevant extensions
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    code_structure[file_path] = f.read()
    return code_structure

import openai

def understand_code(code_snippet):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Explain what the following code does:\n\n{code_snippet}",
        max_tokens=150
    )
    return response.choices[0].text.strip()
