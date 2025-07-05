import os
from dotenv import load_dotenv
from google import genai 
from google.genai import types
import sys

def main():
    system_prompt = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""

    if len(sys.argv) < 2:
        print("No prompt provided.")
        sys.exit(1)


    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)


    user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    # contents = input("Contents for LLM: ")
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt))

    print(response.text)
    if "--verbose" in sys.argv:
        print("User prompt:", user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
        



if __name__ == "__main__":
    main()
