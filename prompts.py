# prompts.py

# ========== AUT ========== #
AUT_MODE1_OVERALL = """
Task: You are collaborating with two other team members to come up with five unusual uses of a rope.
Your ideas will be evaluated on their creativity (i.e., they should be both novel and useful).
"""

AUT_MODE1_IDEA_GENERATION = """
- Please propose 5 unusual uses of a rope.
- Each idea should be within 20 words and should not include explanation.
- List each idea on a separate line.
"""

AUT_MODE1_IDEA_GENERATION_DEPENDENT = """
- Please propose 5 additional unusual uses of a rope that are different from the previous ideas.
- Each idea should be within 20 words and should not include explanation.
- List each idea on a separate line.
"""

AUT_MODE1_SELECTION_RATING = """
- Below is the list of all proposed ideas.
- Please rate **each and every idea** on its creativity (i.e., novelty and usefulness), using a scale from 1 to 10. 
- Avoid giving the same score to multiple ideas unless absolutely necessary. 
- Provide your scores in the format 'Idea X: Y'.
- Ensure that the scores span a wide range to reflect varying levels of creativity.
"""

AUT_MODE1_SELECTION_SELECTIONTOP = """
- Please review all the ideas listed below.
- Select 5 ideas that you find the most creative (i.e., novel and useful).
- List the idea numbers of your selections (each on a new line).
"""

AUT_MODE1_DISCUSSION_RATING_ALLATONCE = """
- You are reviewing the current list of top ideas. Each idea should be evaluated individually.
- Your team has a maximum of 20 rounds to finalize the list of ideas. You are currently on round {{total_resp}}.

- Actions you can take for each idea:
  - **Agree:** If the idea meets the task objective and does not require changes, reply "Agree: No changes needed."
  - **Modify:** If the idea is aligned with the task objective but needs improvement, propose modification. Use this format:
    "Modify: [idea after modification] - Reason: [specific reason for improvement]."
  - **Replace:** If the idea is not creative or not aligned with the task objective, replace it with one from the shared replacement pool of top ideas. Use this format:
    "Replace: [replacement idea] - Reason: [why the old idea is not creative or not aligned with the task objective and the replacement idea can be better]."

- **Guidelines for Reviewing the List**:
  1. Carefully evaluate each idea in the list based on the task objective.
  2. Do not summarize or output a final revised list. Focus only on evaluating individual ideas.
  3. Avoid unnecessary changes: While you can suggest improvement or replacement, keep in mind that there are **a maximum of 20 rounds** for your team. If you disapprove one idea, prioritise improving it over replacing it.
  4. Be concise: Each idea should be **within 20 words**.
  5. Focus on meaningful improvement or replacement that enhances alignment with the task objective.
"""


AUT_MODE1_DISCUSSION_SELECTIONTOP_ALLATONCE_FIRSTAGENT = """
- You are reviewing the current list of top ideas. Each idea should be evaluated individually.
- Your team has a maximum of 20 rounds to finalize the list of ideas. You are currently on round {{total_resp}}.

- Actions you can take for each idea:
  - **Agree:** If the idea meets the task objective and does not require changes, reply "Agree: No changes needed."
  - **Modify:** If the idea is aligned with the task objective but needs improvement, propose modification. Use this format:
    "Modify: [idea after modification] - Reason: [specific reason for improvement]."

- **Guidelines for Reviewing the List**:
  1. Carefully evaluate each idea in the list based on the task objective.
  2. Do not summarize or output a final revised list. Focus only on evaluating individual ideas.
  3. Avoid unnecessary changes: While you can suggest improvement or replacement, keep in mind that there are **a maximum of 20 rounds** for your team.
  4. Be concise: Each idea should be **within 20 words**.
  5. Focus on meaningful improvement that enhances alignment with the task objective.
"""

AUT_MODE1_DISCUSSION_SELECTIONTOP_ALLATONCE_OTHERAGENTS = """
- You are reviewing the current list of top ideas. Each idea should be evaluated individually.
- Your team has a maximum of 20 rounds to finalize the list of ideas. You are currently on round {{total_resp}}.

- Actions you can take for each idea:
  - **Agree:** If the idea meets the task objective and does not require changes, reply "Agree: No changes needed."
  - **Modify:** If the idea is aligned with the task objective but needs improvement, propose modification. Use this format:
    "Modify: [idea after modification] - Reason: [specific reason for improvement]."
  - **Replace:** If the idea is not creative or not aligned with the task objective, replace it with one from the replacement pool of top ideas selected by yourself. Use this format:
    "Replace: [replacement idea] - Reason: [specific reason for replacement]."
"""


AUT_MODE1_DISCUSSION_RATING_ONEBYONE = """
- Currently, you are discussing Idea #{{idea_index}}.
- This is discussion round {{current_round}} out of a total of {{max_rounds}} rounds for this idea.
- Please be mindful that your team has limited rounds to finalize this idea.

- Actions you can take for the current idea: 
  - **Agree**: If the current idea meets the task objective and does not require changes, reply "Agree: No changes needed."
  - **Modify**: If the idea is aligned with the task objective but needs improvement, propose modification. Use this format:
    "Modify: [idea after modification] - Reason: [specific reason for improvement]."
  - **Replace**: If the idea is not creative or not aligned with the task objective, replace it with one from the shared replacement pool of top ideas. Use this format:
    "Replace: [replacement idea] - Reason: [specific reason for replacement]."

- Additional Guidelines:
  1. Be concise: Each idea should be **within 20 words**.
  2. Avoid unnecessary changes: While you can suggest improvement or replacement, keep in mind that there are **a maximum of {{max_rounds}} rounds** for your team. If you disapprove one idea, prioritise improving it over replacing it.
  3. Focus on meaningful improvement or replacement that enhances alignment with the task objective.
"""

AUT_MODE1_DISCUSSION_SELECTIONTOP_ONEBYONE = """
- Currently, you are discussing Idea #{{idea_index}}.
- This is discussion round {{current_round}} out of a total of {{max_rounds}} rounds for this idea.
- Please be mindful that your team has limited rounds to finalize this idea.

- Actions you can take for the current idea: 
  - **Agree**: If the current idea meets the task objective and does not require changes, reply "Agree: No changes needed."
  - **Modify**: If the idea is aligned with the task objective but needs improvement, propose modification. Use this format:
    "Modify: [idea after modification] - Reason: [specific reason for improvement]."
  - **Replace**: If the idea is not creative or not aligned with the task objective, replace it with one from the replacement pool of top ideas selected by yourself. Use this format:
    "Replace: [replacement idea] - Reason: [specific reason for replacement]."

- Additional Guidelines:
  1. Be concise: Each idea should be **within 20 words**.
  2. Avoid unnecessary changes: While you can suggest improvement or replacement, keep in mind that there are **a maximum of {{max_rounds}} rounds** for your team. If you disapprove one idea, prioritise improving it over replacing it.
  3. Focus on meaningful improvement or replacement that enhances alignment with the task objective.
"""

# ========== Problem Solving ========== #
PS_OVERALL_Single = """
Task: Global warming, which refers to the ongoing increase in global average temperature, has an increasingly large impact on the environment. Please come up with one creative idea to slow global warming. 
Your answers will be evaluated on its creativity (i.e., it should be both novel and useful).
The idea should be around 80-100 words.
"""

PS_OVERALL = """
Task: Global warming, which refers to the ongoing increase in global average temperature, has an increasingly large impact on the environment. You are collaborating with two other team members to come up with one creative idea to slow global warming.
Your answers will be evaluated on its creativity (i.e., it should be both novel and useful).
"""

PS_GENERATION = """
Think like a 24-year-old White female with a graduate degree in business and management, who works as a management consultant in a consulting firm, with the following personality profile according to the Big Five model (all personality scales range from 1 to 5, where 1 indicates a low score and 5 indicates a high score): Openness to Experience 3.7, Conscientiousness 3.5, Extraversion 3.0, Agreeableness 3.8, and Neuroticism 2.7. 

- Please propose 3 possible ideas for the problem.
- Each idea should be around 80-100 words.
- List each idea on a separate line.
- For example:
  1. [Idea 1]
  2. [Idea 2]
  3. [Idea 3]
"""

PS_GENERATION_DEPENDENT = """
Think like a 24-year-old White female with a graduate degree in business and management, who works as a management consultant in a consulting firm, with the following personality profile according to the Big Five model (all personality scales range from 1 to 5, where 1 indicates a low score and 5 indicates a high score): Openness to Experience 3.7, Conscientiousness 3.5, Extraversion 3.0, Agreeableness 3.8, and Neuroticism 2.7. 

- Please propose 3 additional ideas for the problem that are different from the previous ideas.
- Each idea should be around 80-100 words.
- List each idea on a separate line.
- For example:
  1. [Idea 1]
  2. [Idea 2]
  3. [Idea 3]
"""

PS_SELECTION_RATING = """
Think like a 24-year-old White female with a graduate degree in business and management, who works as a management consultant in a consulting firm, with the following personality profile according to the Big Five model (all personality scales range from 1 to 5, where 1 indicates a low score and 5 indicates a high score): Openness to Experience 3.7, Conscientiousness 3.5, Extraversion 3.0, Agreeableness 3.8, and Neuroticism 2.7. 

- Below is the list of 9 proposed ideas.
- Please rate **each and every idea** on on its creativity (i.e., novelty and usefulness), using a scale from 1 to 10. 
- Avoid giving the same score to multiple ideas unless absolutely necessary. 
- Provide ONLY your scores in the exact format: 'Idea X: Y', without any additional explanation:
  - **X** is the idea number (e.g., 1, 2, 3...).
  - **Y** is the creativity score (1 to 10).
- For example:
  Idea 1: 8
  Idea 2: 7
  Idea 3: 9
- Ensure that the scores span a wide range to reflect varying levels of creativity.
"""
# - Below is the list of all proposed ideas.
#- You MUST provide your scores in the exact format: **'Idea X: Y'**, where:

PS_SELECTION_SELECTIONTOP = """
- Please review all the ideas listed below.
- Select 3 ideas that you find the most creative (i.e., novel and useful).
- List the idea numbers of your selections (each on a new line).
"""

PS_DISCUSSION_RATING = """
Think like a 24-year-old White female with a graduate degree in business and management, who works as a management consultant in a consulting firm, with the following personality profile according to the Big Five model (all personality scales range from 1 to 5, where 1 indicates a low score and 5 indicates a high score): Openness to Experience 3.7, Conscientiousness 3.5, Extraversion 3.0, Agreeableness 3.8, and Neuroticism 2.7. 

- You are reviewing the current top idea. 
- Your team has a maximum of 20 rounds to finalize the list of ideas. You are currently on round {{total_resp}}.

- Actions you can take for the idea:
  - **Agree:** If the current idea is extremely creative and you cannot come up with a more creative idea, reply "Agree: No changes needed."
  - **Modify:** If the idea is moderately creative and could use improvement, propose modification. Use this format:
    "Modify: [idea after modification] - Reason: [specific reason for improvement]."
  - **Replace:** If the idea is not creative or not aligned with the task objective, replace it with one from the shared replacement pool of top ideas. Use this format:
    "Replace: [replacement idea] - Reason: [specific reason for replacement]."

- Each idea should be around 80-100 words.
"""

PS_DISCUSSION_RATING_PRE = """
- You are reviewing the current top idea. 
- Your team has a maximum of 20 rounds to finalize the list of ideas. You are currently on round {{total_resp}}.

- Actions you can take for each idea:
  - **Agree:** If the idea meets the task objective and does not require changes, reply "Agree: No changes needed."
  - **Modify:** If the idea is aligned with the task objective but needs improvement, propose modification. Use this format:
    "Modify: [idea after modification] - Reason: [specific reason for improvement]."
  - **Replace:** If the idea is not creative or not aligned with the task objective, replace it with one from the shared replacement pool of top ideas. Use this format:
    "Replace: [replacement idea] - Reason: [specific reason for replacement]."
  
- Each idea should be around 80-100 words.
"""

PS_DISCUSSION_SELECTIONTOP = """
- You are reviewing the current list of top ideas.
- Your team has a maximum of 20 rounds to finalize the list of ideas. You are currently on round {{total_resp}}.

- Actions you can take for the idea:
  - **Agree:** If the idea meets the task objective and does not require changes, reply "Agree: No changes needed."
  - **Modify:** If the idea is aligned with the task objective and needs improvement to be better, propose modification. Use this format:
    "Modify: [idea after modification] - Reason: [specific reason for improvement]."
  - **Replace:** If the idea is not creative or not aligned with the task objective, replace it with one from the replacement pool of top ideas selected by yourself. Use this format:
    "Replace: [replacement idea] - Reason: [specific reason for replacement]."
"""

PS_DISCUSSION_SELECTIONTOP_PRE = """
- You are reviewing the current list of top ideas.
- Your team has a maximum of 20 rounds to finalize the list of ideas. You are currently on round {{total_resp}}.

- Actions you can take for each idea:
  - **Agree:** If the idea meets the task objective and does not require changes, reply "Agree: No changes needed."
  - **Modify:** If the idea is aligned with the task objective but needs improvement, propose modification. Use this format:
    "Modify: [idea after modification] - Reason: [specific reason for improvement]."
  - **Replace:** If the idea is not creative or not aligned with the task objective, replace it with one from the replacement pool of top ideas selected by yourself. Use this format:
    "Replace: [replacement idea] - Reason: [specific reason for replacement]."
"""

# ========== Direct Discussion ========== #

AUT_DIRECT_FIRST_ROUND_ALL_AT_ONCE = """
- You are initiating the discussion for a collaborative task. Please propose 5 unusual uses of a rope.
- Each idea should be within 20 words and should not include explanation.
- List each idea on a separate line.
"""

AUT_DIRECT_DISCUSSION_ALL_AT_ONCE = """
- You are reviewing the current list of ideas. 
- Your team has a maximum of 30 rounds to finalize the list of ideas. You are currently on round {{total_resp}}.

- Actions you can take for each idea:
  - **Agree:** If the idea meets the task objective and does not require changes, reply "Agree: No changes needed."
  - **Modify:** If the idea is aligned with the task objective but needs improvement, propose modification. Use this format:
    "Modify: [idea after modification] - Reason: [specific reason for improvement]."
  - **Replace:** If the idea is not creative or not aligned with the task objective, propose a new idea to replace the current one. Use this format:
    "Replace: [replacement idea] - Reason: [specific reason for replacement]."

- **Guidelines**:
  1. Carefully evaluate each idea in the list based on the task objective.
  2. Do not summarize or output a final revised list. Focus only on evaluating individual ideas. 
  3. Avoid unnecessary changes: While you can suggest improvement or replacement, keep in mind that there are **a maximum of 30 rounds** for your team. If you disapprove one idea, prioritise improving it over replacing it.
  4. Be concise: Each idea should be **within 20 words**.
  5. Focus on meaningful improvement or replacement that enhances alignment with the task objective.
"""

AUT_DIRECT_FIRST_ROUND_ONE_BY_ONE = """
- You are initiating the discussion for a collaborative task. Please propose an unusual uses of a rope.
- The idea should be within 20 words and should not include explanations.
"""

AUT_DIRECT_DISCUSSION_ONE_BY_ONE = """
- Currently, you are discussing Idea #{{idea_index}}.
- This is discussion round {{current_round}} out of a total of 15 rounds for this idea.
- Please be mindful that your team has limited rounds to finalize this idea.

- Actions you can take for the current idea: 
  - **Agree**: If the current idea meets the task objective and does not require changes, reply "Agree: No changes needed."
  - **Modify**: If the idea is aligned with the task objective but needs improvement, propose modification. Use this format:
    "Modify: [idea after modification] - Reason: [specific reason for improvement]."
  - **Replace**: If the idea is not creative or not aligned with the task objective, propose a new idea to replace the current one. Use this format:
    "Replace: [replacement idea] - Reason: [specific reason for replacement]."

- **Guidelines**:
  1. Be concise: Each idea should be **within 20 words**.
  2. Avoid unnecessary changes: While you can suggest improvement or replacement, keep in mind that there are **a maximum of 15 rounds** for your team. If you disapprove one idea, prioritise improving it over replacing it.
  3. Focus on meaningful improvement or replacement that enhances alignment with the task objective.
"""

PS_DIRECT_FIRST_ROUND_ALL_AT_ONCE = """
- You are initiating the discussion for a collaborative task. Please propose an idea for the problem.
- The idea should be around 80-100 words.
"""

PS_DIRECT_DISCUSSION_ALL_AT_ONCE_Pre = """
- You are reviewing the current idea. 
- Your team has a maximum of 30 rounds to finalize the list of ideas. You are currently on round {{total_resp}}.
- Please be mindful that your team has limited rounds to finalize the idea.

- Actions you can take for the idea:
  - **Agree:** If the idea meets the task objective and does not require changes, reply "Agree: No changes needed."
  - **Modify:** If the idea is aligned with the task objective but needs improvement, propose modification. Use this format:
    "Modify: [idea after modification] - Reason: [specific reason for improvement]."
  - **Replace:** If the idea is not creative or not aligned with the task objective, propose a new idea to replace the current one. Use this format:
    "Replace: [replacement idea] - Reason: [specific reason for replacement]."
"""

PS_DIRECT_DISCUSSION_ALL_AT_ONCE = """
- You are reviewing the current idea. 
- Your team has a maximum of 30 rounds to finalize the list of ideas. You are currently on round {{total_resp}}.
- Please be mindful that your team has limited rounds to finalize the idea.

- Actions you can take for the idea:
  - **Agree:** If the current idea is extremely creative and you cannot come up with a more creative idea, reply "Agree: No changes needed."
  - **Modify:** If the idea is moderately creative and could use improvement, propose modification. Use this format:
    "Modify: [idea after modification] - Reason: [specific reason for improvement]."
  - **Replace:** If the idea is not creative or not aligned with the task objective, propose a new idea to replace the current one. Use this format:
    "Replace: [replacement idea] - Reason: [specific reason for replacement]."
"""

PS_DIRECT_DISCUSSION_ALL_AT_ONCE_RESTRICTION_FIRST = """
- You are reviewing the current idea. 
- Your team has a maximum of 30 rounds to finalize the list of ideas. You are currently on round {{total_resp}}.
- Please be mindful that your team has limited rounds to finalize the idea.

- Actions you can take for the idea:
  - **Modify:** If the idea is moderately creative and could use improvement, propose modification. Use this format:
    "Modify: [idea after modification] - Reason: [specific reason for improvement]."
  - **Replace:** If the idea is not creative or not aligned with the task objective, propose a new idea to replace the current one. Use this format:
    "Replace: [replacement idea] - Reason: [specific reason for replacement]."
"""

PS_DIRECT_DISCUSSION_ALL_AT_ONCE_RESTRICTION_OTHER = """
- You are reviewing the current idea. 
- Your team has a maximum of 30 rounds to finalize the list of ideas. You are currently on round {{total_resp}}.
- Please be mindful that your team has limited rounds to finalize the idea.

- Actions you can take for the idea:
  - **Agree:** If the current idea is extremely creative and you cannot come up with a more creative idea, reply "Agree: No changes needed."
  - **Modify:** If the idea is moderately creative and could use improvement, propose modification. Use this format:
    "Modify: [idea after modification] - Reason: [specific reason for improvement]."
  - **Replace:** If the idea is not creative or not aligned with the task objective, propose a new idea to replace the current one. Use this format:
    "Replace: [replacement idea] - Reason: [specific reason for replacement]."
"""



# ========== Raising hands ========== #
INTENTION_PROMPT_IDEAS = """
- Looking at the current list of ideas, please indicate how strongly you feel like responding (1-7)
- Provide your score in the following format: Score:X (replace X with your score).
"""

INTENTION_PROMPT_IDEA = """
- Looking at the current idea, please indicate how strongly you feel like responding (1-7)
- Provide your score in the following format: Score:X (replace X with your score).
"""

# ========== Input into Dictionairy ========== #

TASK_REQUIREMENTS = {
    "AUT_Mode1_Overall": AUT_MODE1_OVERALL,
    "AUT_Mode1_IdeaGeneration": AUT_MODE1_IDEA_GENERATION,
    "AUT_Mode1_IdeaGeneration_Dependent": AUT_MODE1_IDEA_GENERATION_DEPENDENT,
    "AUT_Mode1_Selection_Rating": AUT_MODE1_SELECTION_RATING,
    "AUT_Mode1_Selection_SelectionTop": AUT_MODE1_SELECTION_SELECTIONTOP,
    "AUT_Mode1_Discussion_Rating_AllAtOnce": AUT_MODE1_DISCUSSION_RATING_ALLATONCE,
    "AUT_Mode1_Discussion_SelectionTop_AllAtOnce_FirstAgent": AUT_MODE1_DISCUSSION_SELECTIONTOP_ALLATONCE_FIRSTAGENT,
    "AUT_Mode1_Discussion_SelectionTop_AllAtOnce_OtherAgents": AUT_MODE1_DISCUSSION_SELECTIONTOP_ALLATONCE_OTHERAGENTS,
    "AUT_Mode1_Discussion_Rating_OneByOne": AUT_MODE1_DISCUSSION_RATING_ONEBYONE,
    "AUT_Mode1_Discussion_SelectionTop_OneByOne": AUT_MODE1_DISCUSSION_SELECTIONTOP_ONEBYONE,

    "PS_Overall_Single": PS_OVERALL_Single,
    "PS_Overall": PS_OVERALL,
    "PS_Generation": PS_GENERATION,
    "PS_Generation_Dependent": PS_GENERATION_DEPENDENT,
    "PS_Selection_Rating": PS_SELECTION_RATING,
    "PS_Selection_SelectionTop": PS_SELECTION_SELECTIONTOP,
    "PS_Discussion_SelectionTop": PS_DISCUSSION_SELECTIONTOP,
    "PS_Discussion_Rating": PS_DISCUSSION_RATING,

    "AUT_Direct_First_Round_AllAtOnce": AUT_DIRECT_FIRST_ROUND_ALL_AT_ONCE,
    "AUT_Direct_Dicussion_AllAtOnce": AUT_DIRECT_DISCUSSION_ALL_AT_ONCE,
    "AUT_Direct_First_Round_OneByOne":AUT_DIRECT_FIRST_ROUND_ONE_BY_ONE,
    "AUT_Direct_Discussion_OneByOne":AUT_DIRECT_DISCUSSION_ONE_BY_ONE,
    "PS_Direct_First_Round_AllAtOnce":PS_DIRECT_FIRST_ROUND_ALL_AT_ONCE,
    "PS_Direct_Discussion_AllAtOnce":PS_DIRECT_DISCUSSION_ALL_AT_ONCE,
    "PS_Direct_Discussion_AllAtOnce_First":PS_DIRECT_DISCUSSION_ALL_AT_ONCE_RESTRICTION_FIRST,
    "PS_Direct_Discussion_AllAtOnce_Other":PS_DIRECT_DISCUSSION_ALL_AT_ONCE_RESTRICTION_OTHER,

    "Intention_Prompt_Ideas": INTENTION_PROMPT_IDEAS,
    "Intention_Prompt_Idea": INTENTION_PROMPT_IDEA
}
