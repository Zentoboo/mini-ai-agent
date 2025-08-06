import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not full_path.startswith(working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found.'
    if not full_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        command = ['python', full_path] + args

        completed_process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=working_directory
        )
        output_lines = []
        if completed_process.stdout:
            output_lines.append(
                f"STDOUT:\n{completed_process.stdout.strip()}")

        if completed_process.stderr:
            output_lines.append(f"STDERR:\n{completed_process.stderr.strip()}")

        if completed_process.returncode != 0:
            output_lines.append(
                f"Process exited with code {completed_process.returncode}")

        if not output_lines:
            return "No output produced."
        
        return "\n".join(output_lines)
    except Exception as e:
        return f"Error: executing Python file: {e}"
