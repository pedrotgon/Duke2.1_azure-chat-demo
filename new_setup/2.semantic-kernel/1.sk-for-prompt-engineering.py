import asyncio
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions import KernelArguments
from dotenv import load_dotenv
import os

async def main():
    # 1. Carrega as credenciais do seu arquivo .env
    load_dotenv()
    
    # 2. Configura o Kernel e o serviço de IA do Azure
    kernel = sk.Kernel()

    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")

    kernel.add_service(
        AzureChatCompletion(
            deployment_name=deployment_name,
            endpoint=endpoint,
            api_key=api_key,
        )
    )

    # 3. Define o prompt com uma variável ({{$num_words}})
    prompt = """
    1) A robot may not injure a human being...
    2) A robot must obey orders given it by human beings...
    3) A robot must protect its own existence...

    Give me the TLDR (resumo) in exactly {{$num_words}} words.
    """

    # 4. Define os argumentos para preencher as variáveis no prompt
    arguments = KernelArguments(num_words=5)

    # 5. Invoca o prompt com os argumentos e aguarda a resposta
    print("Executando um prompt com argumentos...")
    result = await kernel.invoke_prompt(prompt, arguments=arguments)

    # 6. Imprime a resposta
    print("Resposta da IA:")
    print(result)

# Executa a função principal
if __name__ == "__main__":
    asyncio.run(main())