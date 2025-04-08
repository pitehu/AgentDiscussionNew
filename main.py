# main.py

from roles import ROLES
from agent import Agent
from config import DEFAULT_MODEL, DEFAULT_TEMPERATURE,get_max_responses
from conversation import Conversation
from data_strategies import GenericDataStrategy
from message_strategies import GenericMessageStrategy
from discussion_modes import GenericDiscussionMode
import logging

def main(llm_count=1, persona_type=None, phases="three_stage", generation_method="dependent", 
         selection_method="rating", discussion_method="all_at_once", 
         discussion_order_method="fixed", task_type="PS", replacement_pool_size=0, 
         skip_to_discussion=False):
    try:
        if persona_type == 'none':
            system_messages = [""] * llm_count
        elif persona_type == 'same':
            system_messages = [ROLES["Same_Persona"]] * llm_count
        elif persona_type == 'different':
            personas = ["Persona_1", "Persona_2", "Persona_3"]
            system_messages = [ROLES[persona] for persona in personas[:llm_count]]
       

        # Handle single or multiple models
        if isinstance(DEFAULT_MODEL, list):
            if len(DEFAULT_MODEL) < llm_count:
                raise ValueError("Not enough models in DEFAULT_MODEL for the number of agents.")
            agent_models = DEFAULT_MODEL[:llm_count]  # Assign models from the list
        else:
            agent_models = [DEFAULT_MODEL] * llm_count  # Use the same model for all agents

        # Create agents with assigned models
        agents = []
        for i, (system_message, model_name) in enumerate(zip(system_messages, agent_models)):
            agent = Agent(name=f"Agent_{i+1}", system_message=system_message, model_name=model_name)
            agents.append(agent)
        
        print(agents)

    #    agents = []

        # for i, system_message in enumerate(system_messages):
        #     agent = Agent(name=f"Agent_{i+1}", system_message=system_message)
        #     agents.append(agent)
        # print(agents)

        # task_config = {
        #     "task_type": "PS",               # "AUT" or "PS"
        #     "phases": phases,          # "three_stage" or "direct_discussion"
        #     "generation_method": generation_method, # "independent" or "dependent"
        #     "selection_method": "rating", # "selectionTop" or "rating"
        #     "discussion_method": "all_at_once",  # "all_at_once" or "one_by_one", "open", or "iterative_refinement", or "creative"
        #     "discussion_order_method": "fixed",  # "fixed" or "random" or "hand_raising"
        #     "persona_type":persona_type,
        #     "llm_count":llm_count,
        #     "model":DEFAULT_MODEL,
        #     "temperature":DEFAULT_TEMPERATURE,
        #     "replacement_pool_size": 0
        # }

        task_config = {
            "task_type": task_type,               # "AUT" or "PS"
            "phases": phases,          # "three_stage" or "direct_discussion"
            "generation_method": generation_method, # "independent" or "dependent"
            "selection_method": selection_method, # "selectionTop" or "rating"
            "discussion_method": discussion_method,  # "all_at_once" or "one_by_one", "open", or "iterative_refinement", or "creative"
            "discussion_order_method": discussion_order_method,  # "fixed" or "random" or "hand_raising"
            "persona_type": persona_type,
            "llm_count": llm_count,
            "model": DEFAULT_MODEL,
            "temperature": DEFAULT_TEMPERATURE,
            "replacement_pool_size": replacement_pool_size
        }

        data_strategy = GenericDataStrategy(task_config=task_config)
        message_strategy = GenericMessageStrategy(task_config=task_config, data_strategy=data_strategy)
        conversation = Conversation(agents=agents, data_strategy=data_strategy, task_config=task_config)
        discussion = GenericDiscussionMode(conversation, task_config, message_strategy)

        # skip_to_discussion parameter
        discussion.run(skip_to_discussion=False)
    except Exception as e:
        logging.error("An error occurred during the discussion: %s", e)
    finally:
        # Always try to save the chat history even if there was an error
        if 'conversation' in locals():
            conversation.save_chat_history()


if __name__ == "__main__":
    # Default: False (set to True for debugging) 
    main(llm_count=3, persona_type="same")

