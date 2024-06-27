from flask import Blueprint, request, jsonify
from .github_integration import fetch_github_repo_contents
from .code_analysis import parse_codebase
import logging
from openai import OpenAI
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

bp = Blueprint('main', __name__)

def summarize_file(path, code):
    try:
        summary = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": f"Provide a high-level overview of what the following code does and highlight important functions:\n\n{code}"}],
            max_tokens=500  # Reduced for quick summarization
        ).choices[0].message.content.strip()
        return path, summary
    except Exception as e:
        logger.error(f"Error summarizing file {path}: {e}")
        return path, ""

@bp.route('/quick_summarize_repo', methods=['POST'])
def quick_summarize_repo():
    repo_url = request.json['repo_url']
    owner, repo = repo_url.strip('/').split('/')[-2:]
    logger.debug("Received request to quick summarize repo: %s", repo_url)

    # Fetch and analyze code
    repo_data = fetch_github_repo_contents(owner, repo)
    logger.debug("Fetched repo data: %s", repo_data)
    
    if not repo_data:
        return jsonify({'error': 'No files found in the repository.'}), 404

    codebase = parse_codebase(repo_data)
    logger.debug("Parsed codebase: %s", codebase)

    quick_summaries = {}
    file_count = 0

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(summarize_file, path, code) for path, code in codebase.items() if file_count < 15]
        file_count += len(futures)

        for future in as_completed(futures):
            path, summary = future.result()
            if summary:
                quick_summaries[path] = summary

    with open('quick_repo_summary.txt', 'w') as file:
        for path, summary in quick_summaries.items():
            file.write(f"{path}:\n{summary}\n\n")

    logger.debug("Quick summary written to quick_repo_summary.txt")
    return jsonify({'message': 'Quick summary completed.', 'summary_file': 'quick_repo_summary.txt'})

