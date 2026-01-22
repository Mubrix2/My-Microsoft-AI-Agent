import os
import asyncio
from dotenv import load_dotenv

from tools import get_weather, save_to_file
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

async def main():
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o",
        api_key=os.getenv("GITHUB_TOKEN"),
        base_url="https://models.github.ai/inference",
    )

    # 1. THE AI AGENT
    travel_agent = AssistantAgent(
        name="travel_agent",
        model_client=model_client,
        tools=[get_weather, save_to_file], 
        system_message="Prepare a travel tip and ask the user for permission to save it to a file."
    )

    # 2. THE HUMAN PROXY (You)
    # human_input_mode="ALWAYS" means it will stop and wait for you to type in the terminal.
    user_proxy = UserProxyAgent(name="user")

    # 3. THE TEAM
    # This creates a flow: Agent talks -> You talk -> Agent talks
    termination = TextMentionTermination("DONE")
    team = RoundRobinGroupChat([travel_agent, user_proxy], termination_condition=termination)

    print("--- Starting Mission with Human Oversight ---")
    
    await team.run(task="I'm going to London. Plan a tip and save it only if I say yes.")

if __name__ == "__main__":
    asyncio.run(main())