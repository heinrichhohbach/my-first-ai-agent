from google import genai

from functions.get_files_info import schema_get_files_info
from functions.run_python import schema_run_python
from functions.write_file import schema_write_file
from functions.get_file_content import schema_get_file_content

def generate_ai_response(api_key, messages, system_prompt):
    available_functions = genai.types.Tool(
    function_declarations=[
        schema_get_files_info,schema_get_file_content,
        schema_write_file, schema_run_python
    ]
)
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=genai.types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
),)
    return response