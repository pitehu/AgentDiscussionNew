import time
import logging
from main import main

task_combinations = [
    # {"llm_count": 3, "persona_type": "same", "phases": "three_stage", "generation_method": "independent"},
    #Open
    #{"llm_count": 3, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "open", "discussion_order_method":"fixed"},
    #Instructed
    #{"llm_count": 3, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"fixed", "replacement_pool_size":0},
    # #Instructed - replacement pool size top 5 
    #{"llm_count": 3, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"fixed", "replacement_pool_size":5},
    #Instructed - replcaement pool 0 - hand_raising

    {"llm_count": 3, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"hand_raising", "replacement_pool_size":0},
    # # Iterative refinement
    #{"llm_count": 3, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method":"fixed", "replacement_pool_size":0},
    # # Additional Idea Generation 
    # {"llm_count": 3, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method":"fixed", "replacement_pool_size":0},

]

for config in task_combinations:
    llm_count = config["llm_count"]
    persona_type = config["persona_type"]
    phases = config["phases"]
    generation_method = config["generation_method"]
    print("running config", config)
    print(f"\nRunning: llm_count={llm_count}, persona_type={persona_type}, phases={phases}, generation_method={generation_method}")
    logging.info(f"Starting run with llm_count={llm_count}, persona_type={persona_type}, phases={phases}, generation_method={generation_method}")

    try:
        main(**config)  # This passes all parameters from the dictionary to the function
    except Exception as e:
        logging.error(f"Error during run: {e}")

    time.sleep(2)

print("\nAll tasks completed.")
