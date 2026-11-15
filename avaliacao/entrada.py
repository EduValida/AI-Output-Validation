import json
from pathlib import Path

from .config import CAMPO_AVALIACAO, CHAVES_OBRIGATORIAS, PREFIXOS_AVALIACAO


class EntradaInvalida(ValueError):
    """Entrada fora do formato esperado (numa API, seria um HTTP 422)."""


def como_lista(dados) -> list[dict]:
    
    if isinstance(dados, dict):
        try:
            dados = [item for lista in dados.values() for item in lista]
        except TypeError:
            raise EntradaInvalida("os valores do objeto JSON deveriam ser listas de itens") from None
    if not isinstance(dados, list) or not all(isinstance(i, dict) for i in dados):
        raise EntradaInvalida("esperado uma lista de objetos JSON")
    if not dados:
        raise EntradaInvalida("arquivo sem itens")
    return dados


def ler_itens(caminho: Path) -> list[dict]:
    try:
        with open(caminho, encoding="utf-8") as f:
            dados = json.load(f)
    except json.JSONDecodeError as e:
        raise EntradaInvalida(f"JSON malformado ({e})") from e
    return como_lista(dados)


def normalizar_avaliacao(itens: list[dict]) -> None:
    
    for item in itens:
        if CAMPO_AVALIACAO not in item and "avaliacao" in item:
            item[CAMPO_AVALIACAO] = item["avaliacao"]


def validar_estrutura(itens: list[dict]) -> None:
    
    problemas = [
        f"item {i}: faltam as chaves {[c for c in CHAVES_OBRIGATORIAS if c not in item]}"
        for i, item in enumerate(itens)
        if any(c not in item for c in CHAVES_OBRIGATORIAS)
    ]
    if problemas:
        resto = f" (+{len(problemas) - 3} outros)" if len(problemas) > 3 else ""
        raise EntradaInvalida("; ".join(problemas[:3]) + resto)


def itens_sem_avaliacao(itens: list[dict]) -> list[str]:
    return [
        str(item.get("conhecimento", "?"))
        for item in itens
        if not str(item.get(CAMPO_AVALIACAO, "")).lower().strip().startswith(PREFIXOS_AVALIACAO)
    ]
