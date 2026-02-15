import os
# from google.genai import types

# schema_write_file = types.FunctionDeclaration(
#     name="write_file",
#     description="Writes content to a file in a specified directory relative to the working directory",
#     parameters=types.Schema(
#         type=types.Type.OBJECT,
#         properties={
#             "file_path": types.Schema(
#                 type=types.Type.STRING,
#                 description="File path to write to, relative to the working directory",
#             ),
#             "content": types.Schema(
#                 type=types.Type.STRING,
#                 description="Content to write to the file",
#             ),
#         },
#     ),
# )

def write_file(working_directory, file_path_relative, content):
    if file_path_relative == ".":
        directory_called = "current"
    else:
        directory_called = file_path_relative
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_dir_abs, file_path_relative))

    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot write to "{directory_called}" as it is outside the permitted working directory'
    
    if os.path.isdir(target_dir):
        return f'Error: Cannot write to "{directory_called}" as it is a directory'
    
    os.makedirs(os.path.dirname(target_dir), exist_ok=True)
    try:
        with open(target_dir, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{directory_called}" ({len(content)} characters written)'
    except Exception as e:
        raise RuntimeError(f"Error: writing to file: {str(e)}")