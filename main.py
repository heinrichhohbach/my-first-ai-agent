import os
from dotenv import load_dotenv
from google import genai
import sys
from functions.get_files_info import schema_get_files_info
from functions.run_python import schema_run_python
from functions.write_file import schema_write_file
from functions.get_file_content import schema_get_file_content
from call_function import call_function
from functions.config import SYSTEM_PROMPT
from generate_response import generate_ai_response

def main():
    # Load environment variables
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


    response, messages = generate_ai_response(api_key, input_prompt, messages, SYSTEM_PROMPT)
    
    if verbose:
        prompt_tokens = str(response.usage_metadata.prompt_token_count)
        response_tokens = str(response.usage_metadata.candidates_token_count)
        print(f"User prompt: {input_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    if response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:   
            if hasattr(part, 'function_call') and part.function_call is not None:
                function_call_result = call_function(part.function_call, verbose)
    
                # Check that the result has the expected structure
                if not hasattr(function_call_result, 'parts') or len(function_call_result.parts) == 0:
                    raise Exception("Function call result missing parts")
    
                if not hasattr(function_call_result.parts[0], 'function_response'):
                    raise Exception("Function call result missing function_response")
    
                # If verbose, print the result
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                
            elif hasattr(part, 'text') and part.text:
                print(part.text)
    else:
        print("No response parts found")


if __name__ == "__main__":
    main()