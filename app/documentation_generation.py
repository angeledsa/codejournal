def generate_documentation(validation_results, user_stories):
    documentation = []
    for story in user_stories:
        story_id = story['id']
        story_summary = story['fields']['summary']
        story_description = story['fields']['description']['content'][0]['content'][0]['text'] if story['fields']['description'] else "No description available"

        story_info = {
            "story_id": story_id,
            "summary": story_summary,
            "description": story_description,
            "matched_code": validation_results.get(story_id, [])
        }
        documentation.append(story_info)
    return documentation
