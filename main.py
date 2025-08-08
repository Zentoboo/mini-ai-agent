import os
import sys
from dotenv import load_dotenv
from google import genai
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function

available_functions = genai.types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories using get_files_info
- Read file contents using get_file_content  
- Execute Python files with optional arguments using run_python_file
- Write or overwrite files using write_file

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

IMPORTANT: When the user asks to "run [filename]", immediately call run_python_file with the filename. Don't ask questions or explain - just execute it.
"""

model_name = "gemini-2.0-flash"

def main():
    print("mini-ai-agent salutes you <3")

    if len(sys.argv) < 2:
        print("Usage: python main.py \"Your prompt here...\"")
        sys.exit(1)

    user_prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv[2:]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Missing GEMINI_API_KEY in environment.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=model_name,
        contents=user_prompt,
        config=genai.types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )

    function_calls = response.function_calls

    if function_calls:
        for fc in function_calls:
            print(f"Calling function: {fc.name}({fc.args})")
            function_call_result = call_function(fc, verbose=verbose)
            # Check for .parts[0].function_response.response
            try:
                response_value = function_call_result.parts[0].function_response.response
            except (AttributeError, IndexError, KeyError):
                raise RuntimeError("Function call did not return a valid response in .parts[0].function_response.response")
            if verbose:
                print(f"-> {response_value}")
    else:
        print("AI response:", response.text, "\n")

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

if __name__ == "__main__":
    main()