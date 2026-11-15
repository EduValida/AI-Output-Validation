import json

def separate(dados):

    True_positive = 0
    False_positive = 0
    False_negative = 0
    True_negative = 0
    pos_indirect, neg_indirect = 0, 0

    if isinstance(dados, dict):
        items = [item for lista in dados.values() for item in lista]
    else:
        items = dados

    for item in items:

        predicted = str(item.get("nivel", "")).lower().strip()
        actual = str(item.get("avaliação", "")).lower().strip()

        if not predicted.startswith("ausente"):
            if actual.startswith("incorreto"):
                False_positive += 1
                if predicted.startswith("indireto"):
                    neg_indirect += 1
                
            else:
                True_positive +=1
                if predicted.startswith("indireto"):
                    pos_indirect += 1

        else:
            if actual.startswith("incorreto"):
                False_negative += 1 
            else:
                True_negative += 1

    return True_positive, False_positive, False_negative, True_negative, pos_indirect, neg_indirect


def matriz_confusao(tp, fp, fn, tn, pi, ni):
    
    return [[tp - pi, fp - ni],
            [fn, tn],
            [pi, ni]]


def calcular_metricas(tp, fp, fn, tn):
    
    def dividir(a, b):
        return a / b if b else None

    precisao = dividir(tp, tp + fp)
    recall = dividir(tp, tp + fn)
    f1 = None
    if precisao is not None and recall is not None:
        f1 = dividir(2 * precisao * recall, precisao + recall)
    return {
        "acuracia": dividir(tp + tn, tp + fp + fn + tn),
        "precisao": precisao,
        "recall": recall,
        "f1": f1,
    }


