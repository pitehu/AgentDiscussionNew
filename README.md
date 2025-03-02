# AgentDiscussionNew

## File Descriptions

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
