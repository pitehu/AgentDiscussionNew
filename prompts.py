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
    "Modify: [full idea after modification] - Reason: [specific reason for improvement]."
  - **Replace:** If the idea is not creative or not aligned with the task objective, replace it with one from the shared replacement pool of top ideas. Use this format:
    "Replace: [full replacement idea] - Reason: [why the old idea is not creative or not aligned with the task objective and the full replacement idea can be better]."

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
    "Modify: [full idea after modification] - Reason: [specific reason for improvement]."

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
    "Modify: [full idea after modification] - Reason: [specific reason for improvement]."
  - **Replace:** If the idea is not creative or not aligned with the task objective, replace it with one from the replacement pool of top ideas selected by yourself. Use this format:
    "Replace: [full replacement idea] - Reason: [specific reason for replacement]."
"""


AUT_MODE1_DISCUSSION_RATING_ONEBYONE = """
- Currently, you are discussing Idea #{{idea_index}}.
- This is discussion round {{current_round}} out of a total of {{max_rounds}} rounds for this idea.
- Please be mindful that your team has limited rounds to finalize this idea.

- Actions you can take for the current idea: 
  - **Agree**: If the current idea meets the task objective and does not require changes, reply "Agree: No changes needed."
  - **Modify**: If the idea is aligned with the task objective but needs improvement, propose modification. Use this format:
    "Modify: [full idea after modification] - Reason: [specific reason for improvement]."
  - **Replace**: If the idea is not creative or not aligned with the task objective, replace it with one from the shared replacement pool of top ideas. Use this format:
    "Replace: [full replacement idea] - Reason: [specific reason for replacement]."

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
    "Modify: [full idea after modification] - Reason: [specific reason for improvement]."
  - **Replace**: If the idea is not creative or not aligned with the task objective, replace it with one from the replacement pool of top ideas selected by yourself. Use this format:
    "Replace: [full replacement idea] - Reason: [specific reason for replacement]."

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
- Please propose 5 possible ideas for the problem.
- Each idea should be around 80-100 words.
- List each idea on a separate line.
- For example:
  1. [Idea 1]
  2. [Idea 2]
  3. [Idea 3]
  4. [Idea 4]
  5. [Idea 5]
"""

PS_GENERATION_DEPENDENT = """
- Please propose 5 additional ideas for the problem that are different from the previous ideas.
- Each idea should be around 80-100 words.
- List each idea on a separate line.
- For example:
  1. [Idea 1]
  2. [Idea 2]
  3. [Idea 3]
  4. [Idea 4]
  5. [Idea 5]
"""

PS_SELECTION_RATING = """
- Below is the list of proposed ideas.
- Please rate **each and every idea** on its **creativity**, using a scale from 1 (Very Low Creativity) to 10 (Exceptional Creativity). 
- We define creativity as a combination of novelty (how original or unexpected the idea is in this context) and usefulness (its potential practical value or impact in addressing the goal). Consider both aspects when assigning your score
**Critically evaluate and differentiate** between the ideas. Assign unique scores wherever possible. Only assign the same score if two ideas are genuinely indistinguishable in their level of creativity based on the definition above.
Ensure your final scores span a wide range across the 1-10 scale (e.g., the difference between the highest and lowest score should be at least 6 points, if the ideas' quality allows for such differentiation). Do not cluster scores narrowly.
Provide **ONLY** your scores. **Strictly adhere** to the format 'Idea X: Y', with each score on a new line. Do **not** include any explanations, justifications, summaries, or any other text before or after the list of scores.
"""
# - Below is the list of all proposed ideas.
#- You MUST provide your scores in the exact format: **'Idea X: Y'**, where:

PS_SELECTION_RATING_NOVELTY = """
- Below is the list of proposed ideas.
- Please rate **each and every idea** on its **novelty**, using a scale from 1 (Very Low Novelty) to 10 (Exceptional Novelty). 
**Critically evaluate and differentiate** between the ideas. Assign unique scores wherever possible. Only assign the same score if two ideas are genuinely indistinguishable in their level of novelty.
Ensure your final scores span a wide range across the 1-10 scale (e.g., the difference between the highest and lowest score should be at least 6 points, if the ideas' quality allows for such differentiation). Do not cluster scores narrowly.
Provide **ONLY** your scores. **Strictly adhere** to the format 'Idea X: Y', with each score on a new line. Do **not** include any explanations, justifications, summaries, or any other text before or after the list of scores.
"""
PS_SELECTION_SELECTIONTOP = """
- Please review all the ideas listed below.
- Select 3 ideas that you find the most creative (i.e., novel and useful).
- List the idea numbers of your selections (each on a new line).
"""

PS_DISCUSSION_RATING = """
- You are reviewing the current top idea. 
- Your team has a maximum of {{max_rounds}} rounds to finalize the list of ideas. You are currently on round {{total_resp}}.
- The goal is to identify or create the SINGLE MOST CREATIVE idea, not to continually expand one idea.

- Actions you can take for the idea:
  - **Agree:** If the current idea is extremely creative and you cannot come up with a more creative idea, reply "Agree: No changes needed."
  - **Modify:** If the idea has a strong creative core but could be significantly elevated. Your modification should aim for a leap in originality or impact, not just a minor tweak. Use this format:
    "Modify: [full idea after modification] - Reason: [specific reason for improvement]."
  - **Replace:** If the idea is not creative or not aligned with the task objective, replace it with one from the shared replacement pool of top ideas. Use this format:
    "Replace: [full replacement idea] - Reason: [specific reason for replacement]."
- The idea should be around 80-100 words.
"""

PS_DISCUSSION_RATING_PRE = """
- You are reviewing the current top idea. 
- Your team has a maximum of {{max_rounds}} rounds to finalize the list of ideas. You are currently on round {{total_resp}}.
- The goal is to identify or create the SINGLE MOST CREATIVE idea, not to continually expand one idea.

- Actions you can take for each idea:
  - **Agree:** If the idea meets the task objective and does not require changes, reply "Agree: No changes needed."
  - **Modify:** If the idea has a strong creative core but could be significantly elevated. Your modification should aim for a leap in originality or impact, not just a minor tweak. Use this format:
    "Modify: [full idea after modification] - Reason: [specific reason for improvement]."
  - **Replace:** If the idea is not creative or not aligned with the task objective, replace it with one from the shared replacement pool of top ideas. Use this format:
    "Replace: [full replacement idea] - Reason: [specific reason for replacement]."
- The idea should be around 80-100 words.
"""

PS_DISCUSSION_SELECTIONTOP = """
- You are reviewing the current list of top ideas.
- Your team has a maximum of {{max_rounds}} rounds to finalize the list of ideas. You are currently on round {{total_resp}}.
- The goal is to identify or create the SINGLE MOST CREATIVE idea, not to continually expand one idea.

- Actions you can take for the idea:
  - **Agree:** If the idea meets the task objective and does not require changes, reply "Agree: No changes needed."
  - **Modify:** If the idea has a strong creative core but could be significantly elevated. Your modification should aim for a leap in originality or impact, not just a minor tweak. Use this format:
    "Modify: [full idea after modification] - Reason: [specific reason for improvement]."
  - **Replace:** If the idea is not creative or not aligned with the task objective, replace it with one from the replacement pool of top ideas selected by yourself. Use this format:
    "Replace: [full replacement idea] - Reason: [specific reason for replacement]."
- Each idea should be around 80-100 words.
"""

 
PS_DISCUSSION_SELECTIONTOP_PRE = """
- You are reviewing the current list of top ideas.
- Your team has a maximum of {{max_rounds}} rounds to finalize the list of ideas. You are currently on round {{total_resp}}.
- The goal is to identify or create the SINGLE MOST CREATIVE idea, not to continually expand one idea.

- Actions you can take for each idea:
  - **Agree:** If the idea meets the task objective and does not require changes, reply "Agree: No changes needed."
  - **Modify:** If the idea has a strong creative core but could be significantly elevated. Your modification should aim for a leap in originality or impact, not just a minor tweak. Use this format:
    "Modify: [full idea after modification] - Reason: [specific reason for improvement]."
  - **Replace:** If the idea is not creative or not aligned with the task objective, replace it with one from the replacement pool of top ideas selected by yourself. Use this format:
    "Replace: [full replacement idea] - Reason: [specific reason for replacement]."
- Each idea should be around 80-100 words.
"""

PS_DISCUSSION_RATING_NoPool = """
- You are reviewing the current top idea.
- Your team has a maximum of {{max_rounds}} rounds to finalize the idea. You are on round {{total_resp}}.
- The goal is to identify or create the SINGLE MOST CREATIVE idea, not to continually expand one idea.

- Actions you can take for the idea:
  - **Agree:** If the current idea is extremely creative and you cannot come up with a more creative idea, reply "Agree: No changes needed."
  - **Modify:** If the idea has a strong creative core but could be significantly elevated. Your modification should aim for a leap in originality or impact, not just a minor tweak. Use this format:
    "Modify: [full idea after modification] - Reason: [specific reason for improvement]."
  - **Replace:** If the idea is not creative or not aligned with the task objective, replace it by coming up with a new one of your own. Use this format:
    "Replace: [full replacement idea] - Reason: [specific reason for replacement]."
- The idea should be around 80-100 words.
"""

PS_DIRECT_DISCUSSION_ALL_AT_ONCE_NoPool = """
- You are reviewing the current idea.
- Your team has a maximum of {{max_rounds}} rounds to finalize the idea. You are on round {{total_resp}}.
- The goal is to identify or create the SINGLE MOST CREATIVE idea, not to continually expand one idea.

- Actions you can take for the idea:
  - **Agree:** If the current idea is extremely creative and you cannot come up with a more creative idea, reply "Agree: No changes needed."
  - **Modify:** If the idea has a strong creative core but could be significantly elevated. Your modification should aim for a leap in originality or impact, not just a minor tweak. Use this format:
    "Modify: [full idea after modification] - Reason: [specific reason for improvement]."
  - **Replace:** If the idea is not creative or not aligned with the task objective, replace it by coming up with a new one of your own, a more creative one. Be bold, especially in earlier rounds. Use this format:
    "Replace: [full replacement idea] - Reason: [specific reason for replacement]."
- The idea should be around 80-100 words.  
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
- The goal is to identify or create the SINGLE MOST CREATIVE idea, not to continually expand one idea.

- Actions you can take for each idea:
  - **Agree:** If the idea meets the task objective and does not require changes, reply "Agree: No changes needed."
  - **Modify:** If the idea is aligned with the task objective but needs improvement, propose modification. Use this format:
    "Modify: [full idea after modification] - Reason: [specific reason for improvement]."
  - **Replace:** If the idea is not creative or not aligned with the task objective, propose a new idea to replace the current one. Use this format:
    "Replace: [full replacement idea] - Reason: [specific reason for replacement]."

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
    "Modify: [full idea after modification] - Reason: [specific reason for improvement]."
  - **Replace**: If the idea is not creative or not aligned with the task objective, propose a new idea to replace the current one. Use this format:
    "Replace: [full replacement idea] - Reason: [specific reason for replacement]."

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
- Your team has a maximum of {{max_rounds}} rounds to finalize the list of ideas. You are currently on round {{total_resp}}.
- Please be mindful that your team has limited rounds to finalize the idea.

- Actions you can take for the idea:
  - **Agree:** If the idea meets the task objective and does not require changes, reply "Agree: No changes needed."
  - **Modify:** If the idea is aligned with the task objective but needs improvement, propose modification. Use this format:
    "Modify: [full idea after modification] - Reason: [specific reason for improvement]."
  - **Replace:** If the idea is not creative or not aligned with the task objective, propose a new idea to replace the current one. Use this format:
    "Replace: [full replacement idea] - Reason: [specific reason for replacement]."
- The idea should be around 80-100 words.
"""

PS_DIRECT_DISCUSSION_ALL_AT_ONCE = """
- You are reviewing the current idea. 
- Your team has a maximum of {{max_rounds}} rounds to finalize the list of ideas. You are currently on round {{total_resp}}.
- Please be mindful that your team has limited rounds to finalize the idea.

- Actions you can take for the idea:
  - **Agree:** If the current idea is extremely creative and you cannot come up with a more creative idea, reply "Agree: No changes needed."
  - **Modify:** If the idea is moderately creative and could use improvement, propose modification. Use this format:
    "Modify: [full idea after modification] - Reason: [specific reason for improvement]."
  - **Replace:** If the idea is not creative or not aligned with the task objective, propose a new idea to replace the current one. Use this format:
    "Replace: [full replacement idea] - Reason: [specific reason for replacement]."
- The idea should be around 80-100 words.
"""

PS_DIRECT_DISCUSSION_ALL_AT_ONCE_RESTRICTION_FIRST = """
- You are reviewing the current idea. 
- Your team has a maximum of {{max_rounds}} rounds to finalize the list of ideas. You are currently on round {{total_resp}}.
- Please be mindful that your team has limited rounds to finalize the idea.

- Actions you can take for the idea:
  - **Modify:** If the idea is moderately creative and could use improvement, propose modification. Use this format:
    "Modify: [full idea after modification] - Reason: [specific reason for improvement]."
  - **Replace:** If the idea is not creative or not aligned with the task objective, propose a new idea to replace the current one. Use this format:
    "Replace: [full replacement idea] - Reason: [specific reason for replacement]."
- The idea should be around 80-100 words.
"""

PS_DIRECT_DISCUSSION_ALL_AT_ONCE_RESTRICTION_OTHER = """
- You are reviewing the current idea. 
- Your team has a maximum of {{max_rounds}} rounds to finalize the list of ideas. You are currently on round {{total_resp}}.
- Please be mindful that your team has limited rounds to finalize the idea.

- Actions you can take for the idea:
  - **Agree:** If the current idea is extremely creative and you cannot come up with a more creative idea, reply "Agree: No changes needed."
  - **Modify:** If the idea is moderately creative and could use improvement, propose modification. Use this format:
    "Modify: [full idea after modification] - Reason: [specific reason for improvement]."
  - **Replace:** If the idea is not creative or not aligned with the task objective, propose a new idea to replace the current one. Use this format:
    "Replace: [full replacement idea] - Reason: [specific reason for replacement]."
- The idea should be around 80-100 words.
"""

# Add new creative generation and practical improvement prompts
CREATIVE_IDEA_GENERATION = """
- You have a ranked list of ideas to address global warming as well as new ideas from this round. (See below for the list.)
- The goal is to generate exactly five radically NEW and CREATIVE ideas, inspired by, but NOT simply a combination of, the existing ideas.
- Think *transformatively*.  What fundamental shifts in approach are possible?
- Consider the TOP ranked ideas as inspiration, but don't be limited by them.
- Explore UNCONVENTIONAL combinations, technologies, and approaches.
- **Challenge assumptions.**  What if the usual constraints didn't apply?
- **Focus on HIGH IMPACT and NOVELTY.**  Feasibility is secondary at this stage.
- Please return only the ideas, each on a separate line. Do not include any explanations or additional text or numberings.
- The ideas should be around 80-100 words each.
Below you'll find:
- Previously ranked ideas (for reference)
- New ideas generated in this round
Your ideas should be radically different from both sets.
"""

PRACTICAL_IMPROVEMENT = """
Your task is to review the following list of creative ideas and refine each one.
Focus on enhancing their practical feasibility (e.g., clarifying implementation steps, identifying necessary resources, simplifying scope) while carefully preserving the core novelty and unique angle of the original idea.
Please return only the ideas, each on a separate line. Do not include any explanations or additional text or numberings.
The ideas should be around 80-100 words each.
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
    "PS_Selection_Rating_Novelty": PS_SELECTION_RATING_NOVELTY,
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
    "Intention_Prompt_Idea": INTENTION_PROMPT_IDEA,
    "PS_Discussion_Rating_NoPool": PS_DISCUSSION_RATING_NoPool,
    "PS_Direct_Discussion_AllAt_Once_NoPool": PS_DIRECT_DISCUSSION_ALL_AT_ONCE_NoPool,
    "Creative_Idea_Generation": CREATIVE_IDEA_GENERATION,
    "Practical_Improvement": PRACTICAL_IMPROVEMENT,
}
