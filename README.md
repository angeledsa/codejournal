>> # CodeJournal
>> 
>> CodeJournal is a comprehensive tool designed to enhance software development by automating documentation, providing intelligent project management insights, and fostering seamless collaboration.
>> 
>> ## Features
>> 
>> ### 1. Quick Repository Summary
>> 
>> >> **Description**: Provides a high-level overview of the codebase quickly.
>> 
>> ### 2. Detailed Code Analysis
>> 
>> >> **Description**: Offers an in-depth understanding and documentation of code functionality.
>> 
>> ### 3. JIRA Summary Comparison
>> 
>> >> **Description**: Validates if all user stories have been implemented as per JIRA.
>> 
>> ### 4. End-User Documentation Generation
>> 
>> >> **Description**: Converts technical summaries into non-technical, user-friendly documentation.
>> 
>> ### 5. Extract README Context
>> 
>> >> **Description**: Extracts and utilizes README content for better context in documentation and analysis.
>> 
>> ### 6. Predict Blockers and Risks
>> 
>> >> **Description**: Predicts potential development blockers and risks based on the current codebase and user stories.
>> 
>> ## Usage
>> 
>> ### Parsing Codebase
>> 
>> >> **Function**: `parse_codebase(repo_data)`
>> >> **Description**: Parses the given repository data to generate a structured representation of the codebase.
>> 
>> ### Understanding Code in Chunks
>> 
>> >> **Function**: `quick_understand_code_chunked(code_snippet)`
>> >> **Description**: Provides a high-level overview of the code in manageable chunks.
>> 
>> ### Fetching JIRA Issues
>> 
>> >> **Function**: `fetch_jira_issues(jira_url, jira_project_key, jira_user, jira_api_token)`
>> >> **Description**: Fetches issues from JIRA for the specified project.
>> 
>> ### Summarizing JIRA Issues
>> 
>> >> **Function**: `summarize_jira_issues(jira_issues)`
>> >> **Description**: Summarizes JIRA issues, providing value insights and improvement suggestions.
>> 
>> ### Comparing Summaries
>> 
>> >> **Function**: `compare_summaries(jira_summary_file, repo_summary_file)`
>> >> **Description**: Compares JIRA user stories with the implemented functions in the repository summary.
>> 
>> ### Generating End-User Documentation
>> 
>> >> **Function**: `generate_end_user_documentation(quick_repo_summary_path, comparison_result_path, output_path)`
>> >> **Description**: Generates end-user, non-technical documentation based on the code summary and project context.
>> 
>> ### Predicting Blockers and Risks
>> 
>> >> **Function**: `predict_blockers(quick_repo_summary_path, comparison_result_path, output_path)`
>> >> **Description**: Predicts potential development blockers and risks and provides suggested mitigations.