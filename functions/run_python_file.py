import os 
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)

    if os.path.commonpath([os.path.abspath(working_directory), os.path.abspath(full_path)]) != os.path.abspath(working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif os.path.exists(os.path.abspath(full_path)) == False:
        return f'Error: File "{file_path}" not found'
    elif file_path.endswith(".py") == False:
        return f'Error: "{file_path}" is not a Python file.'
    else:
        try:    
            result = subprocess.run(['python', file_path], timeout=30, capture_output=True, text=True, cwd=working_directory)

            if result.stdout or result.stderr:
                output = ""
                if result.stdout:
                    output += f"STDOUT: {result.stdout}"
                if result.stderr:
                    output += f"STDERR: {result.stderr}"
                if result.returncode != 0:
                    output += f"Process exited with code {result.returncode}"
                return output
            else:
                return "No output produced."
                        
        except Exception as e:
            return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
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

available_functions_p = types.Tool(
    function_declarations=[
        schema_run_python_file,
    ]
)
