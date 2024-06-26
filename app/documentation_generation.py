def generate_documentation(code_explanations, user_stories):
    documentation = {}
    for story in user_stories:
        context = story['description']
        relevant_code = [explanation for explanation in code_explanations.values() if context in explanation]
        doc_text = f"User Story: {context}\n\nImplemented as follows:\n\n" + "\n\n".join(relevant_code)
        documentation[story['key']] = doc_text
    return documentation
