import os
from config import MAX_CHARS
# from google.genai import types

# schema_get_file_content = types.FunctionDeclaration(
#     name="get_file_content",
#     description="Returns the content of a file in a specified directory relative to the working directory",
#     parameters=types.Schema(
#         type=types.Type.OBJECT,
#         properties={
#             "file_path": types.Schema(
#                 type=types.Type.STRING,
#                 description="File path to read from, relative to the working directory (default is the working directory itself)",
#             ),
#         },
#     ),
# )

def get_file_content(working_directory, file_path="."):
    if file_path==".":
        directory_called = "current"
    else:
        directory_called = file_path
        
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_dir_abs, file_path))
    
    # Will be True or False
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

    if not valid_target_file:
        return f'Error: Cannot read "{directory_called}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{directory_called}"'
    
    try:
        with open(target_file, 'r') as f:
            content = f.read(MAX_CHARS)
            if f.read(1):  # If there is more content beyond MAX_CHARS
                content += f'[...File "{directory_called}" truncated at {MAX_CHARS} characters]'
        return f"Content of {directory_called}:\n{content}"
    except Exception as e:
        raise RuntimeError(f"Error: accessing file: {str(e)}")