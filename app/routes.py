import os
from flask import Blueprint, request, jsonify
from .github_integration import fetch_github_repo_contents
from .code_analysis import parse_codebase, understand_code_chunked, quick_understand_code_chunked
import logging
import concurrent.futures

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
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_path = {executor.submit(understand_code_chunked, code): path for path, code in codebase.items() if not path.lower().endswith("readme.md") and not path.lower().endswith(".md") and len(code) < 10000}  # Filter large files
        for future in concurrent.futures.as_completed(future_to_path):
            path = future_to_path[future]
            try:
                summary = future.result()
                summary_lines.append(f"File: {path}\n{summary}\n")
            except Exception as exc:
                logger.error(f"{path} generated an exception: {exc}")

    output_file = 'repo_summary.txt'
    with open(output_file, 'w') as f:
        f.write("\n".join(summary_lines))

    logger.debug("Summary written to %s", output_file)

    return jsonify({'message': f'Summary written to {output_file}'})

@bp.route('/quick_summarize_repo', methods=['POST'])
def quick_summarize_repo():
    repo_url = request.json['repo_url']
    owner, repo = repo_url.strip('/').split('/')[-2:]
    logger.debug("Received request to quick summarize repo: %s", repo_url)

    # Fetch and analyze code
    repo_data = fetch_github_repo_contents(owner, repo)
    logger.debug("Fetched repo data: %s", repo_data)
    
    codebase = parse_codebase(repo_data)
    logger.debug("Parsed codebase: %s", codebase)

    summary_lines = []
    file_count = 0
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_path = {executor.submit(quick_understand_code_chunked, code): path for path, code in codebase.items() if not path.lower().endswith("readme.md") and not path.lower().endswith(".md") and len(code) < 10000}  # Filter large files
        for future in concurrent.futures.as_completed(future_to_path):
            path = future_to_path[future]
            if file_count >= 15:
                break
            try:
                summary = future.result()
                summary_lines.append(f"File: {path}\n{summary}\n")
                file_count += 1
            except Exception as exc:
                logger.error(f"{path} generated an exception: {exc}")

    output_file = 'quick_repo_summary.txt'
    with open(output_file, 'w') as f:
        f.write("\n".join(summary_lines))

    logger.debug("Quick summary written to %s", output_file)

    return jsonify({'message': f'Quick summary written to {output_file}'})
