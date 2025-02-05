# conversation.py
import logging
import datetime
import json

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
            "total_tokens_used": 0,
        }
        self.phase_token_usage = {
            "idea_generation": {"prompt_tokens_used": 0, "completion_tokens_used": 0, "total_tokens_used": 0},
            "selection": {"prompt_tokens_used": 0, "completion_tokens_used": 0, "total_tokens_used": 0},
            "discussion": {"prompt_tokens_used": 0, "completion_tokens_used": 0, "total_tokens_used": 0},
            "other": {"prompt_tokens_used": 0, "completion_tokens_used": 0, "total_tokens_used": 0},
        }
    
    def update_phase_token_usage(self, phase, prompt_tokens, completion_tokens):
        """
        Update the token usage for a specific phase.
        """
        if phase not in self.phase_token_usage:
            logging.warning(f"Unknown phase: {phase}. Skipping phase token update.")
            phase = "other"  # Default to "other" phase if phase is unknown

        # Update phase-specific statistics
        self.phase_token_usage[phase]["prompt_tokens_used"] += prompt_tokens
        self.phase_token_usage[phase]["completion_tokens_used"] += completion_tokens
        self.phase_token_usage[phase]["total_tokens_used"] += (prompt_tokens + completion_tokens)

        # Also update overall token usage
        self.token_usage["prompt_tokens_used"] += prompt_tokens
        self.token_usage["completion_tokens_used"] += completion_tokens
        self.token_usage["total_tokens_used"] += (prompt_tokens + completion_tokens)

    def get_token_summary(self):
        """
        Return a formatted summary of token usage, broken down by phases.
        """
        summary = []
        total_prompt_tokens = 0
        total_completion_tokens = 0

        # Iterate over phases and calculate their contributions
        for phase, usage in self.phase_token_usage.items():
            phase_prompt = usage.get("prompt_tokens_used", 0)
            phase_completion = usage.get("completion_tokens_used", 0)
            phase_total = phase_prompt + phase_completion
            total_prompt_tokens += phase_prompt
            total_completion_tokens += phase_completion

            summary.append(
                f"{phase.capitalize()} Phase:\n"
                f"  Prompt Tokens Used: {phase_prompt}\n"
                f"  Completion Tokens Used: {phase_completion}\n"
                f"  Total Tokens Used: {phase_total}\n"
            )

        # Add overall total
        summary.append(
            f"Overall:\n"
            f"  Total Prompt Tokens Used: {total_prompt_tokens}\n"
            f"  Total Completion Tokens Used: {total_completion_tokens}\n"
            f"  Grand Total Tokens Used: {total_prompt_tokens + total_completion_tokens}\n"
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
                f"  Total Tokens Used: {usage['total_tokens_used']}\n"
            )
        return summary

    # def get_previous_responses(self, idea_index=None):
    #     """
    #     Retrieve the last 3 responses from the chat history where phase='discussion'.
    #     Optionally filter by idea_index if provided.
    #     """
    #     phases = self.task_config.get("phases", "three_stage")
    #     previous_responses = []
    #     for entry in reversed(self.chat_history):
    #         if entry['phase'] == 'discussion' or phases == 'direct_discussion':
    #             if idea_index is not None:
    #                 if entry.get('idea_index') == idea_index:
    #                     previous_responses.append(f"{entry['agent']}: {entry['response']}")
    #             else:
    #                 previous_responses.append(f"{entry['agent']}: {entry['response']}")
    #         if len(previous_responses) == 3:
    #             break
    #     return list(reversed(previous_responses))

    def get_previous_responses(self, idea_index=None, current_phase=None):
        """
        Retrieve the last 3 responses from the chat history **within the same phase**.
        If in discussion phase, include the n-3 round's current_ideas and n-3/n-2/n-1 responses.

        - `idea_index` (optional): If provided, filters by a specific idea index.
        - `current_phase` (optional): Ensures we only fetch responses from a specific phase.
        """
        previous_responses = []
        n_minus_3_ideas = None  # To store n-3 round's current_ideas

        # Get current task phases (default: "three_stage")
        task_phases = self.task_config.get("phases", "three_stage")

        for i, entry in enumerate(reversed(self.chat_history)):
            entry_phase = entry["phase"]

            # Filter by current phase if specified
            if current_phase and entry_phase != current_phase:
                continue

            # Handle discussion phase
            if entry_phase == "discussion" or task_phases == "direct_discussion":
                if len(previous_responses) == 0:  # First response to include in n-3
                    n_minus_3_ideas = entry.get("current_ideas", [])

                if idea_index is not None:
                    if entry.get("idea_index") == idea_index:
                        previous_responses.append(f"\n{entry['agent']} said: {entry['response']}")
                else:
                    previous_responses.append(f"\n{entry['agent']} said: {entry['response']}")

            # Handle idea_generation phase
            elif entry_phase == "idea_generation":
                previous_responses.append(f"\n{entry['agent']} said: {entry['response']}")

            # Break if we have collected 3 responses
            if len(previous_responses) == 3:
                break

        # Reverse responses for chronological order
        previous_responses = list(reversed(previous_responses))

        # Include n-3 round's current_ideas if available
        if current_phase == "discussion" and n_minus_3_ideas:
            current_ideas_str = "\n".join(f"{i+1}. {idea}" for i, idea in enumerate(n_minus_3_ideas))
            previous_responses.insert(
                0, f"The initial ideas under discussion before team feedback:\n{current_ideas_str if current_ideas_str else '(none)'}\n"
            )

        return previous_responses



    def add_chat_entry(self, agent_name, prompt, response, phase, idea_index=None, prompt_tokens=0, completion_tokens=0,current_ideas=None):
        """
        Add a chat entry and update token usage.
        """
        try:
            entry = {
                'agent': agent_name,
                'prompt': prompt,
                'response': response,
                'phase': phase,
                'idea_index': idea_index if idea_index is not None else "N/A",
            }

            if phase == "discussion" and current_ideas is not None:
                entry['current_ideas'] = list(current_ideas)  # Store a copy of the current_ideas list
            self.chat_history.append(entry)


            # Update phase and overall token usage
            self.update_phase_token_usage(phase, prompt_tokens, completion_tokens)

        except Exception as e:
            logging.error("Failed to add chat entry: %s", e)
            raise

    def save_chat_history(self, filename=None):
        """
        Save the chat history and token usage to a file.
        """
        if not filename:
            filename = f"chat_history_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as file:
                # Save task configuration
                file.write("=== Task Configuration ===\n")
                file.write(json.dumps(self.task_config, indent=4))  # Pretty-print the task config
                file.write("\n\n=== Phase-wise Token Usage Summary ===\n")
                file.write(self.get_phase_token_summary())
                file.write("\n\n=== Token Usage Summary ===\n")
                file.write(self.get_token_summary())
                file.write("\n\n=== Chat History ===\n")

                for entry in self.chat_history:
                    file.write(f"{entry['agent']} ({entry['phase']}, Idea Index: {entry.get('idea_index', 'N/A')})\n")
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
            raise
