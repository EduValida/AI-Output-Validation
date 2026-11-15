from .agrupar_json import agrupar
from .config import CAMPO_AVALIACAO, NIVEIS_CONHECIDOS, DICIONARIO
from .confusion_matrix import calcular_metricas, matriz_confusao, separate
from .correto_incorreto import filtrar
from .entrada import (
    itens_sem_avaliacao,
    normalizar_avaliacao,
    validar_estrutura,
)
from .simples import media_simples
from .ponderada import media_ponderada
from .at_status import atualizar


def _arred(valor, casas: int = 4):
    return None if valor is None else round(valor, casas)


def executar(itens: list[dict]) -> dict:
    
    itens = [dict(item) for item in itens]
    normalizar_avaliacao(itens)
    validar_estrutura(itens)

    avisos: list[str] = []
    desconhecidos = sorted({str(i["nivel"]).strip().lower() for i in itens} - NIVEIS_CONHECIDOS)
    if desconhecidos:
        avisos.append(f"níveis fora do esperado {desconhecidos}")

    agrupado = agrupar(itens)
    agrupado = atualizar(agrupado, DICIONARIO)
    resultado = {
        "status": "completo",
        "n_itens": len(itens),
        "n_competencias": len(agrupado),
        "media_cobertura_pct": _arred(media_simples(agrupado), 2),
        "media_ponderada": _arred(media_ponderada(agrupado, DICIONARIO), 2),
        "agrupado": agrupado,
        "correto_incorreto": None,
        "confusion_matrix": None,
        "avisos": avisos,
    }


    sem_avaliacao = itens_sem_avaliacao(itens)
    if sem_avaliacao:
        resultado["status"] = "sem_avaliacao"
        avisos.append(
            f"{len(sem_avaliacao)} de {len(itens)} itens sem 'avaliação' válida "
            f"(ex.: {sem_avaliacao[:3]}); correto_incorreto e matriz não foram gerados"
        )
        return resultado

    correto, incorreto, parcial = filtrar(itens, "correto", CAMPO_AVALIACAO)
    resultado["correto_incorreto"] = {"correto": correto, "parciais": parcial, "incorreto": incorreto}

    tp, fp, fn, tn, pi, ni = separate(resultado["correto_incorreto"])
    metricas = {nome: _arred(valor) for nome, valor in calcular_metricas(tp, fp, fn, tn).items()}
    resultado["confusion_matrix"] = {
        "contagens": {
            "TP": tp, "FP": fp, "FN": fn, "TN": tn,
            "positivos_indiretos": pi, "negativos_indiretos": ni,
        },
        "matriz": matriz_confusao(tp, fp, fn, tn, pi, ni),
        "formato_matriz": [
            "[TP sem indiretos, FP sem indiretos]",
            "[FN, TN]",
            "[positivos indiretos, negativos indiretos]",
        ],
        "metricas": metricas,
        "total_avaliado": tp + fp + fn + tn,
    }
    return resultado
