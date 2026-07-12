from services.build_prompt import build_prompt
from services.ai_integration import generate_response

def final_output(input):
    prompt=build_prompt(input=input)
    output=generate_response(prompt=prompt)
    return output