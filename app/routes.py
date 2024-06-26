from flask import Blueprint, request, jsonify
from .github_integration import fetch_github_repo
from .jira_integration import fetch_jira_user_stories
from .code_analysis import parse_codebase, understand_code
from .story_validation import match_stories_to_code
from .documentation_generation import generate_documentation

bp = Blueprint('main', __name__)

@bp.route('/validate', methods=['POST'])
def validate_code():
    repo_url = request.json['repo_url']
    jira_project_key = request.json['jira_project_key']
    github_token = request.json['github_token']
    jira_user = request.json['jira_user']
    jira_api_token = request.json['jira_api_token']

    # Fetch and analyze code
    repo = fetch_github_repo(repo_url, github_token)
    codebase = parse_codebase(repo)
    code_explanations = {path: understand_code(code) for path, code in codebase.items()}

    # Fetch and validate user stories
    user_stories = fetch_jira_user_stories(jira_url, jira_project_key, jira_user, jira_api_token)
    validation_results = match_stories_to_code(code_explanations, user_stories)

    # Generate documentation
    documentation = generate_documentation(code_explanations, user_stories)

    return jsonify({'validation_results': validation_results, 'documentation': documentation})
