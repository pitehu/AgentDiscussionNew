# gemini_model_service.py
from google import genai
from base_model_service import BaseModelService  # Import the base class
import re

class GeminiModelService(BaseModelService):
    """
    Model service for interacting with Google's Gemini API.
    """
    def __init__(self):
        self.client = genai.Client(api_key="AIzaSyDyg6V00aMA-5BPILrnjrG33Um-a9cxnlY")

    def generate_response(self, messages, model="gemini-2.0-flash-thinking-exp",temperature=0.7):
        """
        Generates a response using Google's Gemini API.
        """
        try:
            # Convert messages into a format Gemini API accepts
            prompt = "\n".join([msg["content"] for msg in messages if "content" in msg])

            # Make API call
            response = self.client.models.generate_content(
                model=model,
                contents=prompt
            )

            # Extract token usage (if available)
            prompt_tokens = response.usage_metadata.prompt_token_count
            completion_tokens = response.usage_metadata.candidates_token_count
            reasoning_tokens = 0

            return response.text, prompt_tokens, completion_tokens, reasoning_tokens

        except Exception as e:
            print(f"Error generating response with Gemini API: {e}")
            return "(No response due to error)", 0, 0
