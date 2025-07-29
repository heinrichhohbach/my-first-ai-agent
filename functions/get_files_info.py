import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    abs_working_directory = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)
    
    if not abs_full_path.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(abs_full_path):
        return f'Error: "{directory}" is not a directory'
    
    try:
        list_of_dir_content = os.listdir(abs_full_path)
        dir_content = ""

        for item in list_of_dir_content:
            item_path = os.path.join(abs_full_path, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            dir_content += f"- {item}: file_size={file_size} bytes, is_dir={is_dir}\n"
        
        return dir_content
    except Exception as e:
        return f"Error: {str(e)}"

