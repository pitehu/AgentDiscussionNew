import time
import logging
from main import main

task_combinations = [
    # {"llm_count": 3, "persona_type": "same", "phases": "three_stage", "generation_method": "independent"},
    {"llm_count": 3, "persona_type": "same", "phases": "three_stage", "generation_method": "dependent"},
     {"llm_count": 3, "persona_type": "same", "phases": "three_stage", "generation_method": "independent"},
      {"llm_count": 3, "persona_type": "same", "phases": "direct_discussion", "generation_method": "dependent"}
]

for config in task_combinations:
    llm_count = config["llm_count"]
    persona_type = config["persona_type"]
    phases = config["phases"]
    generation_method = config["generation_method"]

    print(f"\nRunning: llm_count={llm_count}, persona_type={persona_type}, phases={phases}, generation_method={generation_method}")
    logging.info(f"Starting run with llm_count={llm_count}, persona_type={persona_type}, phases={phases}, generation_method={generation_method}")

    try:
        main(llm_count=llm_count, persona_type=persona_type, phases=phases, generation_method=generation_method)
    except Exception as e:
        logging.error(f"Error during run: {e}")

    time.sleep(2)

print("\nAll tasks completed.")
