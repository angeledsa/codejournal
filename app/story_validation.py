def match_stories_to_code(code_explanations, user_stories):
    validation_results = {}
    for story in user_stories:
        story_id = story['id']
        story_summary = story['fields']['summary']
        story_description = story['fields']['description']['content'][0]['content'][0]['text'] if story['fields']['description'] else ""
        story_text = f"{story_summary}\n{story_description}"
        
        validation_results[story_id] = []
        matched = False

        for path, explanation in code_explanations.items():
            if story_summary in explanation or story_description in explanation:
                validation_results[story_id].append(path)
                matched = True

        if not matched:
            validation_results[story_id].append("NO FUNCTION FOUND")
                
    return validation_results
