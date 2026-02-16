import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from system_prompt.prompts import system_prompt
from config import modle_name, LOOP_LIMIT
from call_function import available_functions, call_function

load_dotenv()
try:
    api_key = os.environ.get("GEMINI_API_KEY")
except KeyError:
    raise RuntimeError(
        "GEMINI_API_KEY environment variable not set. Please set it to your Gemini API key."
    )
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")

parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

args = parser.parse_args()
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

def main():
    for i in range(LOOP_LIMIT):
        response = client.models.generate_content(
        model=modle_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
            temperature=0.7,
            ),
        )

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.usage_metadata is None:
            raise RuntimeError("Response is missing usage metadata.")

        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        total_tokens = response.usage_metadata.total_token_count
        function_responses = []

        if response.function_calls:
            for call in response.function_calls:
                function_call_result = call_function(call, args.verbose)
                if not function_call_result.parts:
                    raise RuntimeError("Function call result is missing content parts.")
                elif not function_call_result.parts[0].function_response:
                    raise RuntimeError("Function call response is missing.")
                elif not function_call_result.parts[0].function_response.response:
                    raise RuntimeError("Function call response is empty.")
                function_responses.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"User prompt: {args.user_prompt}")
                    print(f"Prompt tokens: {prompt_tokens}")
                    print(f"Response tokens: {response_tokens}")
                    print("Total tokens:", total_tokens)
                    print("------------------------")
                    print(f"-> {function_call_result.parts[0].function_response.response}")

        else:
            print(response.text)  # Print the response text if there are no function calls
            break  # Exit the loop if there are no function calls

        messages.append(types.Content(role="user", parts=function_responses))

        if i >= LOOP_LIMIT - 1:  # Check if the maximum number of iterations has been reached
             print("Maximum iterations reached. Ending conversation.")
             raise SystemExit(1) # Exit the program after reaching the maximum number of iterations

if __name__ == "__main__":
    main()
