from flask import Blueprint, request, jsonify
from .github_integration import fetch_github_repo_contents
from .code_analysis import parse_codebase, understand_code_chunked, extract_readme_context
import logging
import os
import json

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
    
    # Store results in a dictionary
    results = {}
    for path, code in codebase.items():
        summary = understand_code_chunked(code)
        results[path] = summary
        logger.debug("Code summary for %s: %s", path, summary)
    
    # Extract README context
    readme_context = extract_readme_context(repo_data)
    results['README.md'] = readme_context
    logger.debug("README.md context: %s", readme_context)
    
    # Save results to a local JSON file
    output_file = 'code_summaries.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)
    logger.debug("Saved code summaries to %s", output_file)

    return jsonify({'message': f"Summaries saved to {output_file}"})
