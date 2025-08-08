from google import genai
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file

FUNCTION_DICTIONARY = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file
}


def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    if function_name in FUNCTION_DICTIONARY:
        function = FUNCTION_DICTIONARY[function_name]
        kwargs = dict(function_args) if function_args else {}
        kwargs["working_directory"] = "./calculator"

        try:
            function_result = function(**kwargs)
        except TypeError as e:
            error_msg = f"Parameter error in {function_name}: {str(e)}"
            print(f"ERROR: {error_msg}")
            return genai.types.Content(
                role="tool",
                parts=[
                    genai.types.Part.from_function_response(
                        name=function_name,
                        response={"error": error_msg},
                    )
                ],
            )
    else:
        return genai.types.Content(
            role="tool",
            parts=[
                genai.types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    return genai.types.Content(
        role="tool",
        parts=[
            genai.types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
