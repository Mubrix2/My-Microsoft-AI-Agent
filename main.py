import os
import asyncio
from dotenv import load_dotenv

# Importing the new team-based tools from AutoGen 0.10.x
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")

async def main():
    # 1. THE PHONE LINE (Connecting to the GitHub Brain)
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o",
        api_key=github_token,
        base_url="https://models.github.ai/inference",
    )

    # 2. EMPLOYEE 1: THE CODER
    coder = AssistantAgent(
        name="coder",
        model_client=model_client,
        system_message="You are a Python Developer. Write code to solve tasks. Always end your message by asking the reviewer for feedback."
    )

    # 3. EMPLOYEE 2: THE SENIOR REVIEWER
    # This employee's handbook says: "Don't let bad code pass!"
    reviewer = AssistantAgent(
        name="reviewer",
        model_client=model_client,
        system_message="""You are a Senior Reviewer. Check the code for accuracy and speed.
        If the code is perfect, end your message with the exact word: APPROVE.
        If it needs work, tell the coder what to fix."""
    )

    # 4. THE MEETING RULES (Termination)
    # The meeting ends if someone says "APPROVE" or if they've talked for 10 turns.
    termination = TextMentionTermination("APPROVE") | MaxMessageTermination(10)

    # 5. THE MEETING ROOM (The Team)
    team = RoundRobinGroupChat([coder, reviewer], termination_condition=termination)

    # 6. START THE WORK
    print("--- The Meeting is Starting ---")
    
    # We use 'run_stream' so we can watch them talk in real-time
    async for message in team.run_stream(task="Write a Python function for the 10th Fibonacci number."):
        if hasattr(message, 'content'):
            print(f"\n>> {message.source.upper()} says:\n{message.content}")
            print("-" * 30)

if __name__ == "__main__":
    asyncio.run(main())