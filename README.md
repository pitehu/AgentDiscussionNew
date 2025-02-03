# AgentDiscussionNew

## File Descriptions

1. **`agent.py`**
   - Defines the Agent class, representing individual participants in the discussion.
   - Handles agent-specific response generation and interaction with the discussion system.

2. **`conversation.py`**
   - Manages the conversation flow, including chat history, token tracking, and saving logs.
   - Provides utility functions to fetch responses or summarize token usage.

3. **`data_strategies.py`**
   - Manages ideas, scores, and rankings throughout the discussion.
   - Provides methods to calculate rankings, update shared data, and track agreements.

4. **`discussion_modes.py`**
   - Implements different discussion modes:
     - **All-at-once**: Multiple agents discuss simultaneously.
     - **One-by-one**: Agents respond sequentially.
   - Orchestrates the flow of agents and manages their responses.

5. **`message_strategies.py`**
   - Generates task-specific instructions and prompts based on the current phase and agent.
   - Incorporates feedback and previously generated ideas into messages.

6. **`config.py`**
   - Stores global configuration settings, such as task types, phases, and discussion order.
   - Important: Ensure to add your API key for models

7. **`prompts.py`**
   - Contains predefined task requirements and prompts used throughout the discussion.

8. **`roles.py`**
   - Defines system and user roles, including default configurations for agents.

9. **`utils.py`**
   - Provides helper functions for token calculation, data formatting, and parsing.

10. **`main.py`**
   - The entry point for running the system.
   - Loads configurations, initializes agents, and executes the discussion process.
