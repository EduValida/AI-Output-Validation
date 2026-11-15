import json
import sys
from pathlib import Path

NIVEIS_COBERTOS = {"presente", "indireto", "transferivel"}
NIVEL_AUSENTE = "ausente"


def normalizar_item(item: dict) -> dict:
    
    item = dict(item)  
    if "evidências" in item and "evidencias" not in item:
        item["evidencias"] = item.pop("evidências")
    item.setdefault("evidencias", "")
    item.setdefault("conhecimento", "")
    item["nivel"] = (item.get("nivel") or "").strip().lower()
    return item


def agrupar(itens: list[dict]) -> list[dict]:
   
    grupos: dict[str, dict] = {}

    for item_bruto in itens:
        item = normalizar_item(item_bruto)
        competencia = item["competencia"]

        if competencia not in grupos:
            grupos[competencia] = {
                "competencia": competencia,
                "conhecimento": [],
                "status": 0,
                "evidencias": [],
                "faltantes": [],
                "_total": 0,
                "_cobertos": 0,
            }

        grupo = grupos[competencia]
        grupo["_total"] += 1

        if item["nivel"] == NIVEL_AUSENTE:
            grupo["faltantes"].append(item["conhecimento"])
        else:
            grupo["conhecimento"].append(item["conhecimento"])
            grupo["evidencias"].append(item["evidencias"])
            if item["nivel"] in NIVEIS_COBERTOS:
                grupo["_cobertos"] += 1

    resultado = []
    for grupo in grupos.values():
        percentual = int(round(100 * grupo["_cobertos"] / grupo["_total"], 2) if grupo["_total"] else 0.0)
        resultado.append({
            "nivel": percentual,
            "competencia": grupo["competencia"],
            "status": 0,
            "conhecimento": grupo["conhecimento"],
            "evidencias": grupo["evidencias"],
            "faltantes": grupo["faltantes"],
        })

    

    return resultado

"""
def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: python agrupar_json.py entrada.json [saida.json]")
        sys.exit(1)

    caminho_entrada = Path(sys.argv[1])
    with open(caminho_entrada, encoding="utf-8") as f:
        itens = json.load(f)

    resultado = agrupar(itens)

    saida_formatada = json.dumps(resultado, indent=2, ensure_ascii=False)

    if len(sys.argv) >= 3:
        caminho_saida = Path(sys.argv[2])
        caminho_saida.write_text(saida_formatada, encoding="utf-8")
        print(f"{len(itens)} item(ns) agrupado(s) em {len(resultado)} grupo(s). "
              f"Salvo em {caminho_saida}")
    else:
        print(saida_formatada)


if __name__ == "__main__":
    main()

"""