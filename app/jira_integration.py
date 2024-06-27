import requests
import os
import base64

def fetch_jira_user_stories(jira_url, project_key):
    jira_user = os.getenv('JIRA_USER')
    jira_api_token = os.getenv('JIRA_API_TOKEN')
    
    if not jira_user or not jira_api_token:
        raise ValueError("JIRA_USER or JIRA_API_TOKEN environment variable not set")

    auth = base64.b64encode(f"{jira_user}:{jira_api_token}".encode()).decode()
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/json'
    }
    query = {'jql': f'project={project_key}'}
    response = requests.get(f"{jira_url}/rest/api/3/search", headers=headers, params=query)
    
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    
    if response.status_code == 200:
        try:
            return response.json()['issues']
        except requests.exceptions.JSONDecodeError:
            print("Failed to parse JSON:")
            print(response.text)
            raise
    else:
        print("Failed to fetch Jira issues:")
        print(response.text)
        response.raise_for_status()

# Example usage:
if __name__ == "__main__":
    jira_url = os.getenv('JIRA_URL')
    project_key = "LUM"
    user_stories = fetch_jira_user_stories(jira_url, project_key)
