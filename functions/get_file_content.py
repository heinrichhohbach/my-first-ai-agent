import os
from .config import MAX_CHARS
from google import genai

schema_get_file_content = genai.types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file in the specified directory, constrained to the working directory.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The directory where the file is located, relative to the working directory. If not provided, uses the working directory itself.",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    abs_working_directory = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)
    
    if not abs_full_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(abs_full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            file_size = os.path.getsize(abs_full_path)
            if file_size > MAX_CHARS:
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
        return file_content_string

    except Exception as e:
        return f"Error: {str(e)}"