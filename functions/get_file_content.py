import os
from functions.config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        working_directory = os.path.abspath(working_directory)
        file_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not file_path.startswith(working_directory):
            return f'Error: Cannot access "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

        return file_content_string

    except Exception as e:
        return f"Error: {str(e)}"
