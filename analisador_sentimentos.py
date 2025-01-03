from openai import OpenAI
from dotenv import load_dotenv
import os
import openai

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4o-mini"


def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r", encoding="utf-8") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro ao carregar arquivo: {e}")
        return None


def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")


def analisador_sentimentos(produto):
    prompt_sistema = f"""
        Você é um analisador de sentimentos de avaliações de produtos.
        Escreva um parágrafo com até 50 palavras resumindo as avaliações e 
        depois atribua qual o sentimento geral para o produto.
        Identifique também 3 pontos fortes e 3 pontos fracos identificados a partir das avaliações.

        # Formato de Saída

        Nome do Produto:
        Resumo das Avaliações:
        Sentimento Geral: [utilize aqui apenas Positivo, Negativo ou Neutro]
        Pontos fortes: lista com três bullets
        Pontos fracos: lista com três bullets
    """

    prompt_usuario = carrega(f"./dados/avaliacoes-{produto}.txt")
    if not prompt_usuario:
        print(f"Arquivo de avaliações para o produto '{produto}' não encontrado ou vazio.")
        return

    print(f"Iniciou a análise de sentimentos do produto {produto}")

    lista_mensagens = [
        {
            "role": "system",
            "content": prompt_sistema
        },
        {
            "role": "user",
            "content": prompt_usuario
        }
    ]

    try:
        resposta = cliente.chat.completions.create(
            messages=lista_mensagens,
            model=modelo
        )
        texto_resposta = resposta.choices[0].message.content
        salva(f"./dados/analise-{produto}.txt", texto_resposta)
        print(f"Análise concluída e salva em './dados/analise-{produto}.txt'")
    except openai.AuthenticationError as e:
        print(f"Erro de autenticação com o OpenAI: {e}")
    except openai.APIError as e:
        print(f"Erro ao processar a análise de sentimentos: {e}")
    except ValueError as e:
        print(f"Erro nos parâmetros de entrada: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


lista_de_produtos = ["Camisetas de algodão orgânico", "Jeans feitos com materiais reciclados", "Maquiagem mineral"]

for um_produto in lista_de_produtos:
    analisador_sentimentos(um_produto)

