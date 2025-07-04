import os 

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)

    if os.path.commonpath([os.path.abspath(working_directory), os.path.abspath(full_path)]) != os.path.abspath(working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    elif os.path.exists(working_directory) == False:
        try:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(file_path, "w") as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
            return f"Error: {e}"
    else:
        with open(os.path.abspath(full_path), "w") as f:
                f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'