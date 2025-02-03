# config.py

import os

OPENAI_API_KEY = "" #Additional information may be needed.

# default model
DEFAULT_MODEL = "gpt-4o"

# other models
MODEL_FOR_PARSE = "gpt-4o-mini"

def get_max_responses(phases: str):

    if phases == "direct_discussion":
        return 30
    else:
        return 20
