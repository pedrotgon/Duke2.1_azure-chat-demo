import asyncio
from semantic_kernel.agents import ChatCompletionAgent, GroupChatOrchestration, RoundRobinGroupChatManager
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion


chat_service = AzureChatCompletion(
    api_key="CxMDVEFLAczX9HJGl0qopd2PmItYRw1PYefKsv1dEEQiKpOcb7ibJQQJ99BGACfhMk5XJ3w3AAAAACOGD5Ez",
    endpoint="https://p1872-mcsbzpvy-swedencentral.cognitiveservices.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2025-01-01-preview",
    deployment_name="gpt-4o (version:2024-08-06)",
    api_version="2025-01-01-preview",
)


def get_agents():
    return [
        ChatCompletionAgent(
            name="Writer",
            instructions="You are a creative content writer. Generate and refine slogans based on feedback.",
            service=AzureChatCompletion(),
        ),
        ChatCompletionAgent(
            name="Reviewer",
            instructions="You are a critical reviewer. Provide detailed feedback on proposed slogans.",
            service=AzureChatCompletion(),
        ),
    ]

async def main():
    agents = get_agents()
    group_chat = GroupChatOrchestration(
        members=agents,
        manager=RoundRobinGroupChatManager(max_rounds=5),
    )
    runtime = InProcessRuntime()
    runtime.start()
    result = await group_chat.invoke(
        task="Create a slogan for a new electric SUV that is affordable and fun to drive.",
        runtime=runtime,
    )
    value = await result.get()
    print(f"Final Slogan: {value}")

    # Example Output:
    # Final Slogan: "Feel the Charge: Adventure Meets Affordability in Your New Electric SUV!"

    await runtime.stop_when_idle()

if __name__ == "__main__":
    asyncio.run(main())