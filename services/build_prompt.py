def build_prompt(document):
    prompt = f"""
Based on the following document, generate a list of 5 multiple-choice questions.
Return ONLY a JSON array of objects without any markdown formatting or code blocks.
Each object must have exactly these keys:
"question": The question text
"option1": First option text
"option2": Second option text
"option3": Third option text
"option4": Fourth option text
"correct_ans": The correct option letter, which must be exactly "A", "B", "C", or "D".

Document:
{document}
"""
    return prompt
