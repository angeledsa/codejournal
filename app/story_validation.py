def match_stories_to_code(code_explanations, user_stories):
    validation_results = []
    for story in user_stories:
        matched = any(story['description'] in explanation for explanation in code_explanations.values())
        validation_results.append((story['key'], matched))
    return validation_results
