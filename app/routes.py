from flask import Blueprint, request, jsonify
import os
import requests
from .github_integration import fetch_github_repo
from .jira_integration import fetch_jira_user_stories
from .code_analysis import parse_codebase, understand_code
from .story_validation import match_stories_to_code
from .documentation_generation import generate_documentation

bp = Blueprint('main', __name__)

@bp.route('/validate', methods=['POST'])
def validate_code():
    try:
        data = request.get_json()
        print(f"Received data: {data}")
        
        repo_url = data['repo_url'].replace('https://github.com/', 'https://api.github.com/repos/')
        jira_project_key = data['jira_project_key']
        
        print(f"Fetching GitHub repo: {repo_url}")
        # Fetch and analyze code
        repo = fetch_github_repo(repo_url)
        print(f"Repository data: {repo}")
        codebase = parse_codebase(repo)
        code_explanations = {path: understand_code(code) for path, code in codebase.items()}
        
        print("Fetching Jira user stories")
        # Fetch and validate user stories
        jira_url = os.getenv('JIRA_URL')
        if not jira_url:
            raise ValueError("JIRA_URL environment variable is not set")
        user_stories = fetch_jira_user_stories(jira_url, jira_project_key)
        validation_results = match_stories_to_code(code_explanations, user_stories)
        
        print("Generating documentation")
        # Generate documentation
        documentation = generate_documentation(code_explanations, user_stories)
        
        return jsonify({'validation_results': validation_results, 'documentation': documentation})

    except requests.exceptions.HTTPError as http_err:
        if http_err.response.status_code == 401:
            return jsonify({'error': 'Unauthorized access. Please check your GitHub or Jira token.'}), 401
        return jsonify({'error': f'HTTP error occurred: {http_err}'}), 500
    except requests.exceptions.JSONDecodeError as json_err:
        return jsonify({'error': f'Error parsing JSON: {json_err}'}), 500
    except KeyError as key_err:
        return jsonify({'error': f'Missing key in request data: {key_err}'}), 400
    except Exception as err:
        return jsonify({'error': f'An error occurred: {err}'}), 500
