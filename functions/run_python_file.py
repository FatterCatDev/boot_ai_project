import subprocess
import os

def run_python_file(working_directory, file_path_relative, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_dir_abs, file_path_relative))

    # Will be True or False
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

    match (
        valid_target_file, 
        os.path.isfile(target_file),
        ".py" in target_file
        ):
        case (False, _, _):
            return f'Error: Cannot execute "{file_path_relative}" as it is outside the permitted working directory'
        case (_, False, _):
            return f'Error: "{file_path_relative}" does not exist or is not a regular file'
        case (_, _, False):
            return f'Error: "{file_path_relative}" is not a Python file'
        case (True, True, True):
            pass  # continue

    try:
        command = ["python", target_file]
        result = subprocess.run(
            command + (args if args else []), 
            cwd=working_dir_abs, 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30
            )

        if not result.stdout and not result.stderr:
            return "No output produced"
        else:
            output = f"STDOUT: {result.stdout.strip()} "
            error = f"STDERR: {(result.stderr.strip() if result.stderr.strip() else 'None')} "
            combined_output = "\n".join(filter(None, [output, error]))

        if result.returncode != 0:
            return f'Error: Process exited with code {result.returncode}'
        return f'Successfully executed "{file_path_relative}" with output:\n{combined_output}\n---'
    except subprocess.TimeoutExpired:
        return f'Error: Execution of "{file_path_relative}" timed out'
    except Exception as e:
        raise RuntimeError(f"Error: executing Python file: {e}")