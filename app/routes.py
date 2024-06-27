from flask import Blueprint, request, jsonify
import os
import requests
from .github_integration import fetch_github_repo
from .jira_integration import fetch_jira_user_stories
from .code_analysis import parse_codebase, analyze_code_with_openai
from .story_validation import match_stories_to_code
from .documentation_generation import generate_documentation

bp = Blueprint('main', __name__)

@bp.route('/validate', methods=['POST'])
def validate_code():
    try:
        data = request.get_json()
        
        repo_url = data['repo_url'].replace('https://github.com/', 'https://api.github.com/repos/')
        jira_project_key = data['jira_project_key']
        
        # Fetch and analyze code
        repo = fetch_github_repo(repo_url)
        codebase = parse_codebase(repo)
        
        # Analyze code with OpenAI
        code_explanations = analyze_code_with_openai(codebase)
        
        # Fetch and validate user stories
        jira_url = os.getenv('JIRA_URL')
        jira_user = os.getenv('JIRA_USER')
        jira_api_token = os.getenv('JIRA_API_TOKEN')
        user_stories = fetch_jira_user_stories(jira_url, jira_project_key, jira_user, jira_api_token)
        
        # Match stories to code
        validation_results = match_stories_to_code(code_explanations, user_stories)
        
        # Generate structured documentation
        documentation = generate_documentation(validation_results, user_stories)
        
        return jsonify({'documentation': documentation})

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
