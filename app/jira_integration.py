import requests
import os
import base64

def fetch_jira_user_stories(jira_url, project_key, user, api_token):
    auth = base64.b64encode(f"{user}:{api_token}".encode()).decode()
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/json'
    }
    query = {'jql': f'project={project_key}'}
    response = requests.get(f"{jira_url}/rest/api/3/search", headers=headers, params=query)
    
    if response.status_code == 200:
        try:
            return response.json()['issues']
        except requests.exceptions.JSONDecodeError:
            raise ValueError("Failed to parse JSON response from Jira")
    else:
        response.raise_for_status()

# Example usage:
if __name__ == "__main__":
    jira_url = os.getenv('JIRA_URL')
    project_key = "LUM"
    user = os.getenv('JIRA_USER')
    api_token = os.getenv('JIRA_API_TOKEN')
    user_stories = fetch_jira_user_stories(jira_url, project_key, user, api_token)
