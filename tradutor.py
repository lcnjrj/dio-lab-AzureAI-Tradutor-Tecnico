import os
import re
import logging
from openai import AzureOpenAI

# ... (Configurações de logging e ambiente permanecem as mesmas)

def detectar_formato(texto):
    """
    Analisa o texto em busca de padrões comuns de Markdown.
    Retorna 'markdown' ou 'text'.
    """
    # Padrões: Títulos (#), Bold (**), Links ([]()), Blocos de código (```)
    patterns = [
        r'^#\s+',           # Headers
        r'\*\*.*?\*\*',     # Bold
        r'\[.*?\]\(.*?\)',  # Links
        r'```.*?```',       # Code blocks
        r'^-\s+',           # Lists
    ]
    
    # Se encontrar qualquer padrão em qualquer linha, assume Markdown
    for pattern in patterns:
        if re.search(pattern, texto, re.MULTILINE | re.DOTALL):
            return "markdown"
    return "text"

def traduzir_conteudo(texto, idioma_destino="Português"):
    # --- CAMADA DE INTELIGÊNCIA ---
    formato = detectar_formato(texto)
    logger.info(f"🔍 Formato detectado: {formato.upper()}")

    # Ajuste dinâmico do System Prompt
    if formato == "markdown":
        system_prompt = (
            f"Você é um tradutor técnico especializado em Markdown. "
            f"Traduza para {idioma_destino} preservando rigorosamente todas as tags (#, **, links, blocos de código). "
            "Não traduza termos técnicos estáveis em inglês."
        )
    else:
        system_prompt = (
            f"Você é um tradutor técnico especializado. "
            f"Traduza o texto plano para {idioma_destino} mantendo a clareza. "
            "Preserve a terminologia técnica padrão da indústria."
        )

    # --- LÓGICA DE TRADUÇÃO (CHUNKING) ---
    # (Mantemos a lógica de chunking anterior para garantir escalabilidade)
    # ... 
    
    # Exemplo simplificado da chamada:
    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": texto}
            ],
            temperature=0.1
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Erro: {e}")
        return None
