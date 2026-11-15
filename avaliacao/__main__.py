"""
    python -m avaliacao
    python -m avaliacao entradas/output7_Gemma4.json
    python -m avaliacao entradas/glm4/redes.json --saida resultados_glm4
"""

import argparse
import sys
from pathlib import Path

from .entrada import EntradaInvalida, ler_itens
from .pipeline import executar
from .saida import escrever_csv, linha_resumo, salvar_execucao

PASTA_PADRAO = "entradas"


def _fmt(valor, casas: int = 3) -> str:
    if valor is None or valor == "":
        return "-"
    return f"{valor:.{casas}f}" if isinstance(valor, float) else str(valor)


def _imprimir(linha: dict) -> None:
    print(f"[{linha['status']}] {linha['execucao']}: itens={_fmt(linha['n_itens'])} "
          f"competências={_fmt(linha['n_competencias'])} média={_fmt(linha['media_cobertura_pct'], 1)}% "
          f"acc={_fmt(linha['acuracia'])} prec={_fmt(linha['precisao'])} "
          f"rec={_fmt(linha['recall'])} f1={_fmt(linha['f1'])}")
    if linha["avisos"]:
        print(f"    ! {linha['avisos']}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m avaliacao",
                                 description="Pipeline de avaliação das saídas dos modelos")
    ap.add_argument("entrada", nargs="?", default=PASTA_PADRAO,
                    help=f"arquivo .json ou pasta com .json, busca recursiva (padrão: {PASTA_PADRAO})")
    ap.add_argument("--saida", default="resultados", help="pasta de saída (padrão: resultados)")
    args = ap.parse_args(argv)

    entrada = Path(args.entrada).resolve()
    saida = Path(args.saida).resolve()

    if not entrada.exists() and args.entrada == PASTA_PADRAO:
        entrada.mkdir(parents=True)
        print(f"Criei a pasta '{PASTA_PADRAO}/' em {entrada.parent}.\n"
              "Coloque nela os .json dos modelos e rode o comando de novo.")
        return 1

    if entrada.is_dir():
        base_dir = entrada
        arquivos = sorted(p for p in entrada.rglob("*.json") if saida not in p.parents)
    elif entrada.is_file():
        base_dir = entrada.parent
        arquivos = [entrada]
    else:
        print(f"Entrada não encontrada: {entrada}")
        return 1

    if not arquivos:
        print(f"Nenhum .json encontrado em {entrada}")
        return 1

    saida.mkdir(parents=True, exist_ok=True)
    linhas = []

    for arquivo in arquivos:
        execucao = arquivo.relative_to(base_dir).with_suffix("").as_posix()
        try:
            itens = ler_itens(arquivo)
        except EntradaInvalida as e:
            linha = linha_resumo(execucao, erro=f"entrada inválida: {e}")
        else:
            try:
                resultado = executar(itens)
            except EntradaInvalida as e:
                linha = linha_resumo(execucao, n_itens=len(itens), erro=str(e))
            else:
                linha = linha_resumo(execucao, resultado)
                salvar_execucao(saida / execucao, resultado, linha)
        linhas.append(linha)
        _imprimir(linha)

    csv_path = saida / "resumo_geral.csv"
    escrever_csv(csv_path, linhas)
    print(f"\n{len(linhas)} execução(ões). Resultados em {saida}")
    print(f"Resumo comparativo: {csv_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
