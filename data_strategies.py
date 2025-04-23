# data_strategies.py

import re
import json
import logging
from pydantic import BaseModel
from openai import OpenAI
from typing import List
from utils import calculate_tokens
from azure_model_service import AzureModelService

class GenericDataStrategy:
    def __init__(self, task_config):
        self.task_config = task_config
        self.intention_scores = {}

        # For AUT/PS
        self.all_ideas = []                 # [{'idea': str, 'agent': str}, ...]
        self.idea_scores = {}               # { idea_text: [scores] }
        self.ranked_ideas = []              # sorted by average

        # Discussion-time common
        self.current_ideas = []             # For all_at_once or one_by_one
        self.replacement_ideas = []         # For rating scenario (shared), or selectionTop scenario if you prefer
        self.left = []                      # leftover pool, used if we want to keep replacements at a certain size
        self.replaced_ideas = []
        # For selectionTop:
        self.agent_selected_ideas = {}      # {agent_name: [ idx1, idx2 ... ] or direct text}

        # agent_replacement_ideas: optional per-agent. We can do a dict if we want each agent own picks
        self.agent_replacement_ideas = {}   # {agent_name: [ "idea text", ... ] }

        # Agreement sets
        self.agreed_agents = set()          # For all_at_once (AUT)
        self.agreed_agents_per_idea = {}    # For one_by_one (AUT)
        self.agreed_agents_ps = set()       # For PS

        self.current_idea_index = 0
        self.first_agent_name = None

        self.model_service = AzureModelService()


    # ------------------ Idea Generation ------------------
    def collect_ideas(self, agent_name, agent_response):
        lines = self._extract_lines(agent_response)
        # This part remains the same
        for l in lines:
            self.all_ideas.append({'idea': l, 'agent': agent_name})

    def _extract_lines(self, text):
        """
        Extracts each non-empty line from the text as a separate item.
        """
        results = []
        # Split the text into lines
        for line in text.strip().split('\n'):
            # Remove leading/trailing whitespace
            stripped_line = line.strip()
            # If the line has content after stripping, add it to results
            if stripped_line:
                results.append(stripped_line)
        return results



    # ------------------ Selection Phase ------------------
    def collect_scores(self, agent_name, agent_response):
        scores_map= self._parse_rating_scores(agent_response)
        ttype= self.task_config.get("task_type","AUT")

        for idx, sc in scores_map.items():
            if 0<=idx<len(self.all_ideas):
                txt= self.all_ideas[idx]['idea']
                if txt not in self.idea_scores:
                    self.idea_scores[txt] = []
                self.idea_scores[txt].append(sc)

    def _parse_rating_scores(self, text):
        """
        parse 'Idea X: Y' or 'Solution X: Y' => { (X-1): Y }
        """
        pattern = r'(?:Idea\s*)?(\d+)[\s:\-]+(\d+)'
        out={}
        for line in text.split('\n'):
            line=line.strip()
            match= re.search(pattern, line, re.IGNORECASE)
            if match:
                idx= int(match.group(1))-1
                sc= int(match.group(2))
                out[idx]= sc
        return out

    def calculate_rankings_by_average(self,conversation):
        """
        Calculate average scores for each idea, rank them in descending order, 
        and add the process to the chat history.
        """
        try:
            items = []
            for txt, sc_list in self.idea_scores.items():
                avg = sum(sc_list) / len(sc_list)
                items.append((txt, avg))
            
            # Sort items by average score in descending order
            items.sort(key=lambda x: x[1], reverse=True)
            self.ranked_ideas = [x[0] for x in items]

            # Log and record the process
            rank_summary = "\n".join(
                [f"Rank {i+1}: {idea} (Avg Score: {avg:.2f})" for i, (idea, avg) in enumerate(items)]
            )
            conversation.add_chat_entry(
                model_name="System",
                agent_name='System',
                prompt="Ranking ideas based on average scores.",
                response=f"Ranked Ideas:\n{rank_summary}",
                phase="other",
            )
            print(f"Ranked Ideas:\n{rank_summary}")
        except Exception as e:
            logging.error("Error calculating rankings by average: %s", e)
            raise

    def collect_selections(self, agent_name, agent_response):
        lines= agent_response.strip().split('\n')
        idxs=[]
        for line in lines:
            line=line.strip()
            match= re.match(r'^\s*(?:\d+\.)?\s*(?:Idea)?\s*(\d+)[\s:.-]*', line, re.IGNORECASE)
            if match:
                i= int(match.group(1))-1
                idxs.append(i)
        ttype= self.task_config.get("task_type","AUT")
        if ttype=="AUT":
            idxs= idxs[:5]
        else:
            idxs= idxs[:3]
        self.agent_selected_ideas[agent_name]= idxs
        print(agent_name, self.agent_selected_ideas)
        print("")

    # ------------------ Discussion / Agreement ------------------
    def reset_agreements(self):
        ttype= self.task_config.get("task_type","AUT")
        dmethod= self.task_config.get("discussion_method","all_at_once")
        if ttype=="AUT":
            if dmethod=="all_at_once":
                self.agreed_agents= set()
            else:
                idx= self.current_idea_index
                self.agreed_agents_per_idea[idx]= set()
        else:
            self.agreed_agents_ps= set()

    def agent_has_agreed(self, agent_name):
        ttype= self.task_config.get("task_type","AUT")
        dmethod= self.task_config.get("discussion_method","all_at_once")
        if ttype=="AUT":
            if dmethod=="all_at_once":
                return agent_name in self.agreed_agents
            else:
                idx= self.current_idea_index
                return agent_name in self.agreed_agents_per_idea.get(idx, set())
        else:
            return agent_name in self.agreed_agents_ps
    
    def _set_agent_agreed(self, agent_name):
        ttype= self.task_config.get("task_type","AUT")
        dmethod= self.task_config.get("discussion_method","all_at_once")
        if ttype=="AUT":
            if dmethod=="all_at_once":
                self.agreed_agents.add(agent_name)
            else:
                idx= self.current_idea_index
                if idx not in self.agreed_agents_per_idea:
                    self.agreed_agents_per_idea[idx] = set()
                self.agreed_agents_per_idea[idx].add(agent_name)
        else:
            self.agreed_agents_ps.add(agent_name)

    def all_agents_agreed(self, agents):
        ttype= self.task_config.get("task_type","AUT")
        dmethod= self.task_config.get("discussion_method","all_at_once")
        if ttype=="AUT":
            if dmethod=="all_at_once":
                return len(self.agreed_agents)== len(agents)
            else:
                idx= self.current_idea_index
                return len(self.agreed_agents_per_idea.get(idx, set()))== len(agents)
        else:
            return len(self.agreed_agents_ps)== len(agents)

    def update_shared_data(self, conversation, agent_response):

        agent_name= conversation.current_agent.name

        # 1) use GPT to interprete agent_response =>  "If_agree", "current_ideas", "replacement_ideas"
        # Call the parsing function
        parse_result, prompt_tokens, completion_tokens,reasoning_tokens = self._parse_agent_response_with_gpt(agent_response, agent_name)
        print("parse_result", parse_result)
        # Update token usage in the conversation
        conversation.update_phase_token_usage("other",prompt_tokens, completion_tokens,reasoning_tokens)

        # 2) if parse_result["If_agree"] == True => self._set_agent_agreed
        action_type = parse_result.action_type
        self.current_ideas = parse_result.current_ideas
        replaced_ideas = parse_result.replaced_ideas

        # Append replaced idea if applicable
        if action_type == "replace" and replaced_ideas:
            self.replaced_ideas.append(replaced_ideas)
            print(self.replaced_ideas)

        # Phases-specific logic
        phases = self.task_config.get("phases", "three_stage")
        if phases == "direct_discussion":
            # For direct_discussion, only update current_ideas; replacement_ideas are not relevant
            if action_type == "agree":
                self._set_agent_agreed(agent_name)
            elif action_type in {"modify", "replace", "adjust"}:
                print(f"Agent {agent_name} chose to {action_type} ideas.")
                self.reset_agreements()

        else:
            if action_type == "agree":
                self._set_agent_agreed(agent_name)
            elif action_type in {"modify", "replace","adjust"}:

                print(f"Agent {agent_name} chose to {action_type} ideas.")
                self.reset_agreements()
                sel_method = self.task_config.get("selection_method", "rating")
                if sel_method == "selectionTop":
                    self.agent_replacement_ideas[agent_name] = parse_result.replacement_ideas
                
                else:
                    self.replacement_ideas = parse_result.replacement_ideas
                    ttype = self.task_config.get("task_type", "AUT")
                    if ttype == "AUT":
                        desired_size = 5
                    else:
                        # PS branch: use config option (default: 3)
                        desired_size = self.task_config.get("replacement_pool_size", 3)
                    if len(self.replacement_ideas) < desired_size and self.left:
                        gap = desired_size - len(self.replacement_ideas)
                        for _ in range(gap):
                            if self.left:
                                self.replacement_ideas.append(self.left[0])
                                self.left.pop(0)


    
    def _parse_agent_response_with_gpt(self, agent_response, agent_name):
        """
        Parses the agent's response, adapting to the discussion method.
        """
        ttype= self.task_config.get("task_type","AUT")
        phases = self.task_config.get("phases", "three_stage")

        if phases == 'three_stage':
            if ttype=="AUT":
                discussion_method = self.task_config.get("discussion_method", "one_by_one")
        
                if discussion_method == "one_by_one":
                    return self._parse_one_by_one_response(agent_response, agent_name)
                elif discussion_method == "all_at_once":
                    return self._parse_all_at_once_response(agent_response, agent_name)
                else:
                    raise ValueError(f"Unsupported discussion method: {discussion_method}")
            else:
                return self._parse_one_by_one_response(agent_response, agent_name)
        
        elif phases == "direct_discussion":
            discussion_method = self.task_config.get("discussion_method", "all_at_once")
            if ttype == 'AUT':
                if discussion_method == "all_at_once":
                    return self._parse_direct_all_at_once_response(agent_response, agent_name)
                elif discussion_method == "one_by_one":
                    return self._parse_direct_one_by_one_response(agent_response, agent_name)
            elif ttype == 'PS':
                return self._parse_direct_one_by_one_response(agent_response, agent_name)
            else:
                raise ValueError(f"Unsupported discussion method for direct_discussion: {discussion_method}")


    def _parse_one_by_one_response(self, agent_response, agent_name):
        """
        GPT + pydantic parse approach => we must provide current_ideas, replacement_ideas, agent_name in the prompt.
        """
        class AgentResponse(BaseModel):
            action_type: str  # "agree", "modify", or "replace"
            current_ideas: List[str]  
            replacement_ideas: List[str]
            replaced_ideas: str = None  

        # 1) figure out which replacement pool to display:
        sel_method = self.task_config.get("selection_method", "rating")
        if sel_method == "rating":
            # Shared
            rep_list = self.replacement_ideas
        else:
            # selectionTop => each agent has their own replacement pool
            # if not exist => fallback empty
            rep_list = self.agent_replacement_ideas.get(agent_name, [])

        # 2) build the strings
        current_str = "\n".join(f"- {idea}" for idea in self.current_ideas)
        replacement_str = "\n".join(f"- {idea}" for idea in rep_list)

        system_msg_one_by_one = f"""Here is the current list of ideas:
        {current_str if current_str else "(none)"}

        Here is the replacement ideas list:
        {replacement_str if replacement_str else "(none)"}

        Based on the agent's response, judge whether the agent:
        - **Agrees** with the current ideas without suggesting any changes. The agent explicitly says "Agree:..."
        - **Modifies** any of the current ideas. The agent explicitly says "Modify:..."
        - **Replaces** any of the current ideas with one from the replacement pool. The agent explicitly says "Replace:..."

        For each action, the agent must ensure that the lists reflect the following updates:

        1. **Agree**: 
            - If the agent agrees, the `current_ideas` remain unchanged.
            - The `replacement_ideas` list also remains unchanged.

        2. **Modify**:
            - If the agent modifies an idea, update the `current_ideas` list with the modified version of the idea.
            - The `replacement_ideas` list remains unchanged.

        3. **Replace**:
            - If the agent replaces an idea:
                - Update the `current_ideas` list by the agent's newply proposed idea, VERBATIM.
                - Remove the selected replacement idea from the `replacement_ideas` list. Skip if there is no replacement idea.
                - Move the replaced idea to the `replaced_ideas` list by appending this list.
        
        **Important**:
            - The `current_ideas` list must only include **one idea**. If the agent modifies or replaces an idea, ensure that the `current_ideas` list reflects this change.
            - The `replacement_ideas` list must reflect the updated pool after any replacements.
            - The `replaced_ideas` list must include the replaced idea(s) for record-keeping.
            - You MUST preserve the VERBATIM original text and formatting of all idea strings in the output. 

        The expected output JSON structure should detail the action taken, the updated list of current ideas (only include one idea), an updated list of replacement ideas and an updated list of replaced ideas, all must in full and not shortened:
        {{
            "action_type": "agree/modify/replace",
            "current_ideas": [],
            "replacement_ideas": [],
            "replaced_ideas": [],
        }}
        """.strip()

        messages = [
            {"role": "system", "content": system_msg_one_by_one},
            {"role": "user", "content": agent_response}
        ]

        return self._call_gpt_and_parse(messages, AgentResponse)
        
    
    def _parse_all_at_once_response(self, agent_response, agent_name):
        """
        Parses the agent's response for all ideas in all_at_once discussion mode with a simplified action_type.
        """
        class AgentResponse(BaseModel):
            action_type: str  # "agree" or "adjust"
            current_ideas: List[str]  # Updated list of current ideas (always 5 items)
            replacement_ideas: List[str]  # Updated replacement pool after adjustments
            replaced_ideas: str = None

        # 1) figure out which replacement pool to display:
        sel_method = self.task_config.get("selection_method", "rating")
        if sel_method == "rating":
            # Shared
            rep_list = self.replacement_ideas
        else:
            # selectionTop => each agent has their own replacement pool
            # if not exist => fallback empty
            rep_list = self.agent_replacement_ideas.get(agent_name, [])

        # Build strings for current ideas and replacement pool
        current_str = "\n".join(f"{i + 1}. {idea}" for i, idea in enumerate(self.current_ideas))
        replacement_str = "\n".join(f"{i + 1}. {idea}" for i, idea in enumerate(rep_list))

        system_msg_all_at_once = f"""
        Here is the current list of ideas being reviewed:
        {current_str if current_str else "(none)"}

        Here is the replacement ideas list:
        {replacement_str if replacement_str else "(none)"}

        Based on the agent's response, evaluate the entire list:
        - **Agree**: Reply "Agree: The list meets all objectives." if the list requires no changes.
        - **Adjust**: Reply "Adjust: Updates applied to the list as per individual idea evaluations." if any modifications or replacements are needed.

        For each idea:
        - **Agree**: Reply "Agree: No changes needed."
        - **Modify**: Reply "Modify: [updated idea] - Reason: [specific reason]."
        - **Replace**: Reply "Replace: [full replacement idea] - Reason: [why this is better and what the original idea lacks]."

        Updates to apply:
        - **Agree**: No changes to the `current_ideas` or `replacement_ideas`.
        - **Modify**: Update the `current_ideas` list with the modified idea; do not modify or shorten the `replacement_ideas`.
        - **Replace**: 
            1. Replace the idea in `current_ideas` with the selected replacement idea.
            2. Remove the used replacement idea from the replacement_ideas pool to ensure it’s no longer available for further use.
            3. Discard the replaced idea and move it to the `replaced_ideas` list for record-keeping.

        Ensure the `current_ideas` list always contains exactly 5 ideas after adjustments.
        **IMPORTANT: When constructing the `current_ideas` and `replacement_ideas` lists in the JSON output, you MUST use the exact, full, original text of each idea as presented in the input context above. Do NOT shorten or summarize the ideas unless an idea was specifically modified (in which case, use the full modified text). Preserve formatting like newlines within the idea text if possible.**
        Expected output JSON:
        {{
            "action_type": "agree" or "adjust",
            "current_ideas": ["idea1", "idea2", "idea3", "idea4", "idea5"],
            "replacement_ideas": ["idea6", "idea7", ...],
            "replaced_ideas": ["idea1", "idea2",...]
        }}
        """.strip()

        messages = [
            {"role": "system", "content": system_msg_all_at_once},
            {"role": "user", "content": agent_response}
        ]

        return self._call_gpt_and_parse(messages, AgentResponse)


    def _call_gpt_and_parse(self, messages, response_model):
        """
        Sends messages to GPT and parses the response using the given response model.
        """
        model = "gpt-4o"
        phases = self.task_config.get("phases", "three_stage")

        try:
            response = self.model_service.parse_response(messages, model=model, response_model=response_model)
            data = response.choices[0].message.parsed
            print(data)
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            reasoning_tokens = 0
            
            if phases == "direct_discussion":
                if hasattr(data, 'action_type') and hasattr(data, 'current_ideas'):
                    return data, prompt_tokens, completion_tokens,reasoning_tokens
                else:
                    raise ValueError("Incomplete data in parsed response for direct_discussion.")
            else:
                if hasattr(data, 'action_type') and hasattr(data, 'current_ideas') and hasattr(data, 'replacement_ideas') and hasattr(data, 'replaced_ideas'):
                    return data, prompt_tokens, completion_tokens,reasoning_tokens
                else:
                    raise ValueError("Incomplete data in parsed response for three_stage.")
        except Exception as e:
            print(f"Error in parsing agent response: {e}")
            fallback_data = {
                "action_type": "agree",
                "current_ideas": self.current_ideas,
            }
            if phases != "direct_discussion":
                fallback_data["replacement_ideas"] = self.replacement_ideas
            return fallback_data, prompt_tokens, 0, 0

    def _parse_direct_all_at_once_response(self, agent_response, agent_name):
        """
        Parses the agent's response for all ideas in all_at_once discussion mode under direct_discussion.
        """
        class AgentResponse(BaseModel):
            action_type: str  # "agree" or "adjust"
            current_ideas: List[str]  # Updated list of current ideas (always 5 items)

        # Build strings for current ideas
        current_str = "\n".join(f"{i + 1}. {idea}" for i, idea in enumerate(self.current_ideas))

        # Update the system message to reflect direct_discussion requirements
        system_msg_all_at_once = f"""
        You are reviewing the current list of ideas in the context of a direct discussion session:
        {current_str if current_str else "(none)"}

        Actions you can take for the list:
        - **Agree**: Reply "Agree: The list meets all objectives." if no changes are needed.
        - **Adjust**: Reply "Adjust: Updates applied to the list as per individual evaluations." if any modifications or replacements are required.

        For each idea:
        - **Agree**: Reply "Agree: No changes needed."
        - **Modify**: Reply "Modify: [updated idea] - Reason: [specific reason]."
        - **Replace**: Propose a **new idea** to replace the current idea. Use this format:
            "Replace: [new idea] - Reason: [why this is better aligned with the task objectives and what the current idea lacks]."

        Updates to apply:
        - **Agree**: Keep the `current_ideas` list unchanged.
        - **Modify**: Update the `current_ideas` list with the modified idea. 
        - **Replace**: Replace the idea in `current_ideas` with the proposed new idea. Ensure that the updated `current_ideas` list always contains exactly 5 ideas.

        Expected output JSON:
        {{
            "action_type": "agree" or "adjust",
            "current_ideas": ["idea1", "idea2", "idea3", "idea4", "idea5"]
        }}
        """.strip()

        messages = [
            {"role": "system", "content": system_msg_all_at_once},
            {"role": "user", "content": agent_response}
        ]

        return self._call_gpt_and_parse(messages, AgentResponse)

    def _parse_direct_one_by_one_response(self, agent_response, agent_name):
        """
        GPT + pydantic parse approach => we must provide current_ideas, replacement_ideas, agent_name in the prompt.
        """
        class AgentResponse(BaseModel):
            action_type: str  # "agree", "modify", or "replace"
            current_ideas: List[str]
            replaced_ideas: str = None  


        current_str = "\n".join(f"- {idea}" for idea in self.current_ideas)

        system_msg_one_by_one = f"""Here is the current idea:
        {current_str if current_str else "(none)"}

        Based on the agent's response, judge whether the agent:
        - **Agrees**  Reply "Agree: No changes needed."
        - **Modifies** Reply "Modify: [updated idea] - Reason: [specific reason]."
        - **Replaces** Propose a **new idea** to replace the current idea. "Replace: [new idea] - Reason: [specific reason]"

        Updates to apply:
        1. **Agree**: Keep the `current_ideas` unchanged.
        2. **Modify**: URevise the `current_ideas` by incorporating the proposed modifications, ensuring the updated version accurately reflects the changes.
        3. **Replace**: Replace the idea in `current_ideas` with the proposed new idea. Ensure the updated `current_ideas` list contains exactly one idea. Discard the replaced idea and move it to the `replaced_ideas` list for record-keeping.

        Expected output JSON:
        {{
            "action_type": "agree/modify/replace",
            "current_ideas": ["idea1"]
            "replaced_ideas": ["idea1", "idea2",...]
        }}
        """.strip()

        messages = [
            {"role": "system", "content": system_msg_one_by_one},
            {"role": "user", "content": agent_response}
        ]

        return self._call_gpt_and_parse(messages, AgentResponse)
    
    def collect_intention_score(self, agent_name, response):
        """
        Collects the intention score directly from the agent's response.
        Expects the response format to include 'Score:X', where X is a number between 1-7.
        """
        import re

        # Use regex to extract the score from the response
        match = re.search(r'Score:\s*([1-7])', response)
        if match:
            score = int(match.group(1))  # Extract the numeric part
            self.intention_scores[agent_name] = score
            print(f"Collected intention score {score} from {agent_name}.")
        else:
            print(f"Invalid intention score format from {agent_name}: {response}")
            self.intention_scores[agent_name] = None  # Handle invalid responses gracefully


    def get_highest_intention_agent(self, candidates):
        """
        Returns the agent with the highest intention score among the candidates.
        """
        sorted_scores = sorted(
            [(self.intention_scores.get(agent.name, 0), agent) for agent in candidates],
            key=lambda x: (-x[0], x[1].name)  # Sort by score descending, then by name
        )
        return sorted_scores[0][1] if sorted_scores else None