from dotenv import load_dotenv
from openai import OpenAI
import json
import pdfplumber
import time

load_dotenv()


Modelo = "gpt-6.1-sol"
reasoning_effort = "low"
input_price = 2
output_price = 10

system_prompt = open("prompts/prompt_7.txt", encoding="utf-8").read()
roadmap = open("roadmaps/Net.json", encoding="utf-8").read()
with pdfplumber.open("pdf/Redes_de_Comunicação.pdf") as pdf:
    plano = "\n".join(p.extract_text() or "" for p in pdf.pages)


inicio = time.time()

mensagem = f"[ROADMAP]\n{roadmap}\n[/ROADMAP]\n\n[PLANO_DE_ENSINO]\n{plano}\n[/PLANO_DE_ENSINO]"
resposta = OpenAI().responses.create(model=Modelo, reasoning={"effort": reasoning_effort}, instructions=system_prompt, input=mensagem)

fim = time.time()
tempo_total = fim - inicio

texto = resposta.output_text
itens = json.loads(texto[texto.find("["): texto.rfind("]") + 1])
json.dump(itens, open("saida.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)


usage = resposta.usage
input_tokens = usage.input_tokens
output_tokens = usage.output_tokens
total_tokens = usage.total_tokens

custo_input = (input_tokens / 1_000_000) * input_price
custo_output = (output_tokens / 1_000_000) * output_price
custo_total = custo_input + custo_output

print(f"Input Tokens: {input_tokens}")
print(f"Output Tokens: {output_tokens}")
print(f"Total tokens: {total_tokens}")
print(f"Cost: ${custo_total:.6f} USD")
print(f"Time: {tempo_total}")
