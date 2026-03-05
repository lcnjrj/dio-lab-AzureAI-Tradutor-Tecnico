
#  Azure AI - Tradutor Técnico

Este projeto é uma ferramenta de linha de comando (CLI) desenvolvida para traduzir artigos técnicos do inglês para o português, utilizando o **Azure OpenAI**.
O sistema foi projetado especificamente para lidar com textos, garantindo que a formatação e os blocos de código permaneçam intactos.

---

## Diferenciais Técnicos

* **Processamento em Chunks:** Divide textos longos em blocos semânticos para respeitar os limites de tokens da API.
* **Preservação de Código:** Prompt especializado que impede a tradução de sintaxe de programação (Python, JS, etc).
* **Observabilidade:** Sistema de logs em tempo real para monitorar o status do processamento.
* **Controle de Custos:** Exibe o resumo detalhado de tokens consumidos (Prompt vs. Completion) ao final de cada execução.
* **Regex (Expressões Regulares)
Usamos o módulo re para "escanear" o texto. É uma técnica clássica de Análise de Sistemas para identificar estruturas de dados sem precisar de um parser pesado.
* **Prompt Dinâmico
Em vez de um prompt "tamanho único", agora o seu código se adapta ao input.
Se for Markdown: A IA fica em "alerta máximo" para não quebrar a formatação.
Se for Texto: A IA ganha mais liberdade para focar na fluidez linguística, já que não precisa se preocupar com símbolos especiais.
---

## 🛠️ Pré-requisitos

Antes de iniciar, você precisará ter:

1. **Python 3.8+** instalado.
2. Uma conta no **Azure Portal**.
3. Um recurso do **Azure OpenAI Service** criado com um modelo (ex: GPT-3.5-Turbo ou GPT-4) implantado.

---

## ⚙️ Configuração do Ambiente

O projeto utiliza variáveis de ambiente para manter a segurança das chaves. Configure as seguintes variáveis:

| Variável | Descrição |
| --- | --- |
| `AZURE_ENDPOINT` | URL do seu recurso Azure OpenAI. |
| `AZURE_API_KEY` | Sua chave de API secreta. |
| `DEPLOYMENT_NAME` | O nome que você deu ao seu Deployment no Azure Studio. |

---

## 🧪 Passo a Passo para Testar

Siga estas etapas para validar o funcionamento no seu ambiente local:

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

```

### 2. Criar Ambiente Virtual (Recomendado)

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate

```

### 3. Instalar Dependências

```bash
pip install openai

```

### 4. Configurar Variáveis de Ambiente

No terminal (substitua pelos seus dados reais):

```bash
# Windows (PowerShell)
$env:AZURE_ENDPOINT = "https://seu-recurso.openai.azure.com/"
$env:AZURE_API_KEY = "sua_chave_aqui"
$env:DEPLOYMENT_NAME = "seu_deployment"

# Linux/Mac
export AZURE_ENDPOINT="https://seu-recurso.openai.azure.com/"
export AZURE_API_KEY="sua_chave_aqui"
export DEPLOYMENT_NAME="seu_deployment"

```

### 5. Executar o Script

```bash
python main.py

```

---

## 📊 Estrutura de Saída

Durante a execução, você verá logs detalhados no terminal:

* **INFO:** Indica o início da tradução e a quantidade de blocos (chunks) gerados.
* **✅ Bloco X traduzido:** Confirma o sucesso de cada parte do texto.
* **RESUMO FINANCEIRO:** Exibe a métrica exata de tokens para controle de uso da API.

