import os
from dotenv import load_dotenv
from google import genai
import sys

def main():
    system_prompt = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""
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

    print(response.text)

def generate_ai_response(api_key, input_prompt, messages, system_prompt):
    client = genai.Client(api_key=api_key)
    messages.append(genai.types.Content(role="user", parts=[genai.types.Part(text=input_prompt)]))
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=genai.types.GenerateContentConfig(system_instruction=system_prompt),)
    return response, messages


if __name__ == "__main__":
    main()