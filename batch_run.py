import time
import logging
from main import main
import concurrent.futures


task_combinations = [
         {"llm_count": 3, "max_responses":60, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"hand_raising", "replacement_pool_size":0},
         {"llm_count": 3, "max_responses":60, "persona_type": "same", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"hand_raising", "replacement_pool_size":0},
]

task_combinations = [
         {"llm_count": 3, "model":"o3-mini","max_responses":60, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"hand_raising", "replacement_pool_size":0},
]

task_combinations = [
         {"llm_count": 3, "model":"gpt-4o","max_responses":60, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"hand_raising", "replacement_pool_size":0},
         {"llm_count": 3, "model":"gpt-4o","max_responses":60, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"hand_raising", "replacement_pool_size":0},
         {"llm_count": 3, "model":"gpt-4o","max_responses":60, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"hand_raising", "replacement_pool_size":0},

]


task_combinations = [
         {"llm_count": 3, "max_responses":30, "model":"gpt-4o", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"hand_raising", "replacement_pool_size":0},
]

task_combinations = [
         {"llm_count": 3, "max_responses":60, "model":"gpt-4o", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"fixed", "replacement_pool_size":5},
]

task_combinations = [
    #{"llm_count": 3, "persona_type": "same", "phases": "three_stage", "generation_method": "dependent"},
    #Open
    #{"llm_count": 3, "max_responses":60, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "open", "discussion_order_method":"fixed"},
    {"llm_count": 3, "max_responses":60, "model":"gpt-4.1", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "open", "discussion_order_method":"random"},

    #Instructed
    {"llm_count": 3,"max_responses":60, "model":"gpt-4.1", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"fixed", "replacement_pool_size":0},

    # #Instructed - replacement pool size top 5
    {"llm_count": 3, "max_responses":60, "model":"gpt-4.1", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"fixed", "replacement_pool_size":5},

    #Instructed - replcaement pool 0 - hand_raising
    {"llm_count": 3, "max_responses":60, "model":"gpt-4.1", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"hand_raising", "replacement_pool_size":0},
    {"llm_count": 3, "model":"o3-mini","max_responses": 60, "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "hand_raising",
     "replacement_pool_size": 0},

    {"llm_count": 3, "max_responses":60, "model":"gpt-4.1", "persona_type": "same", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"hand_raising", "replacement_pool_size":0},

    # # Iterative refinement
    {"llm_count": 3, "max_responses":60, "model":"gpt-4.1","persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method":"fixed", "replacement_pool_size":0},
    # # Additional Idea Generation (creative)
    {"llm_count": 3, "max_responses":60, "model":"gpt-4.1", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method":"fixed", "replacement_pool_size":0},

    #{"llm_count": 3, "model":"o3-mini", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method":"fixed", "replacement_pool_size":0},


    #{"llm_count": 6, "persona_type": "same", "phases": "three_stage", "generation_method": "independent"},
    #Open
    #{"llm_count": 6, "max_responses":60, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "open", "discussion_order_method":"fixed"},
    #Instructed
    {"llm_count": 6, "max_responses":60, "model":"gpt-4.1", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"fixed", "replacement_pool_size":5},
    #{"llm_count": 6, "max_responses":60, "persona_type": "same", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"fixed", "replacement_pool_size":0},

    # #Instructed - replacement pool size top 5
    {"llm_count": 6, "max_responses":60, "model":"gpt-4.1", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"fixed", "replacement_pool_size":5},

    #Instructed - replcaement pool 0 - hand_raising
    {"llm_count": 6, "max_responses":60,"model":"gpt-4.1",  "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"hand_raising", "replacement_pool_size":0},
    # # Iterative refinement
    #{"llm_count": 6,"max_responses":60, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method":"fixed", "replacement_pool_size":0},
    # # Additional Idea Generation (creative)
    #{"llm_count": 6,"max_responses":60, "model":"gpt-4o", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method":"fixed", "replacement_pool_size":0},

]


task_combinations = [
    #{"llm_count": 3, "persona_type": "same", "phases": "three_stage", "generation_method": "dependent"},
    #Open
    #{"llm_count": 3, "max_responses":60, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "open", "discussion_order_method":"fixed"},
    {"llm_count": 3, "max_responses":60, "model":"gpt-4o", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "open", "discussion_order_method":"random"},

    #Instructed
    {"llm_count": 3,"max_responses":60, "model":"gpt-4o", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"fixed", "replacement_pool_size":0},

    # #Instructed - replacement pool size top 5
    {"llm_count": 3, "max_responses":60, "model":"gpt-4o", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"fixed", "replacement_pool_size":5},

    #Instructed - replcaement pool 0 - hand_raising
    {"llm_count": 3, "max_responses":60, "model":"gpt-4o", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"hand_raising", "replacement_pool_size":0},
    {"llm_count": 3, "model":"o3-mini","max_responses": 60, "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "hand_raising",
     "replacement_pool_size": 0},

    {"llm_count": 3, "max_responses":60, "model":"gpt-4o", "persona_type": "same", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"hand_raising", "replacement_pool_size":0},

    # # Iterative refinement
    {"llm_count": 3, "max_responses":60, "model":"gpt-4o","persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method":"fixed", "replacement_pool_size":0},
    # # Additional Idea Generation (creative)
    {"llm_count": 3, "max_responses":60, "model":"gpt-4o", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method":"fixed", "replacement_pool_size":0},

    #{"llm_count": 3, "model":"o3-mini", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method":"fixed", "replacement_pool_size":0},


    #{"llm_count": 6, "persona_type": "same", "phases": "three_stage", "generation_method": "independent"},
    #Open
    #{"llm_count": 6, "max_responses":60, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "open", "discussion_order_method":"fixed"},
    #Instructed
    {"llm_count": 6, "max_responses":60, "model":"gpt-4o", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"fixed", "replacement_pool_size":0},
    #{"llm_count": 6, "max_responses":60, "persona_type": "same", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"fixed", "replacement_pool_size":0},

    # #Instructed - replacement pool size top 5
    {"llm_count": 6, "max_responses":60, "model":"gpt-4o", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"fixed", "replacement_pool_size":5},

    #Instructed - replcaement pool 0 - hand_raising
    {"llm_count": 6, "max_responses":60,"model":"gpt-4o",  "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"hand_raising", "replacement_pool_size":0},
    # # Iterative refinement
    #{"llm_count": 6,"max_responses":60, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method":"fixed", "replacement_pool_size":0},
    # # Additional Idea Generation (creative)
    #{"llm_count": 6,"max_responses":60, "model":"gpt-4o", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method":"fixed", "replacement_pool_size":0},
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4o", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "fixed",
     "replacement_pool_size": 0},
    # # Additional Idea Generation (creative)
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4o", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method": "fixed",
     "replacement_pool_size": 0},




    #Below is GPT4.1

    # {"llm_count": 3, "persona_type": "same", "phases": "three_stage", "generation_method": "dependent"},
    # Open
    # {"llm_count": 3, "max_responses":60, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "open", "discussion_order_method":"fixed"},
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "open", "discussion_order_method": "random"},

    # Instructed
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
     "replacement_pool_size": 0},

    # #Instructed - replacement pool size top 5
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
     "replacement_pool_size": 5},

    # Instructed - replcaement pool 0 - hand_raising
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "hand_raising",
     "replacement_pool_size": 0},
    {"llm_count": 3, "model": "o3-mini", "max_responses": 60, "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "hand_raising",
     "replacement_pool_size": 0},

    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "same", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "hand_raising",
     "replacement_pool_size": 0},

    # # Iterative refinement
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "fixed",
     "replacement_pool_size": 0},
    # # Additional Idea Generation (creative)
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method": "fixed",
     "replacement_pool_size": 0},

    # {"llm_count": 3, "model":"o3-mini", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method":"fixed", "replacement_pool_size":0},

    # {"llm_count": 6, "persona_type": "same", "phases": "three_stage", "generation_method": "independent"},
    # Open
    # {"llm_count": 6, "max_responses":60, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "open", "discussion_order_method":"fixed"},
    # Instructed
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
     "replacement_pool_size": 0},
    # {"llm_count": 6, "max_responses":60, "persona_type": "same", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"fixed", "replacement_pool_size":0},

    # #Instructed - replacement pool size top 5
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
     "replacement_pool_size": 5},

    # Instructed - replcaement pool 0 - hand_raising
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "hand_raising",
     "replacement_pool_size": 0},
    # # Iterative refinement
    # {"llm_count": 6,"max_responses":60, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method":"fixed", "replacement_pool_size":0},
    # # Additional Idea Generation (creative)
    # {"llm_count": 6,"max_responses":60, "model":"gpt-4.1", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method":"fixed", "replacement_pool_size":0},
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "fixed",
     "replacement_pool_size": 0},
    # # Additional Idea Generation (creative)
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method": "fixed",
     "replacement_pool_size": 0},

]

task_combinations = [
    {"llm_count": 3, "max_responses":60, "model":"gpt-4o","persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method":"fixed", "replacement_pool_size":5},
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "fixed",
     "replacement_pool_size": 0}

    # {"llm_count": 3, "max_responses":60, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "open", "discussion_order_method":"random"},

]

task_combinations = [
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4o", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
     "replacement_pool_size": 5},

]


task_combinations = [
    #{"llm_count": 3, "persona_type": "same", "phases": "three_stage", "generation_method": "dependent"},
    #Open
    #{"llm_count": 3, "max_responses":60, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "open", "discussion_order_method":"fixed"},
    {"llm_count": 3, "max_responses":60, "model":"gpt-4o", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "open", "discussion_order_method":"random"},

    #Instructed
    {"llm_count": 3,"max_responses":60, "model":"gpt-4o", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"fixed", "replacement_pool_size":0},

    # #Instructed - replacement pool size top 5
    {"llm_count": 3, "max_responses":60, "model":"gpt-4o", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"fixed", "replacement_pool_size":5},

    #Instructed - replcaement pool 0 - hand_raising
    {"llm_count": 3, "max_responses":60, "model":"gpt-4o", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"hand_raising", "replacement_pool_size":0},
    {"llm_count": 3, "model":"o3-mini","max_responses": 60, "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "hand_raising",
     "replacement_pool_size": 0},

    {"llm_count": 3, "max_responses":60, "model":"gpt-4o", "persona_type": "same", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"hand_raising", "replacement_pool_size":0},

    # # Iterative refinement
    {"llm_count": 3, "max_responses":60, "model":"gpt-4o","persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method":"fixed", "replacement_pool_size":0},
    # # Additional Idea Generation (creative)
    {"llm_count": 3, "max_responses":60, "model":"gpt-4o", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method":"fixed", "replacement_pool_size":0},

    #{"llm_count": 3, "model":"o3-mini", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method":"fixed", "replacement_pool_size":0},


    #{"llm_count": 6, "persona_type": "same", "phases": "three_stage", "generation_method": "independent"},
    #Open
    #{"llm_count": 6, "max_responses":60, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "open", "discussion_order_method":"fixed"},
    #Instructed
    {"llm_count": 6, "max_responses":60, "model":"gpt-4o", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"fixed", "replacement_pool_size":0},
    #{"llm_count": 6, "max_responses":60, "persona_type": "same", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"fixed", "replacement_pool_size":0},

    # #Instructed - replacement pool size top 5
    {"llm_count": 6, "max_responses":60, "model":"gpt-4o", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"fixed", "replacement_pool_size":5},

    #Instructed - replcaement pool 0 - hand_raising
    {"llm_count": 6, "max_responses":60,"model":"gpt-4o",  "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"hand_raising", "replacement_pool_size":0},
    # # Iterative refinement
    #{"llm_count": 6,"max_responses":60, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method":"fixed", "replacement_pool_size":0},
    # # Additional Idea Generation (creative)
    #{"llm_count": 6,"max_responses":60, "model":"gpt-4o", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method":"fixed", "replacement_pool_size":0},
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4o", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "fixed",
     "replacement_pool_size": 0},
    # # Additional Idea Generation (creative)
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4o", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method": "fixed",
     "replacement_pool_size": 0},
]


task_combinations = [
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4o", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "hand_raising",
     "replacement_pool_size": 5},
]


task_combinations = [
    #{"llm_count": 3, "persona_type": "same", "phases": "three_stage", "generation_method": "dependent"},
    #Open
    #{"llm_count": 3, "max_responses":60, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "open", "discussion_order_method":"fixed"},
    {"llm_count": 6, "max_responses":60, "model":"gpt-4.1", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "open", "discussion_order_method":"random"},

    #Instructed
    {"llm_count": 6,"max_responses":60, "model":"gpt-4.1", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"fixed", "replacement_pool_size":0},

    # #Instructed - replacement pool size top 5
    {"llm_count": 6,"max_responses":60, "model":"gpt-4.1", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"fixed", "replacement_pool_size":5},
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4.1", "persona_type": "none", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
     "replacement_pool_size": 5},

    #Instructed - replcaement pool 0 - hand_raising
    {"llm_count": 3, "max_responses":60, "model":"gpt-4.1", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"hand_raising", "replacement_pool_size":0},

    # # Iterative refinement
    {"llm_count": 3, "max_responses":60, "model":"gpt-4.1","persona_type": "same", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method":"random", "replacement_pool_size":0},
    # # Additional Idea Generation (creative)
    {"llm_count": 3, "max_responses":60, "model":"gpt-4.1", "persona_type": "none", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method":"random", "replacement_pool_size":0},
    {"llm_count": 6, "max_responses": 60, "model": "o4-mini", "persona_type": "none", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method": "random",
     "replacement_pool_size": 0},
]

task_combinations = [
    #{"llm_count": 3, "persona_type": "same", "phases": "three_stage", "generation_method": "dependent"},
    #Open
    #{"llm_count": 3, "max_responses":60, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "open", "discussion_order_method":"fixed"},
    {"llm_count": 6, "max_responses":60, "model":"o3-mini", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "open", "discussion_order_method":"random"},

    #Instructed
    {"llm_count": 6,"max_responses":60, "model":"o3-mini", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"fixed", "replacement_pool_size":0},

    # #Instructed - replacement pool size top 5
    {"llm_count": 6,"max_responses":60, "model":"o3-mini", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"fixed", "replacement_pool_size":5},
    {"llm_count": 6, "max_responses": 60, "model": "o3-mini", "persona_type": "none", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
     "replacement_pool_size": 5},

    #Instructed - replcaement pool 0 - hand_raising
    {"llm_count": 3, "max_responses":60, "model":"o3-mini", "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method":"hand_raising", "replacement_pool_size":0},

    # # Iterative refinement
    {"llm_count": 3, "max_responses":60, "model":"o3-mini","persona_type": "same", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method":"random", "replacement_pool_size":0},
    # # Additional Idea Generation (creative)
    {"llm_count": 3, "max_responses":60, "model":"o3-mini", "persona_type": "none", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method":"random", "replacement_pool_size":0},
    # {"llm_count": 3, "max_responses":60, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "open", "discussion_order_method":"fixed"},
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4o", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "open", "discussion_order_method": "random"},

    # Instructed
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4o", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
     "replacement_pool_size": 0},

    # #Instructed - replacement pool size top 5
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4o", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
     "replacement_pool_size": 5},
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4o", "persona_type": "none", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
     "replacement_pool_size": 5},

    # Instructed - replcaement pool 0 - hand_raising
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4o", "persona_type": "different", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "hand_raising",
     "replacement_pool_size": 0},

    # # Iterative refinement
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4o", "persona_type": "same", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "random",
     "replacement_pool_size": 0},
    # # Additional Idea Generation (creative)
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4o", "persona_type": "none", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method": "random",
     "replacement_pool_size": 0}]
# task_combinations = [
#     #{"llm_count": 3, "max_responses":60, "model":"gpt-4o","persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method":"fixed", "replacement_pool_size":0},
#      {"llm_count": 3, "max_responses":60, "persona_type": "different", "phases": "three_stage", "generation_method": "dependent", "discussion_method": "open", "discussion_order_method":"random"},
#
# ]
task_combinations = [
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4o", "persona_type": "none", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
     "replacement_pool_size": 5},
]
task_combinations = [
    {"llm_count": 6, "max_responses": 60, "model": "o3-mini", "persona_type": "same", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
     "replacement_pool_size": 5},
    {"llm_count": 6, "max_responses": 60, "model": "gpt-4.1", "persona_type": "same", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
     "replacement_pool_size": 5},
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "none", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
     "replacement_pool_size": 5},
    {"llm_count": 3, "max_responses": 60, "model": "o3-mini", "persona_type": "none", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
     "replacement_pool_size": 5},
    {"llm_count": 3, "max_responses": 60, "model": "gpt-4o", "persona_type": "same", "phases": "three_stage",
     "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
     "replacement_pool_size": 5},
]
task_combinations = [
{"llm_count": 6, "max_responses": 60, "model": "gpt-4.1", "persona_type": "same", "phases": "three_stage",
 "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
 "replacement_pool_size": 5},
{"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "none", "phases": "three_stage",
 "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
 "replacement_pool_size": 5}]


task_combinations = [
# {"llm_count": 6, "max_responses": 60, "model": "gpt-4.1", "persona_type": "same", "phases": "direct_discussion",
#  "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
#  "replacement_pool_size": 0},
{"llm_count": 6, "max_responses": 60, "model": "gpt-4.1", "persona_type": "none", "phases": "direct_discussion",
 "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "fixed",
 "replacement_pool_size": 5}]

task_combinations = [
{"llm_count": 6, "max_responses": 60, "model": "gpt-4o", "persona_type": "none", "phases": "three_stage",
 "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "fixed",
 "replacement_pool_size": 0},
{"llm_count": 6, "max_responses": 60, "model": "gpt-4o", "persona_type": "none", "phases": "direct_discussion",
 "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "fixed",
 "replacement_pool_size": 0}]
task_combinations = [
{"llm_count": 3, "max_responses": 60, "model": "gpt-4o", "persona_type": "none", "phases": "three_stage",
 "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "fixed",
 "replacement_pool_size": 0},
{"llm_count": 3, "max_responses": 60, "model": "gpt-4o", "persona_type": "none", "phases": "direct_discussion",
 "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "fixed",
 "replacement_pool_size": 0}]

task_combinations = [{"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "none", "phases": "direct_discussion",
 "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "fixed",
 "replacement_pool_size": 0},
{"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different",
                      "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once",
                      "discussion_order_method": "fixed", "replacement_pool_size": 0, "min_responses":30}]
task_combinations = [
{"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different",
                      "phases": "direct_discussion", "generation_method": "dependent", "discussion_method": "all_at_once",
                      "discussion_order_method": "fixed", "replacement_pool_size": 0, "min_responses":30}]

task_combinations = [
{"llm_count": 3, "max_responses": 60, "model": "o4-mini", "persona_type": "none", "phases": "three_stage",
 "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "fixed",
 "replacement_pool_size": 0},
    {"llm_count": 3, "max_responses": 60, "model": "o4-mini", "persona_type": "different",
                      "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once",
                      "discussion_order_method": "fixed", "replacement_pool_size": 0},
{"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "different",
                      "phases": "three_stage", "generation_method": "dependent", "discussion_method": "all_at_once",
                      "discussion_order_method": "hand_raising", "replacement_pool_size": 0, "min_responses":30},
{"llm_count": 3, "max_responses": 60, "model": "o4-mini", "persona_type": "different",
                      "phases": "three_stage", "generation_method": "dependent",
                      "discussion_method": "all_at_once",
                      "discussion_order_method": "hand_raising", "replacement_pool_size": 0, "min_responses": 30}
                     ]

task_combinations = [
{"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "none", "phases": "three_stage",
 "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "fixed",
 "replacement_pool_size": 0}
                     ]



task_combinations = [
{"llm_count": 3, "max_responses": 60, "model": "o4-mini-high", "persona_type": "none", "phases": "three_stage",
 "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
 "replacement_pool_size": 0},
                     ]


task_combinations = [
{"llm_count": 3, "max_responses": 60, "model": "gpt-4.1", "persona_type": "none", "phases": "three_stage",
 "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
 "replacement_pool_size": 0},
                     ]

task_combinations = [
{"llm_count": 3, "max_responses": 60, "model":"deepseek-ai/DeepSeek-R1", "persona_type": "none", "phases": "three_stage",
 "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
 "replacement_pool_size": 0},
                     ]
task_combinations = [
{"llm_count": 3, "max_responses": 60, "model":["gemini-2.5-pro-preview-05-06",'deepseek-ai/DeepSeek-R1', 'o4-mini-high'], "persona_type": "none", "phases": "three_stage",
 "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
 "replacement_pool_size": 0},
                     ]
task_combinations = [
{"llm_count": 3, "max_responses": 60, "model":"gpt-4o", "persona_type": "none", "phases": "three_stage",
 "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
 "replacement_pool_size": 0},
                     ]

task_combinations = [
{"llm_count": 3, "max_responses": 60, "model":["gemini-2.5-pro-preview-05-06",'deepseek-ai/DeepSeek-R1', 'o4-mini-high'], "persona_type": "none", "phases": "three_stage",
 "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
 "replacement_pool_size": 0},{"llm_count": 3, "max_responses": 60, "model":["gemini-2.5-pro-preview-05-06",'deepseek-ai/DeepSeek-R1', 'o4-mini-high'], "persona_type": "none", "phases": "three_stage",
 "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "hand_raising",
 "replacement_pool_size": 0}
                     ]
task_combinations = [
{"llm_count": 3, "max_responses": 60, "model":"deepseek-ai/DeepSeek-R1", "persona_type": "none", "phases": "three_stage",
 "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "fixed",
 "replacement_pool_size": 0},
                     ]


task_combinations = [
{"llm_count": 3, "max_responses": 60, "model":["gemini-2.5-pro-preview-05-06",'deepseek-ai/DeepSeek-R1', 'o4-mini-high'], "persona_type": "none", "phases": "three_stage",
 "generation_method": "dependent", "discussion_method": "open", "discussion_order_method": "random",
 "replacement_pool_size": 0},

{"llm_count": 3, "max_responses": 60, "model":["gemini-2.5-pro-preview-05-06",'deepseek-ai/DeepSeek-R1', 'o4-mini-high'], "persona_type": "none", "phases": "three_stage",
 "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "random",
 "replacement_pool_size": 0},

{"llm_count": 3, "max_responses": 60, "model":["gemini-2.5-pro-preview-05-06",'deepseek-ai/DeepSeek-R1', 'o4-mini-high'], "persona_type": "none", "phases": "three_stage",
 "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "hand_raising",
 "replacement_pool_size": 0},

{"llm_count": 3, "max_responses": 60, "model":["gemini-2.5-pro-preview-05-06",'deepseek-ai/DeepSeek-R1', 'o4-mini-high'], "persona_type": "none", "phases": "three_stage",
 "generation_method": "dependent", "discussion_method": "iterative_refinement", "discussion_order_method": "random",
 "replacement_pool_size": 0},

{"llm_count": 3, "max_responses": 60, "model":["gemini-2.5-pro-preview-05-06",'deepseek-ai/DeepSeek-R1', 'o4-mini-high'], "persona_type": "none", "phases": "three_stage",
 "generation_method": "dependent", "discussion_method": "creative", "discussion_order_method": "random",
 "replacement_pool_size": 0}]


task_combinations = [
{"llm_count": 3, "max_responses": 60, "model":["gemini-2.5-pro-preview-05-06",'deepseek-ai/DeepSeek-R1', 'o3'], "persona_type": "none", "phases": "three_stage",
 "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "random",
 "replacement_pool_size": 0},

{"llm_count": 3, "max_responses": 60, "model":["gemini-2.5-pro-preview-05-06",'deepseek-ai/DeepSeek-R1', 'o3'], "persona_type": "none", "phases": "three_stage",
 "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "hand_raising",
 "replacement_pool_size": 0}]

task_combinations = [
{"llm_count": 3, "max_responses": 60, "model":["gemini-2.5-pro-preview-05-06",'deepseek-ai/DeepSeek-R1', 'o3'], "persona_type": "none", "phases": "three_stage",
 "generation_method": "dependent", "discussion_method": "all_at_once", "discussion_order_method": "random",
 "replacement_pool_size": 0}]

def run_config(config):
    try:
        logging.info(f"Running config: {config}")
        main(**config)
    except Exception as e:
        logging.error(f"Error during run: {e}")



with concurrent.futures.ProcessPoolExecutor() as executor:
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
