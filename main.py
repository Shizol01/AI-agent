import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
import argparse

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
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', contents= messages)
        if args.verbose:
            print(f"User prompt: {prompt}")
            print(response.text)
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count
            print(f"Prompt tokens: {prompt_tokens} \nResponse tokens: {response_tokens}")
        else:
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
