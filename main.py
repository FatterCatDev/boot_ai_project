import os
from dotenv import load_dotenv
from google import genai
import argparse

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
args = parser.parse_args()

def main():
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=args.user_prompt,
    )

    if response.usage_metadata is None:
        raise RuntimeError("Response is missing usage metadata.")

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    total_tokens = response.usage_metadata.total_token_count

    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
    print("Total tokens:", total_tokens)
    print(response.text)


if __name__ == "__main__":
    main()
