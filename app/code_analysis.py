import os
from openai import OpenAI
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Instantiate the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def parse_codebase(repo_data):
    code_structure = {}
    for path, content in repo_data.items():
        if path == ".gitignore":
            continue  # Ignore .gitignore files
        logger.debug(f"Parsing content for path: {path}")
        code_structure[path] = content  # Store raw content first
    return code_structure

def understand_code(code_snippet):
    logger.debug("Calling OpenAI API to understand code...")
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": f"Explain what the following code does:\n\n{code_snippet}"}],
        max_tokens=8192  # Set to the maximum allowable amount
    )
    logger.debug(f"OpenAI API response: {response}")
    return response.choices[0].message.content.strip()

def extract_readme_context(repo_data):
    readme_content = repo_data.get('README.md', '')
    if readme_content:
        logger.debug("Using README.md to understand context...")
        context_response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": f"Summarize the following README.md content:\n\n{readme_content}"}],
            max_tokens=8192
        )
        logger.debug(f"OpenAI API response for README.md: {context_response}")
        return context_response.choices[0].message.content.strip()
    return "No README.md found in the repository."
