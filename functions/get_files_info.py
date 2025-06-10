import os


def get_files_info(working_directory, directory=None):
    try:
        absolute_directory = os.path.abspath(os.path.join(working_directory, directory))
        if not absolute_directory.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(absolute_directory):
            return f'Error: "{directory}" is not a directory'
        
        file_list = os.listdir(absolute_directory)
        detailed_list = []
        for file in file_list:
            file_path = os.path.join(absolute_directory, file)
            is_dir = os.path.isdir(file_path)
            file_size = os.path.getsize(file_path)
            detailed_list.append(f"- {file}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(detailed_list)
    except Exception as e:
        return f"Error: {e}"