# agent.py

from openai import OpenAI
from config import OPENAI_API_KEY, DEFAULT_MODEL
import logging
from utils import calculate_tokens

class Agent:
    def __init__(self, name, system_message, config=None):
        self.name = name
        self.system_message = system_message.strip()
        self.config = config if config else {}
        self.history = []

    def generate_response(self, messages):
        """
        Generate a response using OpenAI API and return the reply along with token counts.
        """
        model_name = self.config.get("model", DEFAULT_MODEL)
        client = OpenAI(api_key=OPENAI_API_KEY)

        # Calculate prompt tokens
        prompt_tokens = calculate_tokens(messages, model=model_name)

        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=messages
            )

            # Extract the reply content
            reply = response.choices[0].message.content.strip()
            self.history.append({"role": "assistant", "content": reply})

            # Calculate completion tokens
            completion_tokens = calculate_tokens([{"role": "assistant", "content": reply}], model=model_name)

            # Return the reply and token counts
            return reply, prompt_tokens, completion_tokens
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "(No response due to error)"
