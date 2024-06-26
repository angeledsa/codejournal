from atlassian import Jira

def fetch_jira_user_stories(jira_url, project_key, jira_user, jira_api_token):
    jira = Jira(url=jira_url, username=jira_user, password=jira_api_token)
    user_stories = jira.get_all_project_issues(project_key)
    return user_stories
