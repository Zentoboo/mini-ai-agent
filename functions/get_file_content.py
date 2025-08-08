import os
from functions.config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of the specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file to read."
            )
        },
        required=["file_path"]
    ),
)


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
