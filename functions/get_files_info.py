import os 

def get_files_info(working_directory, directory=None):
    if os.path.commonpath([os.path.abspath(working_directory), os.path.abspath(f"{working_directory}/{directory}")]) != os.path.abspath(working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif os.path.isdir(f"{working_directory}/{directory}") == False:
        return f'Error: "{directory}" is not a directory'
    else:
        path = os.path.abspath(f"{working_directory}/{directory}")
        contents = os.listdir(path)
        results = []

        for content in contents:
            full_path = os.path.join(path, content)
            file_size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)
            results.append(f"{content}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(results) if results else f'"{directory}" is an empty directory.'



print(get_files_info("calculator", "../"))

                        
                    

# print(os.path.abspath("calculator"))
# print(os.path.abspath("calculator/pkg"))
# print(os.path.commonpath([os.path.abspath("calculator"), os.path.abspath("calculator/pkg")]))


# CHECK COMMON PATH LOGICCC FUCK MEE. CUNT 


# path = os.path.abspath("calculator") ## variable should be directory
# isdir = os.path.isdir("pkg")

# directory = os.listdir(path)
# x = os.path.getsize("calculator/tests.py")
# y = os.path.isfile("calculator/tests.py")

# # print(x)
# # print(y)
# # print(path)
# # print(isdir)
# # print(contents)
# print(directory)

# # for content in directory:
# #     if os.path.isdir(os.path.join(path, content)) == True:
# #         file_size = os.path.getsize(os.path.join(path, content))
# #         is_dir = os.path.isdir(os.path.join(path, content))
# #         print(f"{content}: file_size={file_size} bytes, is_dir={is_dir}")
# #     elif os.path.isfile(os.path.join(path, content)) == True:
# #         file_size = os.path.getsize(os.path.join(path, content))
# #         is_dir = os.path.isdir(os.path.join(path, content))
# #         print(f"{content}: file_size={file_size} bytes, is_dir={is_dir}")


