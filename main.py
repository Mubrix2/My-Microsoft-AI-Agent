import os
import asyncio
from dotenv import load_dotenv

# For Version 0.10.0+, we use the new import structure
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient

# 1. LOAD SECRETS
load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")

async def main():
    # 2. CONFIGURE THE "BRAIN" (GitHub Models Config)
    # This client connects to GitHub's free model hosting
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o",
        api_key=github_token,
        base_url="https://models.github.ai/inference",
    )

    # 3. CREATE THE AGENT (The Thinker)
    # In 0.10.0, agents are initialized with the model client directly
    assistant = AssistantAgent(
        name="assistant",
        model_client=model_client,
        system_message="You are a helpful AI assistant. Provide Python code in clear blocks."
    )

    # 4. RUN THE TASK
    # We use 'run' to start a simple session with the agent
    print("--- Starting AutoGen (v0.10.0) ---")
    response = await assistant.run(task="Write a Python script to check if a number is prime and test it with 17.")
    
    # Print the final result
    print(response.messages[-1].content)

# 5. RUN THE ASYNC LOOP
if __name__ == "__main__":
    asyncio.run(main())