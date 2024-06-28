import os
from openai import OpenAI
import logging
import requests
from requests.auth import HTTPBasicAuth

# Set up logging
logger = logging.getLogger(__name__)

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def parse_codebase(repo_data):
    code_structure = {}
    for file_path, file_content in repo_data.items():
        if not file_path.endswith('.gitignore'):
            code_structure[file_path] = file_content
    return code_structure

def understand_code_chunked(code_snippet):
    logger.debug("Calling OpenAI API to understand code in chunks...")
    chunk_size = 4096  # Ensure chunks are small enough to fit within max tokens limit
    chunks = [code_snippet[i:i + chunk_size] for i in range(0, len(code_snippet), chunk_size)]
    
    explanations = []
    for chunk in chunks:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": f"Provide a detailed summary of each function in the following code and explain how they relate to the rest of the application:\n\n{chunk}"}],
            max_tokens=4096  # Reduced to avoid hitting token limits in the response
        )
        explanations.append(response.choices[0].message.content.strip())
    return "\n".join(explanations)

def quick_understand_code_chunked(code_snippet):
    logger.debug("Calling OpenAI API to quickly understand code in chunks...")
    chunk_size = 4096  # Ensure chunks are small enough to fit within max tokens limit
    chunks = [code_snippet[i:i + chunk_size] for i in range(0, len(code_snippet), chunk_size)]
    
    explanations = []
    for chunk in chunks:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": f"Provide a high-level overview of what the following code does and highlight important functions:\n\n{chunk}"}],
            max_tokens=4096  # Reduced to avoid hitting token limits in the response
        )
        explanations.append(response.choices[0].message.content.strip())
    return "\n".join(explanations)

def fetch_jira_issues(jira_url, jira_project_key, jira_user, jira_api_token):
    auth = HTTPBasicAuth(jira_user, jira_api_token)
    headers = {
        "Accept": "application/json"
    }
    
    issues_url = f"{jira_url}/rest/api/2/search?jql=project={jira_project_key}"
    response = requests.get(issues_url, headers=headers, auth=auth)
    
    if response.status_code != 200:
        logger.error(f"Failed to fetch JIRA issues: {response.status_code} {response.text}")
        return None
    
    issues = response.json().get('issues', [])
    jira_issues = []
    
    for issue in issues:
        project = issue['fields']['project']['name']
        epic = issue['fields'].get('epic', {}).get('name', 'No Epic')
        story = issue['fields']['summary']
        acceptance_criteria = issue['fields'].get('customfield_10014', 'No Acceptance Criteria')  # Change 'customfield_10014' to your actual field ID
        
        jira_issues.append({
            "project": project,
            "epic": epic,
            "story": story,
            "acceptance_criteria": acceptance_criteria
        })
    
    return jira_issues

def summarize_jira_issues(jira_issues):
    logger.debug("Calling OpenAI API to summarize JIRA issues...")

    summaries = []

    for issue in jira_issues:
        project = issue['project']
        epic = issue['epic']
        story = issue['story']
        acceptance_criteria = issue['acceptance_criteria']
        
        prompt = f"Project: {project}\nEpic: {epic}\nStory/Task: {story}\nAcceptance Criteria: {acceptance_criteria}\n\nProvide user story/task improvement suggestions:"
        
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500  # Limit tokens to ensure quick response
        )

        suggestion = response.choices[0].message.content.strip()
        summaries.append(f"Project: {project}\nEpic: {epic}\nStory/Task: {story}\nAcceptance Criteria: {acceptance_criteria}\nImprovement Suggestions: {suggestion}\n\n")

    return "\n".join(summaries)


def extract_readme_context(repo_data):
    readme_context = ""
    for file_path, file_content in repo_data.items():
        if file_path.lower() == "readme.md":
            readme_context = file_content
            break
    return readme_context
