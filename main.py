import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
import argparse
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    parser = argparse.ArgumentParser(description="Send prompt to Gemini")
    parser.add_argument("question", help="Pytanie użytkownika")
    parser.add_argument("--verbose", action="store_true", help="View detailed description")

    args = parser.parse_args()

    prompt = args.question
    messages = [types.Content(role="user", parts=[types.Part(text=args.question)])]
    system_prompt = system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """
    model = 'gemini-2.0-flash-001'

    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )   

    schema_get_file_content =types.FunctionDeclaration(
        name='get_file_content',
        description='Returns file content as string to 10 000 chars',
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description='Path to file, relative to working directory',
                ),
            },
        ),
    ) 

    schema_run_python_file =types.FunctionDeclaration(
        name='run_python_file',
        description='Runs python file in cli',
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description='Path to file, relative to working directory',
                ),
            },
        ),
    ) 

    schema_write_file =types.FunctionDeclaration(
        name='write_file',
        description='Runs python file in cli',
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description='Path to file, relative to working directory',),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description='String containing thing to write'
                ),
                
            },
        ),
    ) 

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,

    ]
)
    for i in range(20):
        try:
            response = client.models.generate_content(
                model=model,
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
                )
            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)
            if args.verbose:
                print(f"User prompt: {prompt}")
                prompt_tokens = response.usage_metadata.prompt_token_count
                response_tokens = response.usage_metadata.candidates_token_count
                print(f"Prompt tokens: {prompt_tokens} \nResponse tokens: {response_tokens}")
            if response.function_calls:
                for function_call_part in response.function_calls:
                    function_call_result = call_function(function_call_part, args.verbose)
                    if not function_call_result.parts[0].function_response.response:
                        raise Exception('Fatal error. No response.')
                    if args.verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                    messages.append(function_call_result)
            else:
                print(f"Final response:\n{response.text}")
                break
        except Exception as e:
            print(f"Error: {e}")
            exit(1)
        


if __name__ == "__main__":
    main()
