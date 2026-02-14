# Boot Dev AI Project

**Overview**
This repo contains:
- A Gemini-powered CLI chatbot in `main.py`.
- A simple expression calculator CLI in `calculator/main.py` with unit tests.
- A `get_files_info` utility for directory listings in `functions/get_files_info.py`.

**Requirements**
- Python 3.12+
- `uv` (optional, for running scripts with the lockfile)
- A Gemini API key in `GEMINI_API_KEY`

**Setup**
1. Create a `.env` file with your key:
```bash
GEMINI_API_KEY=your_key_here
```
2. Install dependencies (one option):
```bash
uv sync
```

**Gemini Chatbot**
Run the CLI chatbot:
```bash
uv run python main.py "Hello from the CLI"
```
Enable verbose token output:
```bash
uv run python main.py "Hello" --verbose
```

**Calculator CLI**
Run the calculator:
```bash
uv run python calculator/main.py "3 + 5"
```
Output is formatted JSON with the expression and result.

**Utilities**
`get_files_info(working_directory, directory=".")` returns a formatted listing of the target directory, with basic validation and error messages.

**Tests**
Run calculator unit tests:
```bash
uv run python calculator/tests.py
```
Run the `get_files_info` test script:
```bash
uv run python test_get_files_info.py
```
