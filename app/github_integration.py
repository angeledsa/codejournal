import requests
import os

def fetch_github_repo(repo_url):
    github_token = os.getenv('GITHUB_TOKEN')
    headers = {'Authorization': f'token {github_token}'}
    response = requests.get(repo_url, headers=headers)
    
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    
    if response.status_code == 200:
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            print("Failed to parse JSON:")
            print(response.text)
            raise
    else:
        print("Failed to fetch repository data:")
        print(response.text)
        response.raise_for_status()

# Example usage:
if __name__ == "__main__":
    repo_url = "https://api.github.com/repos/angeledsa/lumina"
    repo_data = fetch_github_repo(repo_url)
