from google.genai import types
from functions.get_file_content import *
from functions.get_files_info import *
from functions.run_python_file import *
from functions.write_file import *

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_arguments = function_call_part.args.copy()
    function_arguments["working_directory"] = "./calculator" 
    
    if verbose == True:
        print(f"Calling function: {function_name}({function_arguments})")
        #return f"{function_call_part.name}(**{{'working_directory': './calculator', '{k}': '{v}'}})"
    else:
        print(f" - Calling function: {function_name}")
        #return f"{function_call_part.name}(**{{'working_directory': './calculator', '{k}': '{v}'}})"

    mapping = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file
    }
    
    if function_name not in mapping:
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"error": f"Unknown function: {function_call_part.name}"},
            )
        ],
    )

    try:
        actual_function_call = mapping[function_name] 

        function_result = actual_function_call(**function_arguments)

    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": str(e)},
                )
            ],
        )

        # Success — return result
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )