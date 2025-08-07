import os
import sys
from dotenv import load_dotenv
from google import genai
from functions.get_files_info import schema_get_files_info


available_functions = genai.types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
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
    else:
        print("AI response:", response.text, "\n")

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()
