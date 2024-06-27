import os
import openai
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Set the OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

def parse_codebase(repo_data):
    code_structure = {}
    logger.debug("Parsing codebase...")
    # Assuming `repo_data` is a dictionary containing file paths as keys and file contents as values
    for file_path, file_content in repo_data.items():
        if file_path.endswith('.py'):  # or other relevant extensions
            logger.debug(f"Processing file: {file_path}")
            code_structure[file_path] = file_content
    return code_structure

def understand_code(code_snippet):
    logger.debug("Calling OpenAI API to understand code...")
    response = openai.Completion.create(
        engine="gpt-4-turbo",
        prompt=f"Explain what the following code does:\n\n{code_snippet}",
        max_tokens=150
    )
    logger.debug(f"OpenAI API response: {response}")
    return response.choices[0].text.strip()
