import os
from openai import OpenAI
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def parse_codebase(repo_data):
    code_structure = {}
    # Parse codebase logic
    return code_structure

def understand_code(code_snippet):
    logger.debug("Calling OpenAI API to understand code...")
    response = client.completions.create(
        engine="gpt-4-turbo",
        prompt=f"Explain what the following code does:\n\n{code_snippet}",
        max_tokens=150
    )
    logger.debug(f"OpenAI API response: {response}")
    return response.choices[0].text.strip()

# Example usage:
if __name__ == "__main__":
    test_code = "def hello_world(): print('Hello, world!')"
    explanation = understand_code(test_code)
    print(explanation)
