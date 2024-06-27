import requests
import os
import base64
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def fetch_github_repo_contents(owner, repo, path=''):
    github_token = os.getenv('GITHUB_TOKEN')
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url, headers=headers)
    
    logger.debug("Status Code: %s", response.status_code)
    logger.debug("Response Text: %s", response.text)
    
    if response.status_code == 200:
        try:
            contents_data = response.json()
            file_structure = {}

            if isinstance(contents_data, list):
                for item in contents_data:
                    if item['type'] == 'file':
                        file_response = requests.get(item['url'], headers=headers)
                        if file_response.status_code == 200:
                            file_content = base64.b64decode(file_response.json()['content']).decode('utf-8')
                            file_structure[item['path']] = file_content
                        else:
                            logger.error("Failed to fetch file content for %s: %s", item['path'], file_response.text)
                    elif item['type'] == 'dir':
                        sub_dir_files = fetch_github_repo_contents(owner, repo, item['path'])
                        file_structure.update(sub_dir_files)
            else:
                logger.error("Unexpected data structure: %s", contents_data)
            
            return file_structure
        except requests.exceptions.JSONDecodeError:
            logger.error("Failed to parse JSON:")
            logger.error(response.text)
            raise
    else:
        logger.error("Failed to fetch repository data:")
        logger.error(response.text)
        response.raise_for_status()

# Example usage:
if __name__ == "__main__":
    owner = "angeledsa"
    repo = "lumina"
    repo_data = fetch_github_repo_contents(owner, repo)
    print(repo_data)
