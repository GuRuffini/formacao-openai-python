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

modelo = "gpt-4o"
codificador = tiktoken.encoding_for_model(modelo)
lista_tokens = codificador.encode("Você é um categorizador de produtos.")

print("Lista de Tokens: ", lista_tokens)
print("Quantos tokens temos: ", len(lista_tokens))
custo_usd = (len(lista_tokens) / 1000000) * 2.50
custo_brl = custo_usd * TAXA_CAMBIO
print(f"Custo para o modelo {modelo} é de ${custo_usd:.8f} (R${custo_brl:.8f})")

modelo = "gpt-4o-mini"
codificador = tiktoken.encoding_for_model(modelo)
lista_tokens = codificador.encode("Você é um categorizador de produtos.")

print("Lista de Tokens: ", lista_tokens)
print("Quantos tokens temos: ", len(lista_tokens))
custo_usd = (len(lista_tokens) / 1000000) * 0.15
custo_brl = custo_usd * TAXA_CAMBIO
print(f"Custo para o modelo {modelo} é de ${custo_usd:.8f} (R${custo_brl:.8f})")
