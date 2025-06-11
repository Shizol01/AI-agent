import os
import subprocess

def run_python_file(**kwargs):
    working_directory = kwargs.get("working_directory")
    file_path = kwargs.get("file_path")
    
    try:
        absolute_directory = os.path.abspath(os.path.join(working_directory, file_path))
        if not os.path.exists(absolute_directory):
            return f'Error: File "{file_path}" not found.'
        if not absolute_directory.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not absolute_directory.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        cli = ["python3", absolute_directory]
        result = subprocess.run(cli, timeout=30, capture_output=True)
        output = ""
        if result.stdout.decode():
            output += f"STDOUT: {result.stdout.decode()}\n"
        if result.stderr.decode():
            output += f"STDERR: {result.stderr.decode()}\n"
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}"
        if output == "":
            output += "No output produced."

        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"



