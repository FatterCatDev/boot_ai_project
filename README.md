# Boot Dev AI Project

A learning project for building a small AI agent. It uses Gemini function calling to safely interact with a local workspace and includes a simple calculator CLI to exercise tool calls.

**Overview**
- CLI agent in `main.py` that uses Gemini function calling and a system prompt in `system_prompt/prompts.py`.
- Tool implementations in `functions/` with safety checks. `call_function.py` forces the working directory to `./calculator`.
- Calculator CLI in `calculator/main.py` with parsing and rendering in `calculator/pkg/`.

**Requirements**
- Python 3.12+
- A Gemini API key in `GEMINI_API_KEY`
- Optional: `uv` for dependency management

**Setup**
1. Create a `.env` file with your key:
```bash
GEMINI_API_KEY=your_key_here
```
2. Install dependencies (choose one):
```bash
uv sync
```
```bash
python -m pip install .
```

**Agent Usage**
Run the CLI agent:
```bash
uv run python main.py "List the files in the calculator directory"
```
Enable verbose output (shows function calls and token counts):
```bash
uv run python main.py "Read calculator/main.py" --verbose
```

**Available Tool Functions**
The agent can call these tools (see `functions/`), with the working directory locked to `./calculator` in `call_function.py`:
- `get_files_info(working_directory, directory=".")`
- `get_file_content(working_directory, file_path)`
- `write_file(working_directory, file_path, content)`
- `run_python_file(working_directory, file_path, args=[])`

**Calculator CLI**
Run the calculator:
```bash
uv run python calculator/main.py "3 + 5 * 2"
```
Notes:
- Tokens must be space-separated.
- Supported operators: `+`, `-`, `*`, `/`.
- Integers only, no parentheses.

**Configuration**
See `config.py` for:
- `modle_name` (Gemini model name)
- `MAX_CHARS` (max file content returned by `get_file_content`)
- `LOOP_LIMIT` (max tool-calling iterations)

**Tests**
Run calculator unit tests:
```bash
uv run python calculator/tests.py
```
Run tool test scripts (print results):
```bash
uv run python test_get_files_info.py
```
```bash
uv run python test_get_file_content.py
```
```bash
uv run python test_run_python_file.py
```
```bash
uv run python test_write_file.py
```
