import openai
import os

def parse_codebase(repo_data):
    if not isinstance(repo_data, dict):
        raise ValueError("Expected dictionary input for repo_data")
    
    codebase = {}
    for file_info in repo_data.get('files', []):
        path = file_info.get('path')
        content = file_info.get('content')
        if path and content:
            codebase[path] = content
    
    return codebase

def analyze_code_with_openai(codebase):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    code_explanations = {}
    
    for path, code in codebase.items():
        response = openai.Completion.create(
            engine="davinci-codex",
            prompt=f"Analyze the following code and provide a detailed explanation:\n\n{code}",
            max_tokens=150,
            temperature=0.5
        )
        explanation = response.choices[0].text.strip()
        code_explanations[path] = explanation
    
    return code_explanations
