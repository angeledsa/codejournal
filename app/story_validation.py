def match_stories_to_code(code_explanations, user_stories):
    matched_stories = {}
    for story in user_stories:
        story_key = story['key']
        story_summary = story['fields']['summary']
        story_description = story['fields'].get('description', 'No description provided')
        matched_stories[story_key] = {
            'summary': story_summary,
            'description': story_description,
            # other fields
        }
    return matched_stories
