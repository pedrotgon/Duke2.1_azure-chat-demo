import asyncio
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions import kernel_function
from semantic_kernel.agents import ChatCompletionAgent, GroupChatOrchestration, RoundRobinGroupChatManager
from semantic_kernel.agents.runtime import InProcessRuntime
from typing import Annotated
from dotenv import load_dotenv
import os

# --- Ferramentas (Plugins) para os nossos Agentes ---
# Este é o nosso "cinto de utilidades" que daremos a um dos agentes.
class MenuPlugin:
    """Um plugin que simula as ferramentas de um restaurante."""
    @kernel_function(description="Fornece uma lista de pratos especiais do menu.")
    def get_specials(self) -> Annotated[str, "Retorna os pratos especiais do menu."]:
        return """
        Sopa Especial: Sopa de Tomate com Manjericão
        Prato Principal Especial: Salmão Grelhado com Aspargos
        """

    @kernel_function(description="Fornece o preço de um item do menu solicitado.")
    def get_item_price(
        self, menu_item: Annotated[str, "O nome do item do menu."]
    ) -> Annotated[str, "Retorna o preço do item do menu."]:
        print(f"-> Ferramenta 'get_item_price' chamada com: {menu_item}")
        return "R$ 25,00"

# ---------------------------------------------------

async def main():
    # 1. Carrega as credenciais do seu ficheiro .env
    load_dotenv()
    
    # 2. Configura o Kernel e o serviço de IA do Azure
    kernel = sk.Kernel()

    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")

    service = AzureChatCompletion(
        deployment_name=deployment_name,
        endpoint=endpoint,
        api_key=api_key,
    )
    kernel.add_service(service)

    # 3. Define a nossa equipa de agentes especialistas
    print("A apresentar a equipa de agentes...")

    # O Revisor tem o "cinto de utilidades" (plugin) com as ferramentas do menu.
    reviewer_agent = ChatCompletionAgent(
        name="Revisor",
        service=service,
        description="Um revisor crítico que verifica os factos nas respostas.",
        kernel=kernel,
        instructions="Você é um revisor crítico. O seu trabalho é verificar os factos nas respostas do escritor. Use as ferramentas disponíveis para obter informações precisas.",
        plugins=[MenuPlugin()]
    )

    # O Escritor é um especialista em linguagem, mas não tem ferramentas.
    writer_agent = ChatCompletionAgent(
        name="Escritor",
        service=service,
        description="Um escritor criativo de conteúdo para menus.", 
        kernel=kernel,
        instructions="Você é um escritor criativo de conteúdo para menus. Você cria descrições apelativas para os pratos, mas às vezes esquece-se de verificar os preços.",
        plugins=[MenuPlugin()]
    )

    # 4. Configura a Orquestra para fazer os agentes colaborarem
    group_chat = GroupChatOrchestration(
        members=[writer_agent, reviewer_agent], # A ordem importa! O Escritor começa.
        manager=RoundRobinGroupChatManager(max_rounds=5),
    )

    # 5. Define a tarefa e inicia a colaboração
    task_prompt = "Crie uma descrição para a sopa especial do dia e inclua o preço."
    print(f"\nTarefa: {task_prompt}\n")
    
    runtime = InProcessRuntime()
    runtime.start()

    # O 'invoke' inicia a conversa entre os agentes para completar a tarefa
    result = await group_chat.invoke(task=task_prompt, runtime=runtime)
    
    # Imprime o resultado final da colaboração
    print("\n--- Resultado Final da Colaboração ---")
    print(result)
    print("------------------------------------")

    await runtime.stop_when_idle()

# Executa a função principal
if __name__ == "__main__":
    asyncio.run(main())