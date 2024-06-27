import os
from openai import OpenAI
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def parse_codebase(repo_data):
    code_structure = {}
    for file_path, file_content in repo_data.items():
        if not file_path.endswith('.gitignore'):
            code_structure[file_path] = file_content
    return code_structure

def understand_code_chunked(code_snippet):
    logger.debug("Calling OpenAI API to understand code in chunks...")
    chunk_size = 4096  # Ensure chunks are small enough to fit within max tokens limit
    chunks = [code_snippet[i:i + chunk_size] for i in range(0, len(code_snippet), chunk_size)]
    
    explanations = []
    for chunk in chunks:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": f"Provide a detailed summary of each function in the following code and explain how they relate to the rest of the application:\n\n{chunk}"}],
            max_tokens=4096  # Reduced to avoid hitting token limits in the response
        )
        explanations.append(response.choices[0].message.content.strip())
    return "\n".join(explanations)

def quick_understand_code_chunked(code_snippet):
    logger.debug("Calling OpenAI API to quickly understand code in chunks...")
    chunk_size = 4096  # Ensure chunks are small enough to fit within max tokens limit
    chunks = [code_snippet[i:i + chunk_size] for i in range(0, len(code_snippet), chunk_size)]
    
    explanations = []
    for chunk in chunks:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": f"Provide a high-level overview of what the following code does and highlight important functions:\n\n{chunk}"}],
            max_tokens=4096  # Reduced to avoid hitting token limits in the response
        )
        explanations.append(response.choices[0].message.content.strip())
    return "\n".join(explanations)

def extract_readme_context(repo_data):
    readme_context = ""
    for file_path, file_content in repo_data.items():
        if file_path.lower() == "readme.md":
            readme_context = file_content
            break
    return readme_context
