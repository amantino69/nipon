import os
import openai

openai.api_key = os.getenv("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")

# Abre o arquivo para leitura
with open("C:/Workspace/nipon1/app/models.py", "r") as arquivo:
    codigo = arquivo.read()

# Corrige o código com a API da OpenAI
response = openai.Completion.create(
    model="code-davinci-002",
    prompt=f"##### Fix bugs in the below function\n\n### Buggy Python\n{codigo}\n### Fixed Python",
    temperature=0,
    max_tokens=182,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=["###"]
)

# Substitui o código original pelo código corrigido
codigo_corrigido = response.choices[0].text.strip()
with open("caminho/do/arquivo.py", "w") as arquivo:
    arquivo.write(codigo_corrigido)
