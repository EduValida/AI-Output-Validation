import json


def media_simples(dados):

    count = 0
    sum = 0

    for item in dados:

        sum += int(item.get("nivel"))
        count += 1

    media = sum/count

    return media

