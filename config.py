# config.py

import os


DEFAULT_MODEL = os.getenv("DEFAULT_MODEL",'o3-mini') #gpt-4o,o1-mini o3-mini, deepseek-ai/DeepSeek-R1, gemini-2.0-flash-thinking-exp,'gemini-2.0-flash-thinking-exp','deepseek-ai/DeepSeek-R1','o1' 'gemini-2.0-flash-thinking-exp','deepseek-ai/DeepSeek-R1','o1' 
DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", 1))

def get_max_responses(phases: str):
    if phases == "direct_discussion":
        return 30
    else:
        return 20


