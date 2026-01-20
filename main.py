import os

from dotenv import load_dotenv

load_dotenv()


def main():
    openai_key = os.getenv("OPENAI_API_KEY")


    print("Hello from py-llm-test-app!")
    print(f"OpenAI API Key: {openai_key}")



if __name__ == "__main__":
    main()
