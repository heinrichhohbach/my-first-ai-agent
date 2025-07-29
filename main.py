import os
from dotenv import load_dotenv
from google import genai
import sys
from functions.get_files_info import schema_get_files_info

def main():
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    args = sys.argv[1:]

    if not args:
        print("You provided no prompt.")
        print("Please use the following format: uv run main.py 'Your prompt here'")
        sys.exit(1)
    
    verbose = False
    if "--verbose" in args:
        verbose = True
        args.remove("--verbose")
    
    input_prompt = " ".join(args)
    messages = []


    response, messages = generate_ai_response(api_key, input_prompt, messages, system_prompt)
    
    if verbose:
        prompt_tokens = str(response.usage_metadata.prompt_token_count)
        response_tokens = str(response.usage_metadata.candidates_token_count)
        print(f"User prompt: {input_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    if response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'function_call'):
                print(f"Calling function: {part.function_call.name}({part.function_call.args})")
            elif hasattr(part, 'text') and part.text:
                print(part.text)
    else:
        print("No response parts found")

def generate_ai_response(api_key, input_prompt, messages, system_prompt):
    available_functions = genai.types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)
    client = genai.Client(api_key=api_key)
    messages.append(genai.types.Content(role="user", parts=[genai.types.Part(text=input_prompt)]))
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=genai.types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
),)
    return response, messages


if __name__ == "__main__":
    main()