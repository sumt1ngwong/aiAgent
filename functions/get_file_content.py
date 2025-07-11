import os 
from google.genai import types

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)

    if os.path.commonpath([os.path.abspath(working_directory), os.path.abspath(full_path)]) != os.path.abspath(working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif os.path.isfile(full_path) == False:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    else:
        try:
            maximum_characters = 10000
            with open(full_path, "r") as f:
                content = f.read()
                character_count = len(content)

            if character_count > maximum_characters:
                with open(full_path, "r") as f:
                    file_content_string = f.read(maximum_characters)
                return f'{file_content_string}[...File "{file_path}" truncated at 1000 characters]'
            else:
                with open(full_path, "r") as f:
                    file_content_string = f.read()
                return file_content_string
        except Exception as e:
            return f"Error: {e}"
        

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first 10,000 characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file in respect to the working directory.",
            ),
        },
    ),
)

available_functions_c = types.Tool(
    function_declarations=[
        schema_get_file_content,
    ]
)

