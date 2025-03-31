# Agent Discussion
## File Descriptions

## Done
- [x] first agent propose idea and then directly open discussion implement this open condition;
- [x] Add a round warning at the beginning for the last 5 rounds (at least for some conditions)
- [x] implement replacement idea pool as a function (it can be top-k ideas, or 0 meaning no replacement pool)
- [x] Improve some of the prompt design
- [x] First generate a new one, and then use current and past N ideas to rank (use clean chat history to call the agent), and then select the best one) replace if better; otherwise, pass; Kinda self-improve idea;  
- [x] two phases of idea generation, emphasize novelty, so then we have 30 ideas, then rate again, and select 5, then improve (c.f. existing code; Luning: you might need to experiment with this a bit more)



## To-do
- [ ] Check hand-raising implmentation: we need to decode everyone's answer first, and then ask for given what you said, how much willing are you to respond (we define what "contribution" mean, like you need to be quite different from current discussion etc)/, and then only keep the one with the highest rating； Tiancheng: probably only feasible with the default discussion way
- [ ] Implement idea tracking properly: What I will need to do: explicity record current_idea pool at every turn
- [ ] Implement the role-playing stuff in user prompt for every prompt (currently this is not done consistently)
- [ ] Implement the at round X, total of round Y, and the final rounds warning consistently, across all conditions (will require some refactoring, I think)
- [ ] Check every single prompt to make sure they are at least ok
- [ ] Do a thorough walk-through of the entire codebase to make sure we have everything implemented in the way we want to


1. **`agent.py`**  
   - Defines the `Agent` class, representing individual participants in the discussion.  
   - Handles agent-specific response generation and interaction with the discussion system.
   - Dynamically selects the appropriate service module (deepseek_service.py, genai_service.py, azure_service.py, etc.) based on the assigned model.

2. **`conversation.py`**  
   - Manages the conversation flow, including chat history, token tracking, and saving logs.  
   - Provides utility functions to fetch responses or summarize token usage.  

3. **`data_strategies.py`**  
   - Manages ideas, scores, and rankings throughout the discussion.  
   - Provides methods to calculate rankings, update shared data, and track agreements.  

4. **`discussion_modes.py`**  
   - Implements different discussion modes.  
   - Orchestrates the flow of agents and manages their responses.  

5. **`message_strategies.py`**  
   - Generates task-specific instructions and prompts based on the current phase and agent.  
   - Incorporates feedback and previously generated ideas into messages.  

6. **`batch_run.py`**  
   - Enables running multiple discussion sessions in batch mode.  
   - Automates execution for different configurations and stores results efficiently.  

7. **Service Modules**  
   - These modules handle interactions with different LLM providers:  
     - **`base_service.py`**: Provides a common interface for model interactions, serving as a base class for other services.  
     - **`deepseek_service.py`**: Manages API calls to DeepSeek models.  
     - **`genai_service.py`**: Handles requests to Google’s Gemini/PaLM models via Generative AI API.  
     - **`azure_service.py`**: Connects with Azure OpenAI services for model inference.  

8. **`config.py`**  
   - Stores global configuration settings, such as task types, phases, and discussion order.  
   - **Important**: Ensure to add your API key for models.  

9. **`prompts.py`**  
   - Contains predefined task requirements and prompts used throughout the discussion.  

10. **`roles.py`**  
      - Defines system and user roles, including default configurations for agents.  

11. **`utils.py`**  
      - Provides helper functions for token calculation, data formatting, and parsing.  

12. **`main.py`**  
      - The entry point for running the system.  
      - Loads configurations, initializes agents, and executes the discussion process.  
