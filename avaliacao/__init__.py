"""
Pipeline de avaliação das saídas dos modelos (roadmap x plano de ensino).

Uso pela linha de comando:   python -m avaliacao entradas/
Uso como biblioteca:         from avaliacao import executar
                             resultado = executar(lista_de_itens)
"""

from .entrada import EntradaInvalida
from .pipeline import executar

__all__ = ["executar", "EntradaInvalida"]
