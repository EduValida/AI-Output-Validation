import csv
import json
from pathlib import Path

CAMPOS_CSV = [
    "execucao", "status", "n_itens", "n_competencias", "media_cobertura_pct",
    "media_ponderada","TP", "FP", "FN", "TN", "acuracia", "precisao", "recall",
    "f1", "avisos",
]


def salvar_json(caminho: Path, dados) -> None:
    caminho.write_text(json.dumps(dados, indent=2, ensure_ascii=False), encoding="utf-8")


def linha_resumo(execucao: str, resultado: dict | None = None,
                 n_itens="", erro: str = "") -> dict:
    linha = {campo: "" for campo in CAMPOS_CSV}
    linha["execucao"] = execucao

    if resultado is None:
        linha.update(status="erro", n_itens=n_itens, avisos=erro)
        return linha

    linha.update(
        status=resultado["status"],
        n_itens=resultado["n_itens"],
        n_competencias=resultado["n_competencias"],
        media_cobertura_pct=resultado["media_cobertura_pct"],
        media_ponderada=resultado["media_ponderada"],
        avisos=" | ".join(resultado["avisos"]),
    )
    matriz = resultado["confusion_matrix"]
    if matriz:
        contagens = matriz["contagens"]
        linha.update(
            TP=contagens["TP"], FP=contagens["FP"], FN=contagens["FN"], TN=contagens["TN"],
            **matriz["metricas"],
        )
    return linha


def salvar_execucao(pasta: Path, resultado: dict, linha: dict) -> None:
    
    pasta.mkdir(parents=True, exist_ok=True)
    salvar_json(pasta / "agrupado.json", resultado["agrupado"])
    if resultado["correto_incorreto"] is not None:
        salvar_json(pasta / "correto_incorreto.json", resultado["correto_incorreto"])
    if resultado["confusion_matrix"] is not None:
        salvar_json(pasta / "confusion_matrix.json", resultado["confusion_matrix"])
    salvar_json(pasta / "resumo.json", {k: v for k, v in linha.items() if v != ""})


def escrever_csv(caminho: Path, linhas: list[dict]) -> None:
    
    with open(caminho, "w", newline="", encoding="utf-8-sig") as f:
        escritor = csv.DictWriter(f, fieldnames=CAMPOS_CSV)
        escritor.writeheader()
        escritor.writerows(linhas)
