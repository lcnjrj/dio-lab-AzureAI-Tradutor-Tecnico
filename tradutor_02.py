import os
import sys
import logging
from openai import AzureOpenAI



# 1. Configuração do Logging

logging.basicConfig(

    level=logging.INFO,

    format='%(asctime)s - %(levelname)s - %(message)s',

    handlers=[logging.StreamHandler(sys.stdout)]

)

logger = logging.getLogger(__name__)



# 2. Configurações de Ambiente com Validação

def get_env_variable(name):

    value = os.getenv(name)

    if not value:

        logger.error(f"Falta configuração: {name}")

        sys.exit(1)

    return value



# o endpoint e chaves estão no .env, ou exportados no terminal

AZURE_ENDPOINT = get_env_variable("AZURE_ENDPOINT")

AZURE_API_KEY = get_env_variable("AZURE_API_KEY")

DEPLOYMENT_NAME = get_env_variable("DEPLOYMENT_NAME")



#  API 

client = AzureOpenAI(

    api_key=AZURE_API_KEY,

    api_version="2024-05-01-preview", 

    azure_endpoint=AZURE_ENDPOINT

)



# 3. Lógica de Chunking (quebrar textos longos)

def chunk_text(text, max_chars=4000):

    """Divide o texto respeitando parágrafos para manter o contexto semântico."""

    paragraphs = text.split('\n\n')

    chunks = []

    current_chunk = ""



    for p in paragraphs:

        # Se um parágrafo for gigante, ele entra como um chunk próprio

        if len(current_chunk) + len(p) < max_chars:

            current_chunk += p + "\n\n"

        else:

            if current_chunk:

                chunks.append(current_chunk.strip())

            current_chunk = p + "\n\n"

    

    if current_chunk:

        chunks.append(current_chunk.strip())

    

    return chunks



# 4. Tradução

def traduzir_markdown(texto, idioma_destino="Português"):

    chunks = chunk_text(texto)

    texto_traduzido_final = []

    usage_stats = {"prompt": 0, "completion": 0}



    logger.info(f"🚀 Iniciando tradução. Total de chunks: {len(chunks)}")



    # Prompt de sistema otimizado para manter código e links intactos

    system_prompt = (

        f"Você é um tradutor técnico especializado em ecossistema Azure e Markdown. "

        f"Traduza para {idioma_destino}. "

        "REGRAS: "

        "1. Preserve tags Markdown (#, **, links, imagens). "

        "2. NÃO traduza blocos de código (```). "

        "3. Mantenha termos técnicos como 'Batch', 'Endpoint', 'Payload', 'Polling' se fizerem mais sentido em inglês no contexto tech brasileiro. "

        "4. Saída apenas com o texto traduzido."

    )



    for i, chunk in enumerate(chunks):

        try:

            response = client.chat.completions.create(

                model=DEPLOYMENT_NAME,

                messages=[

                    {"role": "system", "content": system_prompt},

                    {"role": "user", "content": chunk}

                ],

                temperature=0.1 # Baixa temperatura = maior precisão técnica

            )



            # Logging do Consumo

            u = response.usage

            usage_stats["prompt"] += u.prompt_tokens

            usage_stats["completion"] += u.completion_tokens

            

            logger.info(f"✅ Bloco {i+1} traduzido ({u.total_tokens} tokens)")

            texto_traduzido_final.append(response.choices[0].message.content)



        except Exception as e:

            logger.error(f"❌ Falha no bloco {i+1}: {str(e)}")

            continue



    print("\n" + "="*30)

    logger.info(f"RESUMO FINANCEIRO: Prompt {usage_stats['prompt']} | Comp {usage_stats['completion']} tokens.")

    print("="*30 + "\n")



    return "\n\n".join(texto_traduzido_final)



if __name__ == "__main__":

    # Texto de exemplo 

    artigo_input = """

# Translating documents with Azure AI Translator's synchronous API



The Azure AI Translator service offers two approaches for document translation: asynchronous batch processing and synchronous single-document translation. While the asynchronous approach is well-documented and widely used for large-scale operations, the synchronous API for single documents is a powerful yet underutilized feature that deserves more attention.

In this guide, I will talk a bit more on when to use the synchronous API and show you how you can implement it in your applications.

What is synchronous document translation?
The synchronous document translation API allows you to translate a single document in real-time without requiring Azure Blob Storage. Unlike the asynchronous batch translation that processes multiple documents and requires storage containers, the synchronous API:

Processes one document at a time - Perfect for on-demand translations
Returns results immediately - No polling required
Requires no storage setup - The translated document is returned directly in the HTTP response
Maintains document formatting - Preserves the original layout and structure
When to use synchronous vs asynchronous translation
When To use synchronous translation when:
You need immediate results for single documents
Working with smaller files (under 10MB file size limits)
Building interactive applications where users upload and receive translated documents instantly
You want to avoid Azure Storage complexity and costs
Processing user-generated content in real-time
When to use asynchronous translation:
Translating multiple documents simultaneously
Working with large files or batch operations
Building background processing systems
You need to translate entire document collections
How to use the synchronous API
In the official documentation, you can find the details about the query parameters and the request body structure, but not a lot of examples, that is why I thought it would be useful to provide a practical example of how to use the synchronous API in a web application.

async function translateDocument(
  file,
  sourceLanguage,
  targetLanguage,
  subscriptionKey,
  endpoint
) {
  const url = new URL(`${endpoint}/translator/document:translate`);
  url.searchParams.append("targetLanguage", targetLanguage);
  if (sourceLanguage) {
    url.searchParams.append("sourceLanguage", sourceLanguage);
  }
  url.searchParams.append("api-version", "2024-05-01");

  const formData = new FormData();
  formData.append("document", file, file.name);

  try {
    const response = await fetch(url.toString(), {
      method: "POST",
      headers: {
        "Ocp-Apim-Subscription-Key": subscriptionKey,
      },
      body: formData,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Translation failed: ${response.status} ${errorText}`);
    }

    const blob = await response.blob();
    return blob;
  } catch (error) {
    console.error("Translation error:", error);
    throw error;
  }
}

// Use a file input like: <input type="file" id="fileInput" accept=".docx,.pdf,.txt,.html,.htm,.rtf,.odt,.xlsx,.pptx">
const fileInput = document.getElementById("fileInput");
if (!fileInput.files.length) {
  console.error("No file selected");
  return;
}

const file = fileInput.files[0];
const translatedBlob = await translateDocument(
  file,
  "en",
  "es",
  "YOUR_SUBSCRIPTION_KEY",
  "https://your-resource.cognitiveservices.azure.com"
);

// Create download link
const link = document.createElement("a");
link.href = URL.createObjectURL(translatedBlob);
link.download = `translated-${file.name}`;
link.click();

This example demonstrates how to use the synchronous API to translate a document selected by the user. The function translateDocument takes the file, source and target languages, subscription key, and endpoint as parameters. It constructs the request URL, prepares the form data, and sends the POST request to the Azure Translator service.

The response is returned as a Blob, which can be used to create a download link for the translated document.

Conclusion
The synchronous document translation API in Azure AI Translator is a powerful tool for real-time, single-document translations. It simplifies the translation process by eliminating the need for storage and allowing immediate results, making it ideal for interactive applications and user-generated content.





## What is synchronous document translation?

The synchronous document translation API allows you to translate a single document in real-time without requiring Azure Blob Storage.



```javascript

async function translateDocument(file, targetLanguage) {

  const url = new URL(`${endpoint}/translator/document:translate`);

  url.searchParams.append("targetLanguage", targetLanguage);

  // ... lógica de fetch

}
