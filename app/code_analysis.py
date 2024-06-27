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
        logger.debug(f"Parsing content for path: {path}")
        code_structure[path] = content  # Store raw content first
    return code_structure

def understand_code(code_snippet):
    logger.debug("Calling OpenAI API to understand code...")
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": f"Explain what the following code does:\n\n{code_snippet}"}],
        max_tokens=150
    )
    logger.debug(f"OpenAI API response: {response}")
    return response.choices[0].message.content.strip()
