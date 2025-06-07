import groq
import json
from config import get_api_key

class Agent:
    def __init__(self):
        api_key = get_api_key()
        self.client = groq.Groq(api_key=api_key)

    def ask(self, prompt: str):
        messages = [
            {
                "role": "system",
                "content": (
                    "You're a helpful book assistant. "
                    "Extract the genre, author, and length from the user's prompt. "
                    "Return the result in JSON format like: "
                    '{"genre": "mystery", "author": "Agatha Christie", "length": "short"}'
                )
            },
            {"role": "user", "content": prompt}
        ]

        response = self.client.chat.completions.create(
            model="meta-llama/llama-4-maverick-17b-128e-instruct",
            messages=messages,
        )

        content = response.choices[0].message.content
        try:
            return json.loads(content)
        except Exception:
            return {"genre": "", "author": "", "length": ""}
