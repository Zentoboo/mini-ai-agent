import os 
import sys
from dotenv import load_dotenv
from google import genai


def main():
    print("Hello from mini-ai-agent!")
    
    if len(sys.argv) < 2:
        print("Usage: python main.py \"Your prompt here...\"")
        sys.exit(1)
    user_prompt = sys.argv[1]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Missing GEMINI_API_KEY in environment.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=user_prompt
    )
    print(response.text)
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()
