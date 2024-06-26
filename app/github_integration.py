import requests

def fetch_github_repo(repo_url, access_token):
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(repo_url, headers=headers)
    return response.json()
