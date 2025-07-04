import os 

def get_files_info(working_directory, directory=None):
    full_path = os.path.join(working_directory, directory)

    if os.path.commonpath([os.path.abspath(working_directory), os.path.abspath(full_path)]) != os.path.abspath(working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif os.path.isdir(full_path) == False:
        return f'Error: "{directory}" is not a directory'
    else:
        try:
            path = os.path.abspath(full_path)
            contents = os.listdir(path)
            results = []

            for content in contents:
                full_path_c = os.path.join(path, content)
                file_size = os.path.getsize(full_path_c)
                is_dir = os.path.isdir(full_path_c)
                results.append(f"{content}: file_size={file_size} bytes, is_dir={is_dir}")

            return "\n".join(results) if results else f'"{directory}" is an empty directory.'
        except Exception as e:
            return f"Error: {e}"
