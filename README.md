>> # CodeJournal
>> 
>> CodeJournal is an application that reviews code from a GitHub repository, validates it against user stories in Jira Cloud, and generates functional user documentation.
>> 
>> ## Setup
>> 
>> 1. Clone the repository:
>>     ```bash
>>     git clone <repository-url>
>>     cd <repository-folder>
>>     ```
>> 
>> 2. Create a virtual environment and activate it:
>>     ```bash
>>     python -m venv venv
>>     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
>>     ```
>> 
>> 3. Install the dependencies:
>>     ```bash
>>     pip install -r requirements.txt
>>     ```
>> 
>> 4. Set environment variables for GitHub, Jira, and OpenAI credentials:
>>     ```bash
>>     export GITHUB_TOKEN=<your-github-token>
>>     export JIRA_USER=<your-jira-user>
>>     export JIRA_API_TOKEN=<your-jira-api-token>
>>     export OPENAI_API_KEY=<your-openai-api-key>
>>     ```
>> 
>> 5. Run the application:
>>     ```bash
>>     python run.py
>>     ```
>> 
>> ## Usage
>> 
>> ### Mode 1: Summarize the GitHub repository
>> Send a POST request to `/summarize_repo` with the following JSON payload:
>> 
>> ```bash
>> curl -X POST http://127.0.0.1:5000/summarize_repo -H "Content-Type: application/json" -d '{
>>     "repo_url": "https://api.github.com/repos/username/repository",
>>     "github_token": "your-github-token"
>> }'
>> ```
>> 
>> ### Mode 2: Summarize the Jira project
>> Send a POST request to `/summarize_jira` with the following JSON payload:
>> 
>> ```bash
>> curl -X POST http://127.0.0.1:5000/summarize_jira -H "Content-Type: application/json" -d '{
>>     "jira_url": "https://your-domain.atlassian.net",
>>     "jira_project_key": "PROJECTKEY",
>>     "jira_user": "your-jira-username",
>>     "jira_api_token": "your-jira-api-token"
>> }'
>> ```
>> 
>> ### Mode 3: Compare the GitHub repository with the Jira project
>> Send a POST request to `/compare_repo_jira` with the following JSON payload:
>> 
>> ```bash
>> curl -X POST http://127.0.0.1:5000/compare_repo_jira -H "Content-Type: application/json" -d '{
>>     "repo_url": "https://api.github.com/repos/username/repository",
>>     "jira_url": "https://your-domain.atlassian.net",
>>     "jira_project_key": "PROJECTKEY",
>>     "github_token": "your-github-token",
>>     "jira_user": "your-jira-username",
>>     "jira_api_token": "your-jira-api-token"
>> }'
>> ```
>> 
>> ## Response
>> 
>> The application will return a JSON response based on the mode.
>> 
>> ### Example Response for `/summarize_repo`
>> 
>> ```json
>> {
>>     "code_explanations": {
>>         "path/to/file1.py": "Explanation of file1.py",
>>         "path/to/file2.py": "Explanation of file2.py"
>>     }
>> }
>> ```
>> 
>> ### Example Response for `/summarize_jira`
>> 
>> ```json
>> {
>>     "user_stories": [
>>         {
>>             "key": "PROJECT-1",
>>             "description": "User story description"
>>         },
>>         {
>>             "key": "PROJECT-2",
>>             "description": "Another user story description"
>>         }
>>     ]
>> }
>> ```
>> 
>> ### Example Response for `/compare_repo_jira`
>> 
>> ```json
>> {
>>     "validation_results": [
>>         {"story_key": "PROJECT-1", "matched": true},
>>         {"story_key": "PROJECT-2", "matched": false}
>>     ]
>> }
>> ```
>> 
>> ## Project Structure
>> 
>> ```
>> project-root/
>> │
>> ├── app/
>> │   ├── __init__.py
>> │   ├── github_integration.py
>> │   ├── jira_integration.py
>> │   ├── code_analysis.py
>> │   ├── story_validation.py
>> │   ├── documentation_generation.py
>> │   ├── routes.py
>> │
>> ├── config.py
>> ├── requirements.txt
>> ├── run.py
>> ├── README.md
>> ```
>> 
>> ## Troubleshooting
>> 
>> If you encounter a 404 error when accessing the routes, ensure that:
>> 
>> 1. The Flask application is running correctly using `python run.py`.
>> 2. The routes are correctly defined in `routes.py` and registered in `__init__.py`.
>> 3. You are making the requests to the correct URL and port (e.g., `http://127.0.0.1:5000`).
>> 
>> Feel free to modify and expand this structure as needed for your project. CodeJournal aims to streamline the process of ensuring that your codebase aligns with your project requirements and provides clear, functional documentation.
