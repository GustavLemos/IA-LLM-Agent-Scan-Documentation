import os
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Função para carregar as regras de RPA a partir de um arquivo
def carregar_regras_rapa(caminho_regras):
    with open(caminho_regras, 'r', encoding='utf-8') as file:
        regras = file.read()
    return regras

# Função para gerar o relatório baseado na documentação e nas regras
def gerar_relatorio(documentacao, regras, model, prompt):
    context = f"As regras de RPA são: {regras}\n"
    context += f"A documentação da automação é: {documentacao}\n"

    # Gerar o relatório com base na documentação e nas regras
    chain = prompt | model
    result = chain.invoke({"context": context, "question": "A automação está em conformidade com as melhores práticas? Existem débitos técnicos?"})
    return result

# Função principal para processar os arquivos de documentação
def analisar_documentacoes(regras_rpa, pasta_docs, model, prompt):
    # Ler as regras do arquivo
    regras = carregar_regras_rapa(regras_rpa)

    # Verificar todos os arquivos na pasta de documentações
    for doc_name in os.listdir(pasta_docs):
        if doc_name.endswith(".txt"):
            caminho_doc = os.path.join(pasta_docs, doc_name)
            
            with open(caminho_doc, 'r', encoding='utf-8') as file:
                documentacao = file.read()
            
            # Gerar o relatório para a documentação atual
            relatorio = gerar_relatorio(documentacao, regras, model, prompt)
            
            # Salvar o relatório em um arquivo
            nome_relatorio = f"relatorio_{os.path.splitext(doc_name)[0]}.txt"
            caminho_relatorio = os.path.join(pasta_docs, nome_relatorio)
            
            with open(caminho_relatorio, 'w', encoding='utf-8') as file:
                file.write(relatorio)
            
            print(f"Relatório gerado para {doc_name}!")

if __name__ == '__main__':
    # Caminho do arquivo de regras e da pasta de documentações
    caminho_regras_rpa = 'regras_rpa.txt'
    pasta_docs = 'docs/docs rpa'
    
    # Carregar o modelo
    model = OllamaLLM(model="qwen2.5")
    prompt = ChatPromptTemplate.from_template("""
    Você é um especialista em Robotic Process Automation (RPA) e seu objetivo é analisar a documentação de uma automação para identificar possíveis débitos técnicos.

    Aqui estão as regras de RPA: {context}

    Com base nesse conteúdo, forneça um relatório indicando:
    1. Se a automação está conforme as melhores práticas.
    2. Se existem problemas que indicam débito técnico ou melhorias a serem feitas.
    3. Detalhes das áreas que precisam de atenção.

    Pergunta: {question}

    Resposta:
    """)

    # Iniciar a análise das documentações
    analisar_documentacoes(caminho_regras_rpa, pasta_docs, model, prompt)
