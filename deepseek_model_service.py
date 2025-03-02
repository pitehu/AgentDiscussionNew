# together_model_service.py
from together import Together
from base_model_service import BaseModelService  # Import the base class
import re

class DeepSeekModelService(BaseModelService):
    """
    Model service for interacting with Together AI.
    """
    def __init__(self):
        self.client = Together(api_key = 'tgp_v1_8NILfECFUm331WsMBSH5_Lerhy3sevt80Kv2ecX0nIU')

    def generate_response(self, messages, model=None, temperature=0.6):
        """
        Generates a response using Together AI.
        """
        try:
            response = self.client.chat.completions.create(
                model=model if model else "deepseek-ai/DeepSeek-R1",
                messages=messages,
                temperature = temperature
            )
            raw_content = response.choices[0].message.content
            content_after_think = re.split(r'</think>\s*', raw_content, maxsplit=1)[-1].strip()
            while '</think>' in content_after_think:
                content_after_think = re.split(r'</think>\s*', content_after_think, maxsplit=1)[-1].strip()
            print("after think:", content_after_think)
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            reasoning_tokens = 0

            return content_after_think,prompt_tokens,completion_tokens, reasoning_tokens
        except Exception as e:
            print(f"Error generating response with Together AI: {e}")
            return "(No response due to error)"