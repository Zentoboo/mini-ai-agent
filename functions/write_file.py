import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a file at the specified path with the given content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file to write to."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file."
            )
        },
        required=["path", "content"]
    )
)

def write_file(working_directory, file_path, content):
    try:
        working_directory = os.path.abspath(working_directory)
        file_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not file_path.startswith(working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        parent_dir = os.path.dirname(file_path)
        os.makedirs(parent_dir, exist_ok=True)
        
        with open(file_path, "w", encoding="UTF-8") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"
