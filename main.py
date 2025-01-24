# main.py

from roles import ROLES
from config import get_max_responses
from agent import Agent
from conversation import Conversation
from data_strategies import GenericDataStrategy
from message_strategies import GenericMessageStrategy
from discussion_modes import GenericDiscussionMode
import logging

def main(skip_to_discussion=False):
    try:
        chosen_roles = ["CEO", "CFO", "CTO"]
        agents = []
        for role_name in chosen_roles:
            sys_msg = ROLES.get(role_name, f"You are {role_name}.")
            agent = Agent(name=role_name, system_message=sys_msg, config={"model": "gpt-4o-mini"})
            agents.append(agent)

        task_config = {
            "task_type": "AUT",               # "AUT" or "PS"
            "phases": "three_stage",          # "three_stage" or "direct_discussion"
            "generation_method": "dependent", # "independent" or "dependent"
            "selection_method": "rating", # "selectionTop" or "rating"
            "discussion_method": "all_at_once",  # "all_at_once" or "one_by_one"
            "discussion_order_method": "random"  # "fixed" or "random" or "hand_raising"
        }
        data_strategy = GenericDataStrategy(task_config=task_config)
        message_strategy = GenericMessageStrategy(task_config=task_config, data_strategy=data_strategy)
        conversation = Conversation(agents=agents, data_strategy=data_strategy, task_config=task_config)
        discussion = GenericDiscussionMode(conversation, task_config, message_strategy)

        # 调用 run 时传递 skip_to_discussion 参数
        discussion.run(skip_to_discussion=skip_to_discussion)
    except Exception as e:
        logging.error("An error occurred during the discussion: %s", e)
    finally:
        # Always try to save the chat history even if there was an error
        if 'conversation' in locals():
            conversation.save_chat_history()


if __name__ == "__main__":
    # 控制是否直接跳到讨论阶段
    main(skip_to_discussion=False)