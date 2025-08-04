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
    user_prompt_added = False

    i= 0

    while i < 20:
        function_called = False
        try:
            if not user_prompt_added:
                messages.append(genai.types.Content(role="user", parts=[genai.types.Part(text=input_prompt)]))
                user_prompt_added = True

            response = generate_ai_response(api_key, messages, SYSTEM_PROMPT)
            messages.append(response.candidates[0].content)
            
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
                        messages.append(function_call_result)
                        function_called = True
                        #print(f"DEBUG: These are the messages AFTER TOOLS: {messages}")
            
                        # Check that the result has the expected structure
                        if not hasattr(function_call_result, 'parts') or len(function_call_result.parts) == 0:
                            raise Exception("Function call result missing parts")
            
                        if not hasattr(function_call_result.parts[0], 'function_response'):
                            raise Exception("Function call result missing function_response")
            
                        # If verbose, print the result
                        if verbose:
                            print(f"-> {function_call_result.parts[0].function_response.response}")
                        
                        break
                        
                    
                    elif hasattr(part, 'text') and part.text:
                        lower_text = part.text.lower().strip()
                        # Only exit if the agent says "goodbye"
                        if "goodbye" in lower_text:
                            print(part.text)
                            return
                        else:
                            # It's probably just talking about its next step or plan—keep looping!
                            function_called = True
                            break

                    
            else:
                print("No response parts found")
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again with a different prompt.")
        
        if not function_called:
            break
        i += 1


if __name__ == "__main__":
    main()