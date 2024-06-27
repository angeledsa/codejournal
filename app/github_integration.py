import requests
import os
import base64
import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

GITHUB_API_URL = "https://api.github.com"

EXCLUDED_DIRS = ['node_modules', 'vendor', 'dist', 'build']
EXCLUDED_FILES = ['package-lock.json', 'yarn.lock', 'Gemfile.lock', 'Pipfile.lock']
MAX_FILE_SIZE = 50000  # Limit the size of files to be fetched in bytes

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
            if file_info['type'] == 'dir' and file_info['name'] not in EXCLUDED_DIRS:
                subdir_files = fetch_github_repo_contents(owner, repo, file_info['path'])
                file_structure.update(subdir_files)
            elif file_info['type'] == 'file' and file_info['name'] not in EXCLUDED_FILES and file_info['size'] <= MAX_FILE_SIZE:
                file_response = requests.get(file_info['url'], headers=headers)
                if file_response.status_code == 200:
                    file_content = base64.b64decode(file_response.json()['content']).decode('utf-8')
                    file_structure[file_info['path']] = file_content
                else:
                    logger.error(f"Failed to fetch file content for {file_info['path']}")
        return file_structure
    else:  # It's a single file
        if repo_data['type'] == 'file' and repo_data['size'] <= MAX_FILE_SIZE:
            file_content = base64.b64decode(repo_data['content']).decode('utf-8')
            return {repo_data['path']: file_content}

    return {}

