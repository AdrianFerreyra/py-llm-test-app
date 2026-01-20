from openai import OpenAI

from src.application.ports import LLMPort


class OpenAILLMAdapter(LLMPort):
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def call(self, message: str) -> str:
        response = self.client.responses.create(
            model="gpt-4.1",
            input=[
                {"role": "user", "content": message},
            ],
        )
        return response.output_text
