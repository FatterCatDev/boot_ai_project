import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The base working directory from which to list files. The target directory must be within this working directory.",
            ),
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. Use '.' for the current directory.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    if directory==".":
        directory_called = "current"
    else:
        directory_called = directory
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_dir_abs, directory))
    
    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(target_dir):
        return f'Error: "{target_dir}" is not a directory'
    
    try:
        if os.path.isdir(target_dir):
            lines = []
            for item in os.listdir(target_dir):
                item_path = os.path.join(target_dir, item)
                lines.append(
                    f" - {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
                )
            items_info = "\n".join(lines)
            return f"Result for {directory_called} directory:\n{items_info}"
    except Exception as e:
        raise RuntimeError(f"Error: accessing directory: {str(e)}")