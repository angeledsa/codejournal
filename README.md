>> # CodeJournal
>>
>> CodeJournal is an advanced tool designed to automate code review, JIRA ticket creation, and validation processes. Leveraging OpenAI's capabilities, CodeJournal significantly reduces the time and cost associated with traditional manual processes.
>>
>> ## Features
>>
>> - **Quick Repository Summary**: Summarizes the main functions and provides a high-level overview of code files.
>> - **JIRA Issue Summarization**: Fetches and summarizes JIRA issues, including user story improvement suggestions.
>> - **JIRA and Repository Comparison**: Compares JIRA user stories with code implementations to verify if all tasks have been implemented.
>> - **End-User Documentation Generation**: Generates non-technical, end-user documentation based on code summaries and context.
>>
>> ## API Endpoints
>>
>> ### Quick Summarize Repository
>> - **Endpoint**: `/quick_summarize_repo`
>> - **Method**: `POST`
>> - **Description**: Summarizes the repository's main functions and provides a high-level overview of the code files.
>> - **Request Body**:
>>   ```json
>>   {
>>     "repo_url": "https://github.com/user/repo"
>>   }
>>   ```
>> - **Response**:
>>   ```json
>>   {
>>     "message": "Quick summary completed.",
>>     "summary_file": "quick_repo_summary.txt"
>>   }
>>   ```
>>
>> ### Summarize JIRA Issues
>> - **Endpoint**: `/summarize_jira`
>> - **Method**: `POST`
>> - **Description**: Summarizes JIRA issues for a given project.
>> - **Request Body**:
>>   ```json
>>   {
>>     "jira_url": "https://your-jira-instance.atlassian.net",
>>     "jira_project_key": "PROJECT_KEY",
>>     "jira_user": "your-email@example.com",
>>     "jira_api_token": "your-jira-api-token"
>>   }
>>   ```
>> - **Response**:
>>   ```json
>>   {
>>     "message": "JIRA summary completed.",
>>     "summary_file": "jira_summary.txt"
>>   }
>>   ```
>>
>> ### Compare Summaries
>> - **Endpoint**: `/compare_summaries`
>> - **Method**: `POST`
>> - **Description**: Compares JIRA user stories with repository code implementations.
>> - **Response**:
>>   ```json
>>   {
>>     "message": "Comparison completed.",
>>     "comparison_file": "comparison_result.txt"
>>   }
>>   ```
>>
>> ### Generate End-User Documentation
>> - **Endpoint**: `/generate_end_user_documentation`
>> - **Method**: `POST`
>> - **Description**: Generates end-user, non-technical documentation based on code summaries and context.
>> - **Request Body**:
>>   ```json
>>   {
>>     "quick_repo_summary_path": "quick_repo_summary.txt",
>>     "comparison_result_path": "comparison_result.txt",
>>     "output_path": "end_user_documentation.txt" // optional
>>   }
>>   ```
>> - **Response**:
>>   ```json
>>   {
>>     "message": "End-user documentation generated.",
>>     "output_file": "end_user_documentation.txt"
>>   }
>>   ```
>>
>> ## Installation
>>
>> 1. Clone the repository:
>>    ```sh
>>    git clone https://github.com/user/repo.git
>>    ```
>> 2. Navigate to the project directory:
>>    ```sh
>>    cd repo
>>    ```
>> 3. Install the dependencies:
>>    ```sh
>>    pip install -r requirements.txt
>>    ```
>>
>> ## Configuration
>>
>> - Set up environment variables for OpenAI API:
>>   ```sh
>>   export OPENAI_API_KEY='your-openai-api-key'
>>   ```
>>
>> ## Running the Application
>>
>> - Start the Flask application:
>>   ```sh
>>   flask run
>>   ```
>>
>> ## Logging
>>
>> Logging is set up to provide debug-level output to help trace the operations and API calls.
>>
>> ## Contributing
>>
>> Contributions are welcome! Please open an issue or submit a pull request.
>>
>> ## License
>>
>> This project is licensed under the GNU General Public License v3.0.
