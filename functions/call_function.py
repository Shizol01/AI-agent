# call_function.py

from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from google import genai


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:    
        print(f" - Calling function: {function_call_part.name}")

    working_directory = "./calculator"
    function_name = function_call_part.name
    arguments = dict(function_call_part.args)
    arguments["working_directory"] = working_directory
    functions = {'get_file_content': get_file_content,
                 'get_files_info': get_files_info,
                 'run_python_file': run_python_file,
                 'write_file': write_file,
                 }

    if not function_name in functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )



    function_result = functions[function_name](**arguments)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
    