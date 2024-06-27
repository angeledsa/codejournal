from flask import Blueprint, request, jsonify
from .github_integration import fetch_github_repo_contents
from .jira_integration import fetch_jira_user_stories
from .code_analysis import parse_codebase, understand_code, extract_readme_context
from .story_validation import match_stories_to_code
from .documentation_generation import generate_documentation
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
    
    code_explanations = {path: understand_code(code) for path, code in codebase.items()}
    logger.debug("Code explanations: %s", code_explanations)
    
    readme_context = extract_readme_context(repo_data)
    logger.debug("README.md context: %s", readme_context)

    return jsonify({'code_explanations': code_explanations, 'readme_context': readme_context})

@bp.route('/summarize_jira', methods=['POST'])
def summarize_jira():
    jira_url = request.json['jira_url']
    jira_project_key = request.json['jira_project_key']
    jira_user = request.json['jira_user']
    jira_api_token = request.json['jira_api_token']
    logger.debug("Received request to summarize JIRA project: %s", jira_project_key)

    # Fetch user stories
    user_stories = fetch_jira_user_stories(jira_url, jira_project_key, jira_user, jira_api_token)
    logger.debug("Fetched user stories: %s", user_stories)

    return jsonify({'user_stories': user_stories})

@bp.route('/compare_repo_jira', methods=['POST'])
def compare_repo_jira():
    repo_url = request.json['repo_url']
    jira_url = request.json['jira_url']
    jira_project_key = request.json['jira_project_key']
    github_token = request.json['github_token']
    jira_user = request.json['jira_user']
    jira_api_token = request.json['jira_api_token']
    owner, repo = repo_url.strip('/').split('/')[-2:]
    logger.debug("Received request to compare repo with JIRA project: %s", jira_project_key)

    # Fetch and analyze code
    repo_data = fetch_github_repo_contents(owner, repo)
    logger.debug("Fetched repo data: %s", repo_data)
    
    codebase = parse_codebase(repo_data)
    logger.debug("Parsed codebase: %s", codebase)
    
    code_explanations = {path: understand_code(code) for path, code in codebase.items()}
    logger.debug("Code explanations: %s", code_explanations)

    # Fetch user stories
    user_stories = fetch_jira_user_stories(jira_url, jira_project_key, jira_user, jira_api_token)
    logger.debug("Fetched user stories: %s", user_stories)

    # Validate stories against code
    validation_results = match_stories_to_code(code_explanations, user_stories)
    logger.debug("Validation results: %s", validation_results)

    return jsonify({'validation_results': validation_results})
