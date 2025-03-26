# message_strategies.py

import re
import logging  # <-- Added for logging
from prompts import TASK_REQUIREMENTS
from utils import calculate_tokens

class GenericMessageStrategy:
    def __init__(self, task_config, data_strategy):
        self.task_config = task_config
        self.data_strategy = data_strategy

    def construct_messages(self, agent, phase, conversation, idea_index=None,total_resp=None,current_round=None, max_rounds=None, include_intention_prompt=False):
        msgs=[]
        single_llm_mode = len(conversation.agents) == 1 and not agent.system_message  # Check for single LLM and no persona
        persona_type =  self.task_config.get("persona_type", "none")
        model = agent.model_name  # Fetch the correct model for each agent
        role = (
            # "developer" if model in ['o3-mini','o1'] else
            "user" if model in ['o3-mini','o1','o1-mini',"deepseek-ai/DeepSeek-R1","gemini-2.0-flash-thinking-exp"] else
            "system"
        )

        # Add role description unless it's a single LLM mode
        if not single_llm_mode and persona_type !='none':
            msgs.append({"role": role, "content": f"# **Role**\n{agent.system_message}"})
        # Overall
        if self.task_config.get("task_type","AUT")=="AUT":
            msgs.append({"role":role,"content": f"\n# **Task Requirement**\n{TASK_REQUIREMENTS['AUT_Mode1_Overall'].strip()}"})
        else:
            msgs.append({"role":role,"content": f"\n# **Task Requirement**\n{TASK_REQUIREMENTS['PS_Overall'].strip()}"})

        # Adjust content based on phase and task configuration
        if single_llm_mode:
            self._add_single_llm_instructions(msgs, agent, conversation)
        elif phase=="idea_generation":
            self._add_generation_instructions(msgs, agent, conversation)
        elif phase=="selection":
            self._add_selection_instructions(msgs, agent, conversation)
        elif phase=="iterative_refinement":
            self._add_iterative_refinement_instructions(msgs, agent, conversation)
        elif phase=="discussion":
            self._add_discussion_instructions(msgs, agent, conversation, idea_index,total_resp=total_resp,current_round=current_round, max_rounds=max_rounds)
            if include_intention_prompt:
                if (self.task_config.get("task_type","AUT")=="AUT" and self.task_config.get("discussion_method","all_at_once")=="one_by_one") or self.task_config.get("task_type","AUT")=="PS":
                    intention_prompt = TASK_REQUIREMENTS["Intention_Prompt_Idea"]
                else:
                    intention_prompt = TASK_REQUIREMENTS["Intention_Prompt_Ideas"]
                msgs.append({"role": "user", "content": "\n\n"+intention_prompt.strip()})
        elif phase == "direct_discussion":
            self._add_direct_discussion_instructions(msgs, agent, conversation, total_resp, current_round)
            if include_intention_prompt:
                intention_prompt = TASK_REQUIREMENTS["Intention_Prompt"]
                msgs.append({"role": "user", "content": "\n\n"+intention_prompt.strip()})
        elif phase == "open_discussion":
            self._add_open_discussion_instructions(msgs, agent, conversation, current_round, max_rounds)

        return msgs
    
    def _add_single_llm_instructions(self, msgs, agent, conversation):
        """
        Add instructions specifically tailored for a single LLM scenario.
        """
        # This could be dynamic based on some specific task requirements defined elsewhere or simplified
        task_requirement = TASK_REQUIREMENTS['PS_Overall_Single']
        msgs.append({"role": "user", "content": f"# **Task Requirement**\n{task_requirement}"})

    def _add_generation_instructions(self, msgs, agent, conversation):
        """
        If generation_method=='dependent' & agent != first => show previous ideas, else just ask for new
        """
        gen_method= self.task_config.get("generation_method","independent")
        ttype= self.task_config.get("task_type","AUT")

        # check if we have first_agent
        if not self.data_strategy.first_agent_name:
            self.data_strategy.first_agent_name= agent.name
            is_first= True
        else:
            is_first= (agent.name== self.data_strategy.first_agent_name)

        if ttype=="AUT":
            if gen_method=="independent":
                msgs.append({"role":"user","content": f"# **Current Task**\n{TASK_REQUIREMENTS['AUT_Mode1_IdeaGeneration'].strip()}"})
            else:
                if is_first:
                    msgs.append({"role":"user","content": f"# **Current Task**\n{TASK_REQUIREMENTS['AUT_Mode1_IdeaGeneration'].strip()}"})
                else:
                    msgs.append({"role":"user","content": f"# **Current Task**\n{TASK_REQUIREMENTS['AUT_Mode1_IdeaGeneration_Dependent'].strip()}"})
        else:
            # PS
            if gen_method=="independent":
                msgs.append({"role":"user","content": f"# **Current Task**\n{TASK_REQUIREMENTS['PS_Generation'].strip()}"})
            else:
                if is_first:
                    msgs.append({"role":"user","content": f"# **Current Task**\n{TASK_REQUIREMENTS['PS_Generation'].strip()}"})
                else:
                    msgs.append({"role":"user","content": f"# **Current Task**\n{TASK_REQUIREMENTS['PS_Generation_Dependent'].strip()}"})
        
        if gen_method == "dependent" and not is_first:
            previous_responses = conversation.get_previous_responses(current_phase="idea_generation")
            history_str = "\n".join(previous_responses) if previous_responses else "No previous responses."
            msgs.append({"role": "user", "content": f"# **Previous ideas from other agents**\n{history_str}\n"})

    def _add_selection_instructions(self, msgs, agent, conversation):
        sel_method= self.task_config.get("selection_method","rating")
        ttype= self.task_config.get("task_type","AUT")

        if ttype=="AUT":
            if sel_method=="rating":
                msgs.append({"role":"user","content": f"\n# **Current Task**\n{TASK_REQUIREMENTS['AUT_Mode1_Selection_Rating'].strip()}"})
            else:
                msgs.append({"role":"user","content": f"\n# **Current Task**\n{TASK_REQUIREMENTS['AUT_Mode1_Selection_SelectionTop'].strip()}"})
        else:
            if sel_method=="rating":
                msgs.append({"role":"user","content": f"\n# **Current Task**\n{TASK_REQUIREMENTS['PS_Selection_Rating'].strip()}"})
            else:
                msgs.append({"role":"user","content": f"\n# **Current Task**\n{TASK_REQUIREMENTS['PS_Selection_SelectionTop'].strip()}"})

    def _add_discussion_instructions(self, msgs, agent, conversation, idea_index, total_resp=None, current_round=None, max_rounds=None):
        """
        Modify discussion phase instructions to integrate previous responses and to 
        structure the message flow according to specified requirements.
        """
        task_type = self.task_config.get("task_type", "AUT")
        disc_method = self.task_config.get("discussion_method", "all_at_once")
        sel_method = self.task_config.get("selection_method", "rating")
        # model = self.task_config.get("model", "gpt-4o")
        model = agent.model_name  # Fetch the correct model for each agent
        print(model)
        role = (
            # "developer" if model in ['o3-mini','o1'] else
            "user" if model in ['o3-mini','o1','o1-mini',"deepseek-ai/DeepSeek-R1","gemini-2.0-flash-thinking-exp"] else
            "system"
        )

        # Fetch and format previous responses
        previous_responses = conversation.get_previous_responses(idea_index if disc_method == "one_by_one" else None,current_phase="discussion")
        history_str = "\n".join(previous_responses) if previous_responses else "No previous responses."

        # Setup the task-specific prompt
        if task_type == 'AUT':
            if disc_method == "all_at_once":
                if sel_method == "rating":
                    prompt = TASK_REQUIREMENTS["AUT_Mode1_Discussion_Rating_AllAtOnce"]
                    prompt = (
                    prompt.replace("{{total_resp}}", str(total_resp + 1))
                )
                else:
                    prompt = (TASK_REQUIREMENTS["AUT_Mode1_Discussion_SelectionTop_AllAtOnce_FirstAgent"] if agent.name == self.data_strategy.first_agent_name
                            else TASK_REQUIREMENTS["AUT_Mode1_Discussion_SelectionTop_AllAtOnce_OtherAgents"])
                    prompt = (
                    prompt.replace("{{total_resp}}", str(total_resp + 1))
                )
            else:
                prompt_key = "AUT_Mode1_Discussion_Rating_OneByOne" if sel_method == "rating" else "AUT_Mode1_Discussion_SelectionTop_OneByOne"
                prompt = TASK_REQUIREMENTS[prompt_key]
                prompt = (
                    prompt.replace("{{idea_index}}", str(idea_index + 1))
                        .replace("{{current_round}}", str(current_round or 0))
                        .replace("{{max_rounds}}", str(max_rounds or 0))
                )
        else:
            if sel_method == "rating":
                pool_size = self.task_config.get("replacement_pool_size", 3)
                if pool_size == 0:
                    prompt = TASK_REQUIREMENTS["PS_Discussion_Rating_NoPool"]
                else:
                    prompt = TASK_REQUIREMENTS["PS_Discussion_Rating"]
            else:
                prompt = TASK_REQUIREMENTS["PS_Discussion_SelectionTop"]
            prompt = prompt.replace("{{total_resp}}", str(total_resp + 1))
            prompt = prompt.replace("{{max_rounds}}", str(self.task_config.get("max_rounds", 20)))

        # Display task-specific prompt first
        
        msgs.append({"role": role, "content": f"\n# **Current Task**\n{prompt.strip()}"})

        # Insert previous responses before current and replacement ideas
        msgs.append({"role": "user", "content": "\n# **Disucssion History**\nBelow is the discussion history for the past three rounds. Other team members' feedback on these ideas so far (last 3 responses, in chronological order):\n" + history_str +"\n"})

        current_ideas_str = "\n".join(f"{i+1}. {txt}" for i, txt in enumerate(self.data_strategy.current_ideas))
        replacement_ideas_str = self.get_replacement_ideas_str(agent, sel_method)

        if self.data_strategy.replaced_ideas:
            replaced_ideas_str = "\n".join(f"{i+1}. {idea}" for i, idea in enumerate(self.data_strategy.replaced_ideas))
            replaced_ideas_section = f"\n**Previously Replaced Ideas:**\n{replaced_ideas_str}"
        else:
            replaced_ideas_section = ""  

        # Append structured message with Markdown formatting
        msgs.append({"role": "user", "content": 
            "# **Current, Replacement, and Replaced Ideas**\n"
            "**Current Ideas Under Discussion:**\n"
            f"{current_ideas_str if current_ideas_str else '(None)'}\n\n"
            
            "**Replacement Ideas (yours):**\n"
            f"{replacement_ideas_str if replacement_ideas_str else '(None)'}"
            f"{replaced_ideas_section}" 
        })

    

    def get_replacement_ideas_str(self, agent, sel_method):
        """
        Fetch and format replacement ideas based on the selection method.
        """
        if sel_method == "rating":
            replacement_ideas = self.data_strategy.replacement_ideas
        else:  # selectionTop
            replacement_ideas = self.data_strategy.agent_replacement_ideas.get(agent.name, [])
        return "\n".join(f"{i+1}. {idea}" for i, idea in enumerate(replacement_ideas))
    
    def _add_direct_discussion_instructions(self, msgs, agent, conversation, total_resp=None, current_round=None, idea_index=None):
        """
        Add instructions for direct discussion mode, including first and subsequent rounds.
        """
        task_type = self.task_config.get("task_type", "AUT")
        discussion_method = self.task_config.get("discussion_method", "all_at_once")
        model = agent.model_name  # Fetch the correct model for each agent
        role = (
            # "developer" if model in ['o3-mini','o1'] else
            "user" if model in ['o3-mini','o1','o1-mini',"deepseek-ai/DeepSeek-R1","gemini-2.0-flash-thinking-exp"] else
            "system"
        )

        if total_resp == 0 or current_round == 1:
        # First round: Initial idea generation
            if task_type == "AUT":
                if discussion_method == "all_at_once":
                    prompt = TASK_REQUIREMENTS["AUT_Direct_First_Round_AllAtOnce"]
                else:  # one_by_one
                    prompt = TASK_REQUIREMENTS["AUT_Direct_First_Round_OneByOne"]
            else:  # PS
                prompt = TASK_REQUIREMENTS["PS_Direct_First_Round_AllAtOnce"]
        else:
            # Subsequent rounds: Modifications and agreements
            if task_type == "AUT":
                if discussion_method == "all_at_once":
                    prompt = TASK_REQUIREMENTS["AUT_Direct_Dicussion_AllAtOnce"]
                    prompt = prompt.replace("{{total_resp}}", str(total_resp + 1))
                else:  # one_by_one
                    prompt = TASK_REQUIREMENTS["AUT_Direct_Discussion_OneByOne"]
                    prompt = (
                    prompt.replace("{{current_round}}", str(current_round))
                        .replace("{{idea_index}}", str(idea_index or 0 + 1))
                        
                )
            else:  # PS
                prompt = TASK_REQUIREMENTS["PS_Direct_Discussion_AllAtOnce"]
                prompt = prompt.replace("{{total_resp}}", str(total_resp + 1))
                prompt = prompt.replace("{{max_rounds}}", str(self.task_config.get("max_rounds", 20)))


        # Fetch previous responses
        disc_method = self.task_config.get("discussion_method", "all_at_once")
        previous_responses = conversation.get_previous_responses(idea_index if disc_method == "one_by_one" else None,current_phase="direct_discussion")
        history_str = "\n".join(previous_responses) if previous_responses else "No previous responses."

        # Construct message content
        msgs.append({"role": role, "content": f"\n# **Current Task**\n{prompt.strip()}"})
        msgs.append({"role": "user", "content": f"\n# **Disucssion History**\nBelow is the discussion history for the past three rounds. Other team members' feedback on these ideas so far (last 3 responses, in chronological order): \n\n{history_str}"})

        # Add current and replacement ideas
        if total_resp == 0 or (disc_method == 'one_by_one' and current_round == 1):
            pass
        else:
            current_ideas_str = "\n".join(f"{i + 1}. {txt}" for i, txt in enumerate(self.data_strategy.current_ideas))
            msgs.append({"role": "user", "content": f"\n# **Current Ideas Under Discussion:**\n{current_ideas_str if current_ideas_str else '(none)'}"})

    def _add_open_discussion_instructions(self, msgs, agent, conversation, current_round=None, total_rounds=None):
        round_info = ""
        agreement_focus_section = ""
        is_final_rounds = False
        instruction_header = "# **Instruction: Open Discussion**\n" # Default header

        if current_round is not None and total_rounds is not None:
            round_info = f"Current Round: {current_round} of {total_rounds}\n"
            final_round_threshold = 5 # Or 3, adjust as needed
            
            if total_rounds - current_round < final_round_threshold:
                is_final_rounds = True
                instruction_header = "# **Instruction: Final Rounds - Drive Towards Agreement**\n" # More specific header
                # Create the dedicated agreement section
                agreement_focus_section = (
                    "---\n"
                    "**URGENT: FOCUS ON AGREEMENT**\n"
                    f"You are in the final {final_round_threshold} rounds. Your primary objective now is to **actively work towards reaching an agreement or concrete proposal.**\n"
                    "**Action Items for this round:**\n"
                    "1.  **Summarize** points of agreement and disagreement based on the history below.\n"
                    "2.  **Propose** specific compromises, solutions, or next steps towards resolution.\n"
                    "3.  **Ask** targeted questions ONLY to resolve remaining differences needed for agreement.\n"
                    "4.  **Avoid** introducing new, unrelated topics.\n"
                    "Review the history below with this goal in mind.\n"
                    "---\n"
                )

        # Base instruction body - might be slightly adjusted based on context
        if is_final_rounds:
             # In final rounds, the focus isn't really "share freely" anymore
             base_instruction_body = (
                 "Use the discussion history below to formulate a response that moves towards agreement, following the action items listed above.\n"
                 "--- Discussion History ---\n"
             )
        else:
            base_instruction_body = (
                 "In this open discussion phase, please share your thoughts freely to explore the topic. "
                 "Build upon previous points and share your perspective.\n"
                 "--- Discussion History ---\n"
             )

        # Append history
        history = conversation.get_previous_responses(current_phase="open_discussion")
        history_text = "\n".join(history) if history else "(No previous responses.)"

        # --- Combine Message Parts ---
        # Order: Header, Round Info, Agreement Focus (if applicable), Base Body Intro, History
        full_instruction = (
            instruction_header +
            round_info +
            agreement_focus_section + # Placed BEFORE the history
            base_instruction_body +
            history_text
        )
        
        msgs.append({"role": "user", "content": full_instruction})
        
        logging.info(f"Open discussion instructions added (Final Rounds: {is_final_rounds}), "
                     f"current_round={current_round}, total_rounds={total_rounds}")

    def _add_iterative_refinement_instructions(self, msgs, agent, conversation):
        """
        Add instructions for the iterative refinement process.
        This includes current ideas, previous discussion context, and clear guidance.
        """
        # Get the model and role
        model = agent.model_name
        role = "user" if model in ['o3-mini','o1','o1-mini',"deepseek-ai/DeepSeek-R1","gemini-2.0-flash-thinking-exp"] else "system"
        
        # Get task type
        task_type = self.task_config.get("task_type", "AUT")
        
        # 1. Add the main instructions
        instruction = """# **Iterative Idea Refinement**
Your goal is to generate ONE significantly improved and novel idea based on the provided context. Analyze the current idea(s) and discussion, identify weaknesses or opportunities, and create a superior alternative.

**Process:**
1.  **Review Current Idea(s):** Understand the core concept, strengths, and weaknesses of the idea(s) presented below.
2.  **Analyze Previous Discussion:** Identify key insights, critiques, suggestions, and unresolved points from the discussion context.
3. Create a new idea that is:
   - More original, useful, and novel
   - Addresses any limitations of the current idea(s)
   - Builds on discussion insights
   - Is clearly articulated and implementable
   - The idea should be around 80-100 words.

**Important:** 
- Focus on quality over quantity - create ONE excellent idea rather than multiple ideas
- Ensure your response is in valid, parseable JSON format with these exact field names
- Use proper escaping for any quotes within JSON strings (e.g., \\" for quotes inside strings)
- Structure your response in valid JSON format as follows:
{ "Thinking": "Your detailed thought process and reasoning here, including how this idea improves upon existing ones", "Idea": "Your concise, clear idea statement here" }

"""
        msgs.append({"role": role, "content": instruction})
        
        current_round = conversation.data_strategy.current_idea_index + 1 if hasattr(conversation.data_strategy, "current_idea_index") else 1
        max_rounds = self.task_config.get("max_responses", 15)  # Get the max_responses from task_config
        round_info = f"Round: {current_round} of {max_rounds}"
        msgs.append({"role": "user", "content": f"# **Round Information**\n{round_info}"})

        # 2. Add current ideas section
        current_ideas = conversation.data_strategy.current_ideas + conversation.data_strategy.replacement_ideas
        if current_ideas:
            current_ideas_formatted = "\n".join([f"{i+1}. {idea}" for i, idea in enumerate(current_ideas)])
            msgs.append({"role": "user", "content": f"# **Current Idea(s)**\n{current_ideas_formatted}"})
        
        # 3. Add previous discussion context
        prior_context = conversation.get_previous_responses(current_phase="discussion")
        if prior_context:
            msgs.append({"role": "user", "content": "# **Previous Discussion Context**\n" + "\n".join(prior_context)})
        
        # 4. Final prompt for generation
        msgs.append({"role": "user", "content": "Please generate a new idea that is significantly better and more novel than the current idea(s). Be creative but practical."})
        
        return msgs
