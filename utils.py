# utils.py

from tiktoken import encoding_for_model

def calculate_tokens(messages, model="gpt-4"):
    """
    Calculate the number of tokens used in a list of messages or parsed content.
    Each input should be a dictionary with 'role' and 'content', or a parsed object.
    """
    encoding = encoding_for_model(model)
    token_count = 0

    for msg in messages:
        if isinstance(msg, dict) and "content" in msg:
            # Handle message format with role and content
            token_count += len(encoding.encode(msg["content"]))
        elif isinstance(msg, str):
            # Handle plain string
            token_count += len(encoding.encode(msg))
        else:
            # Handle parsed object by converting it to JSON string
            from pydantic import BaseModel
            if isinstance(msg, BaseModel):
                token_count += len(encoding.encode(msg.json()))
            elif isinstance(msg, dict):
                import json
                token_count += len(encoding.encode(json.dumps(msg)))
            else:
                raise ValueError("Unsupported message format for token calculation.")

    return token_count

