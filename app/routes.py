import os
from flask import Blueprint, request, jsonify
from .github_integration import fetch_github_repo_contents
from .code_analysis import parse_codebase, understand_code_chunked
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bp = Blueprint('main', __name__)

@bp.route('/summarize_repo', methods=['POST'])
def summarize_repo():
    repo_url = request.json['repo_url']
    owner, repo = repo_url.strip('/').split('/')[-2:]
    logger.debug("Received request to summarize repo: %s", repo_url)

    # Fetch and analyze code
    repo_data = fetch_github_repo_contents(owner, repo)
    logger.debug("Fetched repo data: %s", repo_data)
    
    codebase = parse_codebase(repo_data)
    logger.debug("Parsed codebase: %s", codebase)

    summary_lines = []
    for path, code in codebase.items():
        if not path.lower().endswith("readme.md") and not path.lower().endswith(".md"):
            logger.debug(f"Analyzing file: {path}")
            summary = understand_code_chunked(code)
            summary_lines.append(f"File: {path}\n{summary}\n")

    output_file = 'repo_summary.txt'
    with open(output_file, 'w') as f:
        f.write("\n".join(summary_lines))

    logger.debug("Summary written to %s", output_file)

    return jsonify({'message': f'Summary written to {output_file}'})
