from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file
from functions.get_file_content import get_file_content
from google import genai
from functions.config import WORKING_DIR

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    functions = {
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
        "get_file_content": get_file_content,
    }

    function_name = function_call_part.name

    if function_name not in functions:
        return genai.types.Content(
            role="tool",
            parts=[
            genai.types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
            )
        ],
    )
    
    args = dict(function_call_part.args)
    args['working_directory'] = WORKING_DIR

    function_to_call = functions[function_name]
    #print(f"DEBUG: Calling function {function_name} with args: {args}")
    function_result = function_to_call(**args)

    return genai.types.Content(
        role="tool",
        parts=[
            genai.types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )