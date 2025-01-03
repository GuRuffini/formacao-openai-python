from openai import OpenAI
from dotenv import load_dotenv
import os
import tiktoken
from forex_python.converter import CurrencyRates

def obter_taxa_cambio():
    c = CurrencyRates()
    try:
        return c.get_rate('USD', 'BRL')
    except Exception as e:
        print(f"Erro ao obter a taxa de câmbio: {e}")
        return 6.00

TAXA_CAMBIO = obter_taxa_cambio()
print(f"Taxa de câmbio atual: 1 USD = {TAXA_CAMBIO:.2f} BRL")

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

modelo = "gpt-4o-mini"
capacidade_tokens = 4096
preco_por_milhao_tokens_entrada = 0.15
preco_por_milhao_tokens_saida = 0.60

codificador = tiktoken.encoding_for_model(modelo)

def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro: {e}")
        return ""

prompt_sistema = """
Identifique o perfil de compra para cada cliente a seguir.

O formato de saída deve ser:

cliente - descreva o perfil do cliente em 3 palavras
"""

prompt_usuario = carrega("dados/lista_de_compras_100_clientes.csv")

lista_de_tokens = codificador.encode(prompt_sistema + prompt_usuario)
numero_de_tokens_entrada = len(lista_de_tokens)
print(f"Número de tokens na entrada: {numero_de_tokens_entrada}")
tamanho_esperado_saida = 2048

if numero_de_tokens_entrada >= capacidade_tokens - tamanho_esperado_saida:
    modelo = "gpt-4"
    capacidade_tokens = 8192
    preco_por_milhao_tokens_entrada = 2.50
    preco_por_milhao_tokens_saida = 10.00
    codificador = tiktoken.encoding_for_model(modelo)

print(f"Modelo escolhido: {modelo}")

custo_entrada_usd = (numero_de_tokens_entrada / 1000000) * preco_por_milhao_tokens_entrada
custo_entrada_brl = custo_entrada_usd * TAXA_CAMBIO
print(f"Custo estimado em tokens de entrada: ${custo_entrada_usd:.8f} (R${custo_entrada_brl:.8f})")

resposta = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": prompt_sistema
        },
        {
            "role": "user",
            "content": prompt_usuario
        }
    ],
    model=modelo
)

resposta_tokens = codificador.encode(resposta.choices[0].message.content)
numero_de_tokens_saida = len(resposta_tokens)
print(f"Número de tokens na saída: {numero_de_tokens_saida}")

custo_saida_usd = (numero_de_tokens_saida / 1000000) * preco_por_milhao_tokens_saida
custo_saida_brl = custo_saida_usd * TAXA_CAMBIO
print(f"Custo estimado em tokens de saída: ${custo_saida_usd:.8f} (R${custo_saida_brl:.8f})")

custo_total_usd = custo_entrada_usd + custo_saida_usd
custo_total_brl = custo_entrada_brl + custo_saida_brl
print(f"Custo total estimado: ${custo_total_usd:.8f} (R${custo_total_brl:.8f})")

print(resposta.choices[0].message.content)
