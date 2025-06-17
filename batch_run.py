import time
import logging
from main import main
import concurrent.futures

task_combinations = [
    # Condition 0: 1 agent, no persona, one idea
    {"llm_count": 1, "max_responses": 60, "model": "gpt-4.1", "persona_type": "none", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "none", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 1: 3 agents, no persona, interactive
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "none", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "none", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 2: 3 agents, same persona, interactive
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "same", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "none", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 3: 3 agents, different persona, interactive
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "none", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 4: 6 agents, no persona, interactive
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4.1", "persona_type": "none", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "none", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 5: 6 agents, same persona, interactive
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4.1", "persona_type": "same", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "none", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 6: 6 agents, different persona, interactive
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "none", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 7: 3 agents, different persona, nominal
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "independent", "discussion_method": "none", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 8: 6 agents, different persona, nominal
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "independent", "discussion_method": "none", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 9: 3 agents, no persona, open discussion, 30 responses, fixed order (DIRECT DISCUSSION)
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "none", "phases": "direct_discussion",
     "generation_method": "dependent", "discussion_method": "open", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 10: 3 agents, same persona, open discussion, 30 responses, fixed order (DIRECT DISCUSSION)
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "same", "phases": "direct_discussion",
     "generation_method": "dependent", "discussion_method": "open", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 11: 3 agents, different persona, open discussion, 30 responses, fixed order (DIRECT DISCUSSION)
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "direct_discussion",
     "generation_method": "dependent", "discussion_method": "open", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 12: 3 agents, different persona, open discussion, 30 responses, random order (DIRECT DISCUSSION)
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "direct_discussion",
     "generation_method": "dependent", "discussion_method": "open", "discussion_order_method": "random",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 13: 3 agents, no persona, open discussion, 60 responses, fixed order (DIRECT DISCUSSION)
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "none", "phases": "direct_discussion",
     "generation_method": "dependent", "discussion_method": "open", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 14: 3 agents, same persona, open discussion, 60 responses, fixed order (DIRECT DISCUSSION)
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "same", "phases": "direct_discussion",
     "generation_method": "dependent", "discussion_method": "open", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 15: 3 agents, different persona, open discussion, 60 responses, fixed order (DIRECT DISCUSSION)
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "direct_discussion",
     "generation_method": "dependent", "discussion_method": "open", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 16: 3 agents, different persona, open discussion, 60 responses, random order (DIRECT DISCUSSION)
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "direct_discussion",
     "generation_method": "dependent", "discussion_method": "open", "discussion_order_method": "random",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 17: 3 agents, no persona, one_by_one discussion, 30 responses, fixed order (DIRECT DISCUSSION)
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "none", "phases": "direct_discussion",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 18: 3 agents, same persona, one_by_one discussion, 30 responses, fixed order (DIRECT DISCUSSION)
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "same", "phases": "direct_discussion",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 19: 3 agents, different persona, one_by_one discussion, 30 responses, fixed order (DIRECT DISCUSSION)
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "direct_discussion",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 20: 3 agents, different persona, one_by_one discussion, 30 responses, hand_raising order (DIRECT DISCUSSION)
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "direct_discussion",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "hand_raising",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 21: 3 agents, different persona, one_by_one discussion, 30 responses, random order (DIRECT DISCUSSION)
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "direct_discussion",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "random",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 22: 3 agents, no persona, one_by_one discussion, 60 responses (minimum 30), fixed order (DIRECT DISCUSSION)
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "none", "phases": "direct_discussion",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "min_responses": 30, "question_id": "plastic_waste"},

    # Condition 23: 3 agents, same persona, one_by_one discussion, 60 responses (minimum 30), fixed order (DIRECT DISCUSSION)
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "same", "phases": "direct_discussion",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "min_responses": 30, "question_id": "plastic_waste"},

    # Condition 24: 3 agents, different persona, one_by_one discussion, 60 responses (minimum 30), fixed order (DIRECT DISCUSSION)
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "direct_discussion",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "min_responses": 30, "question_id": "plastic_waste"},

    # Condition 25: 3 agents, different persona, one_by_one discussion, 60 responses (minimum 30), hand_raising order (DIRECT DISCUSSION)
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "direct_discussion",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "hand_raising",
     "replacement_pool_size": 0, "min_responses": 30, "question_id": "plastic_waste"},

    # Condition 26: 3 agents, different persona, one_by_one discussion, 60 responses (minimum 30), random order (DIRECT DISCUSSION)
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "direct_discussion",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "random",
     "replacement_pool_size": 0, "min_responses": 30, "question_id": "plastic_waste"},

    # Condition 27: 3 agents, no persona, iterative_refinement discussion, 30 responses, fixed order (DIRECT DISCUSSION)
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "none", "phases": "direct_discussion",
     "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 28: 3 agents, same persona, iterative_refinement discussion, 30 responses, fixed order (DIRECT DISCUSSION)
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "same", "phases": "direct_discussion",
     "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 29: 3 agents, different persona, iterative_refinement discussion, 30 responses, fixed order (DIRECT DISCUSSION)
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "direct_discussion",
     "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 30: 3 agents, different persona, iterative_refinement discussion, 30 responses, random order (DIRECT DISCUSSION)
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "direct_discussion",
     "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "random",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 31: 3 agents, no persona, interactive + one_by_one discussion, 30 responses, fixed order
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "none", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 32: 3 agents, same persona, interactive + one_by_one discussion, 30 responses, fixed order
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "same", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 33: 3 agents, different persona, interactive + one_by_one discussion, 30 responses, fixed order
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 34: 3 agents, different persona, interactive + one_by_one discussion, 30 responses, hand_raising order
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "hand_raising",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 35: 3 agents, different persona, interactive + one_by_one discussion, 30 responses, random order
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "random",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 36: 3 agents, no persona, interactive + one_by_one discussion, 60 responses (minimum 30), fixed order
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "none", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "min_responses": 30, "question_id": "plastic_waste"},

    # Condition 37: 3 agents, same persona, interactive + one_by_one discussion, 60 responses (minimum 30), fixed order
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "same", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "min_responses": 30, "question_id": "plastic_waste"},

    # Condition 38: 3 agents, different persona, interactive + one_by_one discussion, 60 responses (minimum 30), fixed order
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "min_responses": 30, "question_id": "plastic_waste"},

    # Condition 39: 3 agents, different persona, interactive + one_by_one discussion, 60 responses (minimum 30), hand_raising order
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "hand_raising",
     "replacement_pool_size": 0, "min_responses": 30, "question_id": "plastic_waste"},

    # Condition 40: 3 agents, different persona, interactive + one_by_one discussion, 60 responses (minimum 30), random order
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "random",
     "replacement_pool_size": 0, "min_responses": 30, "question_id": "plastic_waste"},

    # Condition 41: 3 agents, no persona, interactive + one_by_one discussion with top5, 30 responses, fixed order
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "none", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "fixed",
     "replacement_pool_size": 5, "question_id": "plastic_waste"},

    # Condition 42: 3 agents, same persona, interactive + one_by_one discussion with top5, 30 responses, fixed order
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "same", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "fixed",
     "replacement_pool_size": 5, "question_id": "plastic_waste"},

    # Condition 43: 3 agents, different persona, interactive + one_by_one discussion with top5, 30 responses, fixed order
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "fixed",
     "replacement_pool_size": 5, "question_id": "plastic_waste"},

    # Condition 44: 3 agents, different persona, interactive + one_by_one discussion with top5, 30 responses, hand_raising order
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "hand_raising",
     "replacement_pool_size": 5, "question_id": "plastic_waste"},

    # Condition 45: 3 agents, different persona, interactive + one_by_one discussion with top5, 30 responses, random order
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "random",
     "replacement_pool_size": 5, "question_id": "plastic_waste"},

    # Condition 46: 6 agents, no persona, interactive + one_by_one discussion, 30 responses, fixed order
    {"llm_count": 6, "max_responses": 30, "model": "gpt-4.1", "persona_type": "none", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 47: 6 agents, same persona, interactive + one_by_one discussion, 30 responses, fixed order
    {"llm_count": 6, "max_responses": 30, "model": "gpt-4.1", "persona_type": "same", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 48: 6 agents, different persona, interactive + one_by_one discussion, 30 responses, fixed order
    {"llm_count": 6, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 49: 6 agents, different persona, interactive + one_by_one discussion, 30 responses, hand_raising order
    {"llm_count": 6, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "hand_raising",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 50: 6 agents, different persona, interactive + one_by_one discussion, 30 responses, random order
    {"llm_count": 6, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "random",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 51: 6 agents, no persona, interactive + one_by_one discussion, 60 responses (minimum 30), fixed order
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4.1", "persona_type": "none", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "min_responses": 30, "question_id": "plastic_waste"},

    # Condition 52: 6 agents, same persona, interactive + one_by_one discussion, 60 responses (minimum 30), fixed order
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4.1", "persona_type": "same", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "min_responses": 30, "question_id": "plastic_waste"},

    # Condition 53: 6 agents, different persona, interactive + one_by_one discussion, 60 responses (minimum 30), fixed order
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "min_responses": 30, "question_id": "plastic_waste"},

    # Condition 54: 6 agents, different persona, interactive + one_by_one discussion, 60 responses (minimum 30), hand_raising order
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "hand_raising",
     "replacement_pool_size": 0, "min_responses": 30, "question_id": "plastic_waste"},

    # Condition 55: 6 agents, different persona, interactive + one_by_one discussion, 60 responses (minimum 30), random order
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "one_by_one", "discussion_order_method": "random",
     "replacement_pool_size": 0, "min_responses": 30, "question_id": "plastic_waste"},

    # Condition 56: 3 agents, no persona, interactive + iterative_refinement discussion, 30 responses, fixed order
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "none", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 57: 3 agents, same persona, interactive + iterative_refinement discussion, 30 responses, fixed order
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "same", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 58: 3 agents, different persona, interactive + iterative_refinement discussion, 30 responses, fixed order
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 59: 3 agents, different persona, interactive + iterative_refinement discussion, 30 responses, random order
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "random",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 60: 6 agents, no persona, interactive + iterative_refinement discussion, 30 responses, fixed order
    {"llm_count": 6, "max_responses": 30, "model": "gpt-4.1", "persona_type": "none", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 61: 6 agents, same persona, interactive + iterative_refinement discussion, 30 responses, fixed order
    {"llm_count": 6, "max_responses": 30, "model": "gpt-4.1", "persona_type": "same", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 62: 6 agents, different persona, interactive + iterative_refinement discussion, 30 responses, fixed order
    {"llm_count": 6, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 63: 6 agents, different persona, interactive + iterative_refinement discussion, 30 responses, random order
    {"llm_count": 6, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "random",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 64: 3 agents, no persona, interactive + creative discussion, fixed order
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "none", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 65: 3 agents, same persona, interactive + creative discussion, fixed order
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "same", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 66: 3 agents, different persona, interactive + creative discussion, fixed order
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 67: 3 agents, different persona, interactive + creative discussion, random order
    {"llm_count": 3, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method": "random",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 68: 6 agents, no persona, interactive + creative discussion, fixed order
    {"llm_count": 6, "max_responses": 30, "model": "gpt-4.1", "persona_type": "none", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 69: 6 agents, same persona, interactive + creative discussion, fixed order
    {"llm_count": 6, "max_responses": 30, "model": "gpt-4.1", "persona_type": "same", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 70: 6 agents, different persona, interactive + creative discussion, fixed order
    {"llm_count": 6, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method": "fixed",
     "replacement_pool_size": 0, "question_id": "plastic_waste"},

    # Condition 71: 6 agents, different persona, interactive + creative discussion, random order
    {"llm_count": 6, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method": "random",
     "replacement_pool_size": 0, "question_id": "plastic_waste"}
]

# task_combinations = [
#     # Condition 0: 1 agent, no persona, one idea
#     {"llm_count": 6, "max_responses": 30, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
#      "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method": "random",
#      "replacement_pool_size": 0, "question_id": "plastic_waste"}]
def run_config(config):
    try:
        logging.info(f"Running config: {config}")
        main(**config)
    except Exception as e:
        logging.error(f"Error during run: {e}")



with concurrent.futures.ProcessPoolExecutor(max_workers=36) as executor:
    futures = [executor.submit(run_config, config) for config in task_combinations]
    for future in concurrent.futures.as_completed(futures):
        try:
            future.result()
        except Exception as exc:
            print(f"Task generated an exception: {exc}")

print("\nAll tasks completed.")

# for config in task_combinations:
#     llm_count = config["llm_count"]
#     persona_type = config["persona_type"]
#     phases = config["phases"]
#     generation_method = config["generation_method"]
#     print("running config", config)
#     print(f"\nRunning: llm_count={llm_count}, persona_type={persona_type}, phases={phases}, generation_method={generation_method}")
#     logging.info(f"Starting run with llm_count={llm_count}, persona_type={persona_type}, phases={phases}, generation_method={generation_method}")
#
#     try:
#         main(**config)  # This passes all parameters from the dictionary to the function
#     except Exception as e:
#         logging.error(f"Error during run: {e}")
#
#     time.sleep(2)

print("\nAll tasks completed.")
