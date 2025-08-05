import os


def get_files_info(working_directory, directory="."):
    try:
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, directory))

        if not full_path.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
            
        entries = []
        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            is_dir = os.path.isdir(item_path)
            try:
                size = os.path.getsize(item_path)
            except OSError as e:
                size = 0
            entries.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(entries)

    except Exception as e:
        return f"Error: {str(e)}"