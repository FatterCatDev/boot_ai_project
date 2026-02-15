import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to file in specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="Base working directory from which to write the file",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["working_directory", "file_path", "content"]
    ),
)

def write_file(working_directory, file_path, content):
    if file_path == ".":
        directory_called = "current"
    else:
        directory_called = file_path
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_dir_abs, file_path))

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