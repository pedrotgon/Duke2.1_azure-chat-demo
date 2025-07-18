from dotenv import load_dotenv
import os
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter
from semantic_kernel.orchestration.sk_context import SKContext
from semantic_kernel.planning.basic_planner import BasicPlanner
import math


class TravelWeather:
    @sk_function(
        description="Takes a city and a month and returns the average temperature for that month.",
        name="travel_weather",
    )
    @sk_function_context_parameter(
        name="city", description="The city for which to get the average temperature."
    )
    @sk_function_context_parameter(
        name="month", description="The month for which to get the average temperature."
    )
    def weather(self, context: SKContext) -> str:
        return f"The average temperature in city in month is 75 degrees. {str(context.variables)}"

        city = context["city"]
        month = context["month"]
        return f"The average temperature in {city} in {month} is 75 degrees."
    


async def main():
    # Load the .env file. Replace the path with the path to your .env file.
    load_dotenv('E:\AI\Git\GitHub\Duke2.1_azure-chat-demo\Duke2.1_azure-chat-demo\.env')
    AZURE_OPEN_AI__CHAT_COMPLETION_DEPLOYMENT_NAME = os.environ["AZURE_OPEN_AI__CHAT_COMPLETION_DEPLOYMENT_NAME"]
    AZURE_OPEN_AI__ENDPOINT = os.environ["AZURE_OPEN_AI__ENDPOINT"]
    AZURE_OPEN_AI__API_KEY = os.environ["AZURE_OPEN_AI__API_KEY"]

    kernel = sk.Kernel(log=sk.NullLogger())
    kernel.add_chat_service(
        "chat-gpt",
        AzureChatCompletion(
            AZURE_OPEN_AI__CHAT_COMPLETION_DEPLOYMENT_NAME,
            AZURE_OPEN_AI__ENDPOINT,
            AZURE_OPEN_AI__API_KEY,
            api_version = "2024-12-01-preview"
        ),
    )


    #planner = BasicPlanner()
    weather_plugin = kernel.import_skill(TravelWeather(), skill_name="Travel")
    prompt_config = sk.PromptTemplateConfig.from_completion_parameters(
        max_tokens=2000,
        temperature=0.7,
        top_p=0.8,
        function_call="auto",
        chat_system_prompt="You are a travel weather chat bot. Your name is Frederick. You are trying to help people find the average temperature in a city in a month.",
    )
    prompt_template = sk.ChatPromptTemplate(
        "{{$user_input}}", kernel.prompt_template_engine, prompt_config
    )
    prompt_template.add_user_message("Hi there, who are you?")
    prompt_template.add_assistant_message(
        "I am Frederic, a chat bot. I'm trying to figure out what people need."
    )

    function_config = sk.SemanticFunctionConfig(prompt_config, prompt_template)
    chat_function = kernel.register_semantic_function("ChatBot", "Chat", function_config)
    functions = [
        {
            "name": "travel_weather",
            "description": "Finds the average temperature for a city in a month.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city for example Madrid",
                    },
                    "month": {
                        "type": "string",
                        "description": "The month of the year, for example June",
                    },
                },
                "required": ["city", "month"],
            },
        }
    ]
    context = kernel.create_new_context()

    context.variables["user_input"] = "What is the average temperature in Seattle in June?"
    context = await chat_function.invoke_async(context=context, functions=functions)
    
    if context.error_occurred:
        print(f"Error occurred: {context.last_error_description}")
        return

    chat_function._chat_prompt_template.messages.append({"role": "assistant", "content": "It is 85 degrees in Seattle in June"})
    context = await chat_function.invoke_async(context=context, functions=functions)
    print("No function was called")
    print(f"Output was: {str(context)}")


# Run the main function
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
