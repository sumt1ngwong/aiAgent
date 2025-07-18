import os
from dotenv import load_dotenv
from google import genai 
from google.genai import types
import sys
from functions.call_function import *
from functions.get_files_info import *
from functions.get_file_content import *
from functions.write_file import *
from functions.run_python_file import *

def main():

    is_verbose = "--verbose" in sys.argv

    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

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

    i = 0 
    while i < 20:
        try:
            # contents = input("Contents for LLM: ")
            response = client.models.generate_content(
                model="gemini-2.0-flash-001", 
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions_i, available_functions_c, available_functions_p, available_functions_w ], system_instruction=system_prompt))

            for candidate in response.candidates:
                messages.append(candidate.content)

            final_text = response.candidates[0].content.parts[0].text
            if final_text and not response.function_calls:
                print(final_text)
                break
        

            function_call_part = response.function_calls


            if function_call_part:
                for func in function_call_part:
                    function_call_result = call_function(func, is_verbose)
                    print(function_call_result)
                    
                    if not function_call_result.parts:
                        raise Exception("No parts returned from call_function.")
                        

                    first_part = function_call_result.parts[0]

                    if not hasattr(first_part, "function_response") or not hasattr(first_part.function_response, "response"):
                        raise Exception("Missing function_response or response in result.")

                    if is_verbose:
                        print(f"-> {first_part.function_response.response}")

                    i += 1
                    messages.append(function_call_result)
            else:
                # If no final text and no function calls, what should happen?
                # Perhaps print a message and break to prevent an infinite loop.
                print("LLM did not provide a final response or function call. Breaking.")
                break

            i += 1

        except Exception as e:
                print("Error", e)
                break

  

    if "--verbose" in sys.argv:
        print("User prompt:", user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
        

if __name__ == "__main__":
    main()
