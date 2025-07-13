import os
import asyncio
from openai import AzureOpenAI
from dotenv import load_dotenv

async def main():
    # 1. Carrega as credenciais do seu arquivo .env
    load_dotenv()
    
    subscription_key = os.environ.get("AZURE_OPENAI_API_KEY")
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
    api_version = "2024-02-15-preview" # Exemplo, pode ser ajustado

    # 2. Inicializa o cliente do Azure OpenAI
    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=subscription_key,
    )

    # 3. Cria a mensagem e envia para a IA
    print("Enviando uma requisição de chat...")
    
    response = client.chat.completions.create(
        model=deployment, # O nome da sua implantação, ex: "gpt-4"
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": "I am going to Paris, what should I see?",
            }
        ],
    )

    # 4. Imprime a resposta da IA
    print("\nResposta do Assistente:")
    print(response.choices[0].message.content)

# Executa a função principal
if __name__ == "__main__":
    asyncio.run(main())