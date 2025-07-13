# Portfólio do Curso: Operacionalização de LLMs no Azure (Duke University)

Este repositório documenta a minha jornada de aprendizagem na especialização em LLMOps da Duke University, oferecida pela Coursera. Ele contém tanto o material original dos laboratórios quanto as minhas próprias implementações, construídas do zero com as práticas e bibliotecas mais modernas.

## Estrutura do Repositório

O projeto está organizado em duas pastas principais para mostrar a evolução do aprendizado:

-   **/old_lab_code**: Contém o código original e desatualizado fornecido pelos laboratórios do curso.
-   **/new_modern_code**: Contém as minhas próprias implementações, construídas do zero e totalmente funcionais, utilizando as versões mais recentes do **Python**, **Semantic Kernel** e do **SDK do Azure OpenAI**.

---

## Guia de Iniciação Rápida (para o Projeto Moderno)

Estas instruções são para configurar e executar o projeto localizado na pasta `new_modern_code`.

### 1. Pré-requisitos

-   Python 3.10+
-   Uma subscrição do Azure com acesso ao Azure OpenAI Service.
-   Um recurso do Azure OpenAI com um modelo implementado (ex: `gpt-4` ou `gpt-4o`).

### 2. Instalação do Ambiente

Execute os seguintes comandos no seu terminal para preparar o ambiente.

#### a. Crie um Ambiente Virtual

É uma boa prática isolar as dependências de cada projeto. Na raiz da pasta `new_modern_code`, execute:
```bash
python -m venv .venv
```

#### b. Ative o Ambiente Virtual

**No Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**No macOS/Linux (bash):**
```bash
source .venv/bin/activate
```

#### c. Instale as Dependências

Crie um ficheiro `requirements.txt` com o seguinte conteúdo:
```
semantic-kernel
python-dotenv
```
Em seguida, instale as bibliotecas com o `pip`:
```bash
pip install -r requirements.txt
```

### 3. Configuração das Credenciais

Para que o código se conecte ao Azure, ele precisa das suas credenciais.

1.  Crie um ficheiro chamado **`.env`** na raiz da pasta `new_modern_code`.
2.  Adicione o seguinte conteúdo, substituindo pelos seus valores do Portal do Azure:

```
# Credenciais do Azure OpenAI
AZURE_OPENAI_API_KEY="COLE_A_SUA_CHAVE_AQUI"
AZURE_OPENAI_ENDPOINT="COLE_O_SEU_ENDPOINT_AQUI"
AZURE_OPENAI_DEPLOYMENT_NAME="NOME_DA_SUA_IMPLANTAÇÃO"
```

### 4. Execução do Projeto

Com o ambiente ativo e o ficheiro `.env` configurado, você pode executar a aplicação principal:

```bash
python main.py 
```
*(ou o nome que você deu ao seu ficheiro principal, como `multi_agent_with_plugins.py`)*