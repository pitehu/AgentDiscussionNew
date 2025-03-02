# conversation.py
import logging
import datetime
import json
import os

class Conversation:
    def __init__(self, agents, data_strategy, task_config):
        self.agents = agents
        self.data_strategy = data_strategy
        self.task_config = task_config
        self.chat_history = []
        self.current_agent = None

        # Initialize token usage tracking
        self.token_usage = {
            "prompt_tokens_used": 0,
            "completion_tokens_used": 0,
            "reasoning_tokens_used":0,
            "total_tokens_used": 0
        }
        self.phase_token_usage = {
            "idea_generation": {"prompt_tokens_used": 0, "completion_tokens_used": 0, "reasoning_tokens_used":0, "total_tokens_used": 0},
            "selection": {"prompt_tokens_used": 0, "completion_tokens_used": 0, "reasoning_tokens_used":0, "total_tokens_used": 0},
            "discussion": {"prompt_tokens_used": 0, "completion_tokens_used": 0, "reasoning_tokens_used":0, "total_tokens_used": 0},
            "other": {"prompt_tokens_used": 0, "completion_tokens_used": 0, "reasoning_tokens_used":0, "total_tokens_used": 0},
        }
    
    def update_phase_token_usage(self, phase, prompt_tokens, completion_tokens,reasoning_tokens):
        """
        Update the token usage for a specific phase.
        """
        if phase not in self.phase_token_usage:
            logging.warning(f"Unknown phase: {phase}. Skipping phase token update.")
            phase = "other"  # Default to "other" phase if phase is unknown

        # Update phase-specific statistics
        self.phase_token_usage[phase]["prompt_tokens_used"] += prompt_tokens
        self.phase_token_usage[phase]["completion_tokens_used"] += completion_tokens
        self.phase_token_usage[phase]["reasoning_tokens_used"] += reasoning_tokens
        self.phase_token_usage[phase]["total_tokens_used"] += (prompt_tokens + completion_tokens + reasoning_tokens)

        # Also update overall token usage
        self.token_usage["prompt_tokens_used"] += prompt_tokens
        self.token_usage["completion_tokens_used"] += completion_tokens
        self.token_usage["reasoning_tokens_used"] += reasoning_tokens
        self.token_usage["total_tokens_used"] += (prompt_tokens + completion_tokens + reasoning_tokens)

    def get_token_summary(self):
        """
        Return a formatted summary of token usage, broken down by phases.
        """
        summary = []
        total_prompt_tokens = 0
        total_completion_tokens = 0
        total_reasoning_tokens = 0

        # Iterate over phases and calculate their contributions
        for phase, usage in self.phase_token_usage.items():
            phase_prompt = usage.get("prompt_tokens_used", 0)
            phase_reasoning = usage.get("reasoning_tokens_used", 0)
            phase_completion = usage.get("completion_tokens_used", 0)
            phase_total = phase_prompt + phase_completion
            total_prompt_tokens += phase_prompt
            total_reasoning_tokens += phase_reasoning
            total_completion_tokens += phase_completion

            summary.append(
                f"{phase.capitalize()} Phase:\n"
                f"  Prompt Tokens Used: {phase_prompt}\n"
                f"  Completion Tokens Used: {phase_completion}\n"
                f"  Reasoning Tokens Used: {phase_reasoning}\n"
                f"  Total Tokens Used: {phase_total}\n"
            )

        # Add overall total
        summary.append(
            f"Overall:\n"
            f"  Total Prompt Tokens Used: {total_prompt_tokens}\n"
            f"  Total Completion Tokens Used: {total_completion_tokens}\n"
            f"  Total Reasoning Tokens Used: {total_reasoning_tokens}\n"
            f"  Grand Total Tokens Used: {total_prompt_tokens + total_reasoning_tokens + total_completion_tokens}\n"
        )

        return "\n".join(summary)
    
    def get_phase_token_summary(self):
        """
        Return a summary of token usage for each phase.
        """
        summary = "=== Phase-wise Token Usage Summary ===\n"
        for phase, usage in self.phase_token_usage.items():
            summary += (
                f"{phase.capitalize()} Phase:\n"
                f"  Prompt Tokens Used: {usage['prompt_tokens_used']}\n"
                f"  Completion Tokens Used: {usage['completion_tokens_used']}\n"
                f"  Reasoning Tokens Used: {usage['reasoning_tokens_used']}\n"
                f"  Total Tokens Used: {usage['total_tokens_used']}\n"
            )
        return summary

    def get_previous_responses(self, idea_index=None, current_phase=None):
        previous_responses = []
        n_minus_3_ideas = None

        filtered_history = [entry for entry in self.chat_history if not current_phase or entry["phase"] == current_phase]
        chat_length = len(filtered_history)
        llm_count = self.task_config.get("llm_count", "none")

        if current_phase in ["discussion", "direct_discussion"]:
            # Extract n_minus_3_ideas with different conditions for discussion and direct_discussion
            if current_phase == "direct_discussion":
                if chat_length < 5:
                    target_index = 0  # For less than 5 entries, use the last one
                else:
                    target_index = chat_length - 3  # For 5 or more entries, use the 4th from the end
            elif current_phase == "discussion":
                if chat_length < 4:
                    target_index = 0  # For less than 4 entries, use the last one
                else:
                    target_index = chat_length - 3  # For 4 or more entries, use the 4th from the end

            if 0 <= target_index < chat_length:
                n_minus_3_ideas = filtered_history[target_index].get("current_ideas", [])

            # Extract previous_responses based on phase conditions
        if current_phase == "direct_discussion":
            # For direct_discussion, skip the oldest entry and get the latest 3
            history_to_use = filtered_history[1:] if chat_length > 1 else []
        else:
            # For discussion, use all history to get the latest 3
            history_to_use = filtered_history

        for i, entry in enumerate(reversed(history_to_use)):
            phase = entry["phase"]

            if phase in ["discussion", "direct_discussion"]:
                if idea_index is not None:
                    if entry.get("idea_index") == idea_index:
                        previous_responses.append(f"\n{entry['agent']} said: {entry['response']}")
                else:
                    previous_responses.append(f"\n{entry['agent']} said: {entry['response']}")

            elif phase == "idea_generation":
                previous_responses.append(f"\n{entry['agent']} said: {entry['response']}")

            if len(previous_responses) == 3 and not (current_phase == "idea_generation" and llm_count == 6):
                break

        previous_responses = list(reversed(previous_responses))  # Reverse to maintain chronological order

        if current_phase in ["discussion", "direct_discussion"] and n_minus_3_ideas:
            current_ideas_str = "\n".join(f"{i+1}. {idea}" for i, idea in enumerate(n_minus_3_ideas))
            previous_responses.insert(0, f"The initial ideas under discussion before team feedback:\n{current_ideas_str if current_ideas_str else '(none)'}")

        return previous_responses


    def add_chat_entry(self, agent_model_name, agent_name, prompt, response, phase, idea_index=None, prompt_tokens=0, completion_tokens=0,reasoning_tokens=0, current_ideas=None,round_number=None):
        """
        Add a chat entry and update token usage.
        """
        try:
            entry = {
                'agent': agent_name,
                'agent_model':agent_model_name,
                'prompt': prompt,
                'response': response,
                'phase': phase,
                'idea_index': idea_index if idea_index is not None else "N/A",
            }

            if phase in ["discussion","direct_discussion"]  and current_ideas is not None:
                entry['current_ideas'] = list(current_ideas)  # Store a copy of the current_ideas list
            

            if round_number is not None:
                entry['round'] = round_number  # add round number
            
            self.chat_history.append(entry)

            # Update phase and overall token usage
            # self.update_phase_token_usage(phase, prompt_tokens, completion_tokens,reasoning_tokens)

        except Exception as e:
            logging.error("Failed to add chat entry: %s", e)
            raise

    # Define a mapping for short names

    def sanitize_model_name(self, model_name):
        """
        Convert model names into a shorter, valid filename format.
        """
        MODEL_SHORT_NAMES = {
        "gemini-2.0-flash-thinking-exp": "gemini",
        "deepseek-ai/DeepSeek-R1": "deepseek",
        }
        if isinstance(model_name, list):
            model_part = "_".join([MODEL_SHORT_NAMES.get(m, m) for m in model_name])
        else:
            model_part = MODEL_SHORT_NAMES.get(model_name, model_name)  # Use short name if available

        invalid_chars = r'<>:"/\|?*'
        for char in invalid_chars:
            model_part = model_part.replace(char, "-")

        return model_part


    def save_chat_history(self, filename=None):
        """
        Save the chat history and token usage to a file.
        """
        if not filename:
            model_name = self.task_config.get("model", "unknown_model")
            temperature = self.task_config.get("temperature", "default_temp")
            llm_count = len(self.agents)
            persona_type = self.task_config.get("persona_type", "unknown_persona")
            phases = self.task_config.get("phases", "unknown_phases")
            generation_method = self.task_config.get("generation_method", "unknown_generation")

            try:
                model_part = self.sanitize_model_name(model_name) 
            except Exception as e:
                logging.error(f"sanitize_model_name failed: {e}")
                model_part = "unknown_model"
            
            if model_part == "deepseek-ai/DeepSeek-R1":
                base_filename = f"deepseek_{temperature}_{llm_count}_{persona_type}_DiscussionOnly.txt"
            elif model_part in ['o1-mini', 'o3-mini']:
                base_filename = f"{model_part}_#_{llm_count}_{persona_type}_{generation_method if phases != 'direct_discussion' else 'DiscussionOnly'}_Think.txt"
            elif phases == 'direct_discussion':
                base_filename = f"{model_part}_{temperature}_{llm_count}_{persona_type}_DiscussionOnly.txt"
            elif phases == 'three_stage':
                base_filename = f"{model_part}_{temperature}_{llm_count}_{persona_type}_{generation_method}_Think.txt"
            else:
                base_filename = "chat_history.txt" 

            filename = base_filename
            version = 1
            while os.path.exists(filename):
                filename = f"{os.path.splitext(base_filename)[0]}_v{version}.txt"
                version += 1

        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write("=== Task Configuration ===\n")
                file.write(json.dumps(self.task_config, indent=4))
                file.write("\n\n=== Phase-wise Token Usage Summary ===\n")
                file.write(self.get_phase_token_summary())
                file.write("\n\n=== Token Usage Summary ===\n")
                file.write(self.get_token_summary())
                file.write("\n\n=== Chat History ===\n")

                for entry in self.chat_history:
                    file.write(f"{entry['agent']}({entry['agent_model']}, {entry['phase']}, Idea Index: {entry.get('idea_index', 'N/A')}, Round: {entry.get('round', 'N/A')})\n")
                    file.write("-" * 80 + "\n")
                    file.write("Prompt:\n")
                    file.write(f"{entry['prompt']}\n")
                    file.write("-" * 80 + "\n")
                    file.write("Response:\n")
                    file.write(f"{entry['response']}\n")
                    file.write("**" * 80 + "\n\n")
            logging.info("Chat history saved to %s", filename)

        except Exception as e:
            logging.error("Failed to save chat history: %s", e)

            backup_filename = "chat_backup.txt"
            version = 1
            while os.path.exists(backup_filename):
                backup_filename = f"chat_backup_v{version}.txt"
                version += 1

            try:
                with open(backup_filename, "w", encoding="utf-8") as file:
                    file.write("=== Backup Chat History ===\n")
                    file.write(json.dumps(self.task_config, indent=4))
                    file.write("\n\n=== Chat History ===\n")

                    for entry in self.chat_history:
                        file.write(f"{entry['agent']}({entry['agent_model']}, {entry['phase']}, Idea Index: {entry.get('idea_index', 'N/A')}, Round: {entry.get('round', 'N/A')})\n")
                        file.write("-" * 80 + "\n")
                        file.write("Prompt:\n")
                        file.write(f"{entry['prompt']}\n")
                        file.write("-" * 80 + "\n")
                        file.write("Response:\n")
                        file.write(f"{entry['response']}\n")
                        file.write("**" * 80 + "\n\n")

                logging.info(f"Backup chat history saved to: {backup_filename}")

            except Exception as e:
                logging.error(f"Failed to save backup chat history: {e}")
                raise 

