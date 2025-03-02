# azure_model_service.py
import os
from openai import AzureOpenAI
from base_model_service import BaseModelService 

class AzureModelService(BaseModelService):
    """
    Model service for interacting with Azure OpenAI.
    """
    def __init__(self):
        self.client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
            api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
            api_version=""
        )

    def generate_response(self, messages, model=None, temperature=0.7):
        """
        Generates a response using Azure OpenAI.
        """
        try:
            if model in ['o1-mini', 'o3-mini', 'o1']:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages
                )
                reasoning_tokens = response.usage.completion_tokens_details.reasoning_tokens
            else:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature  
                )
                reasoning_tokens = 0
            
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens

            return response.choices[0].message.content.strip(),prompt_tokens,completion_tokens,reasoning_tokens
        except Exception as e:
            print(f"Error generating response with Azure OpenAI: {e}")
            return "(No response due to error)"

    def parse_response(self, messages, model=None, response_model=None):
        """
        Parses a response using Azure OpenAI. This is a conceptual method.
        """
        try:
            response = self.client.beta.chat.completions.parse(
                model=model,
                messages=messages,
                response_format=response_model  # This parameter is hypothetical
            )
            return response
        except Exception as e:
            print(f"Error parsing response with Azure OpenAI: {e}")
            return None
