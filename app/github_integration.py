import requests
import os
import base64
import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

GITHUB_API_URL = "https://api.github.com"

def fetch_github_repo_contents(owner, repo, path=""):
    headers = {
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
        "Accept": "application/vnd.github+json"
    }

    contents_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(contents_url, headers=headers)
    response.raise_for_status()
    
    repo_data = response.json()
    
    if isinstance(repo_data, list):  # It's a directory
        file_structure = {}
        for file_info in repo_data:
            if file_info['type'] == 'file' and not is_common_dependency(file_info['path']):
                file_response = requests.get(file_info['url'], headers=headers)
                if file_response.status_code == 200:
                    file_content = base64.b64decode(file_response.json()['content']).decode('utf-8')
                    file_structure[file_info['path']] = file_content
                else:
                    logger.error(f"Failed to fetch file content for {file_info['path']}")
        return file_structure
    else:  # It's a single file
        if repo_data['type'] == 'file' and not is_common_dependency(repo_data['path']):
            file_content = base64.b64decode(repo_data['content']).decode('utf-8')
            return {repo_data['path']: file_content}

    return {}

def is_common_dependency(file_path):
    common_dirs = ['node_modules', 'vendor', 'dist', 'build', 'bin', '.git', '__pycache__']
    common_extensions = ['.lock', '.json', '.md', '.txt', '.yaml', '.yml', '.xml']
    return any(dir in file_path for dir in common_dirs) or file_path.endswith(tuple(common_extensions))
