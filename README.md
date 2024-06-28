>> # CodeJournal
>> 
>> ## Overview
>> 
>> CodeJournal is a comprehensive tool for analyzing GitHub repositories and JIRA projects, providing detailed summaries and comparisons between user stories and code implementations. The tool leverages OpenAI's GPT-4-turbo model to deliver high-level and detailed insights into codebases and project management data.
>> 
>> ## Features
>> 
>> - **Quick Repository Summary**: Quickly summarize the main functions and high-level overview of code files.
>> - **JIRA Issue Summarization**: Fetch and summarize JIRA issues, including user story improvement suggestions.
>> - **JIRA and Repository Comparison**: Compare JIRA user stories with code implementations to verify if all tasks have been implemented.
>> 
>> ## Installation
>> 
>> ### Prerequisites
>> 
>> - Python 3.9+
>> - Node.js and npm
>> - Git
>> - OpenAI API Key
>> - JIRA API Token
>> 
>> ### Steps
>> 
>> 1. Clone the repository:
>> 
>>     ```bash
>>     git clone https://github.com/yourusername/codejournal.git
>>     cd codejournal
>>     ```
>> 
>> 2. Set up a virtual environment and install dependencies:
>> 
>>     ```bash
>>     python3.9 -m venv venv
>>     source venv/bin/activate
>>     pip install -r requirements.txt
>>     ```
>> 
>> 3. Install frontend dependencies:
>> 
>>     ```bash
>>     cd frontend
>>     npm install
>>     ```
>> 
>> 4. Set up environment variables:
>> 
>>     Create a `.env` file in the root directory and add your OpenAI and JIRA credentials:
>> 
>>     ```plaintext
>>     OPENAI_API_KEY=your_openai_api_key_here
>>     JIRA_API_TOKEN=your_jira_api_token_here
>>     ```
>> 
>> ## Usage
>> 
>> ### Quick Repository Summary
>> 
>> Endpoint: `/quick_summarize_repo`
>> 
>> Payload:
>> 
>> ```json
>> {
>>   "repo_url": "https://github.com/owner/repo"
>> }
>> ```
>> 
>> ### JIRA Issue Summarization
>> 
>> Endpoint: `/summarize_jira`
>> 
>> Payload:
>> 
>> ```json
>> {
>>   "jira_url": "https://yourdomain.atlassian.net",
>>   "jira_project_key": "PROJECT_KEY",
>>   "jira_user": "your_jira_user",
>>   "jira_api_token": "your_jira_api_token"
>> }
>> ```
>> 
>> ### JIRA and Repository Comparison
>> 
>> Endpoint: `/compare_summaries`
>> 
>> This feature compares `quick_repo_summary.txt` with `jira_summary.txt` and provides a human-readable output indicating if all User Stories have been implemented.
>> 
>> ## Project Structure
>> 
>> ```plaintext
>> codejournal/
>> ├── app/
>> │   ├── __init__.py
>> │   ├── routes.py
>> │   ├── github_integration.py
>> │   ├── code_analysis.py
>> ├── frontend/
>> │   ├── public/
>> │   ├── src/
>> │   ├── package.json
>> ├── .gitignore
>> ├── README.md
>> ├── requirements.txt
>> ├── run.py
>> ├── quick_repo_summary.txt
>> ├── jira_summary.txt
>> ├── comparison_result.txt
>> ```
>> 
>> ## Contributing
>> 
>> We welcome contributions! Please fork the repository and submit pull requests for review.
>> 
>> ## License
>> 
>> This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details.
>> 
>> ## Acknowledgements
>> 
>> - OpenAI for the GPT-4-turbo model
>> - Atlassian for JIRA
