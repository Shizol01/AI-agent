import os


def get_file_content(**kwargs):
    working_directory = kwargs.get("working_directory")
    file_path = kwargs.get("file_path")

    try:
        absolute_directory = os.path.abspath(os.path.join(working_directory, file_path))
        if not absolute_directory.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(absolute_directory):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        MAX_CHARS = 10000

        with open(absolute_directory, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) == MAX_CHARS:
                file_content_string += f'\n...File "{absolute_directory}" truncated at 10000 characters'
            
        return file_content_string
        

       
    except Exception as e:
        return f"Error: {e}"