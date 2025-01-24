# config.py

import os

# 默认模型
DEFAULT_MODEL = "gpt-4o"

# 其他调整的模型
MODEL_FOR_PARSE = "gpt-4o-mini"

def get_max_responses(phases: str):
    """
    如果 phases = 'direct_discussion'，可返回30；
    如果 phases = 'three_stage'，可返回20。
    具体 one_by_one的10次限制，会放在 discussion_modes.py 里处理。
    """
    if phases == "direct_discussion":
        return 30
    else:
        return 20
