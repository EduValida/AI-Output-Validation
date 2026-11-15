import json

def filtrar(dados, palavra, campo=None):

    palavra = palavra.lower()
    correto, incorreto = [], []
    parcial = []

    for item in dados:
        
        texto = str(item.get(campo, "")).lower().strip()

        if texto.startswith(palavra):
            correto.append(item)
        elif texto.startswith("parcial"):
            parcial.append(item)
        else:
            incorreto.append(item)

    return correto, incorreto, parcial


