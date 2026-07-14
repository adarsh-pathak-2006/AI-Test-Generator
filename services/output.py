from services.build_prompt import build_prompt
from services.ai_integration import generate_response

def final_output(doc):
    prompt=build_prompt(document=doc)
    output=generate_response(prompt=prompt)
    return output