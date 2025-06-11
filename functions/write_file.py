import os

def write_file(**kwargs):
    working_directory = kwargs.get("working_directory")
    file_path = kwargs.get("file_path")
    content = kwargs.get("content")

    try:

        absolute_directory = os.path.abspath(os.path.join(working_directory, file_path))
        parent_dir = os.path.dirname(absolute_directory)
        if not absolute_directory.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
        
        with open(absolute_directory, "w") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
