import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    abs_working_directory = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)
    
    if not abs_full_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_full_path):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_full_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        sub_args = []
        sub_args.append("python")
        sub_args.append(abs_full_path)
        sub_args += args
        completed_process = subprocess.run(sub_args, capture_output=True, text=True, timeout=30, cwd=abs_working_directory)

        result = ""
        if completed_process.stdout:
            result += f"STDOUT: {completed_process.stdout}"
        if completed_process.stderr:
            result += f"STDERR: {completed_process.stderr}"
        if completed_process.returncode != 0:
            result += f"Process exited with code {completed_process.returncode}"
        if result == "":
            result += "No output produced."
        
        return result

    except Exception as e:
        return f"Error: executing Python file: {e}"