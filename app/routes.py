from flask import Blueprint, request, jsonify
from .github_integration import fetch_github_repo_contents
from .code_analysis import parse_codebase, quick_understand_code_chunked, fetch_jira_issues, summarize_jira_issues, compare_summaries, generate_end_user_documentation
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

@bp.route('/summarize_jira', methods=['POST'])
def summarize_jira():
    jira_url = request.json['jira_url']
    jira_project_key = request.json['jira_project_key']
    jira_user = request.json['jira_user']
    jira_api_token = request.json['jira_api_token']
    logger.debug("Received request to summarize JIRA issues")

    # Fetch JIRA issues
    jira_issues = fetch_jira_issues(jira_url, jira_project_key, jira_user, jira_api_token)
    if not jira_issues:
        return jsonify({'error': 'Failed to fetch JIRA issues.'}), 404

    # Summarize JIRA issues
    summaries = summarize_jira_issues(jira_issues)

    with open('jira_summary.txt', 'w') as file:
        file.write(summaries)

    logger.debug("JIRA summary written to jira_summary.txt")
    return jsonify({'message': 'JIRA summary completed.', 'summary_file': 'jira_summary.txt'})

@bp.route('/compare_summaries', methods=['POST'])
def compare_summaries_route():
    logger.debug("Received request to compare summaries")
    try:
        comparison_result = compare_summaries('jira_summary.txt', 'quick_repo_summary.txt')
        with open('comparison_result.txt', 'w') as file:
            file.write(comparison_result)

        logger.debug("Comparison result written to comparison_result.txt")
        return jsonify({'message': 'Comparison completed.', 'comparison_file': 'comparison_result.txt'})
    except Exception as e:
        logger.error(f"Error comparing summaries: {e}")
        return jsonify({'error': str(e)}), 500
    
@bp.route('/generate_end_user_documentation', methods=['POST'])
def generate_end_user_docs():
    quick_repo_summary_path = request.json['quick_repo_summary_path']
    comparison_result_path = request.json['comparison_result_path']
    output_path = request.json.get('output_path', 'end_user_documentation.txt')
    
    logger.debug("Received request to generate end-user documentation")
    
    try:
        output_file = generate_end_user_documentation(quick_repo_summary_path, comparison_result_path, output_path)
        return jsonify({'message': 'End-user documentation generated.', 'output_file': output_file})
    except Exception as e:
        logger.error(f"Error generating end-user documentation: {e}")
        return jsonify({'error': 'Failed to generate end-user documentation.'}), 500