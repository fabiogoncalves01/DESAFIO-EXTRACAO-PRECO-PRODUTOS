"""
Módulo `storage.py` — utilitários de armazenamento e ordenação.

Este módulo fornece funções para salvar uma lista de anúncios em um
arquivo CSV e para carregar e ordenar esses anúncios por preço.

Funções:

* `save_to_csv(items, filepath)`: salva a lista de dicionários em
  formato CSV usando pandas.
* `load_and_sort_by_price(filepath)`: lê o arquivo CSV, converte o
  preço de string para número e devolve uma lista ordenada do mais
  barato para o mais caro.
"""

from __future__ import annotations

import pandas as pd
import re
from typing import List, Dict


def save_to_csv(items: List[Dict[str, str]], filepath: str) -> None:
    """Salva uma lista de anúncios em um arquivo CSV.

    Args:
        items: lista de dicionários com chaves `titulo`, `preco`,
            `url`, `loja` e `imagem`.
        filepath: caminho do arquivo CSV a ser criado.
    """
    if not items:
        raise ValueError("A lista de itens está vazia; nada a salvar.")
    df = pd.DataFrame(items)
    df.to_csv(filepath, index=False, encoding="utf-8")


def _price_to_float(preco: str) -> float:
    """Converte preço em formato brasileiro para float.

    Remove `R$`, espaços e pontos, substitui vírgula por ponto e pega
    o primeiro número encontrado. Se não houver número, devolve +inf para
    garantir que itens sem preço fiquem no fim da lista ao ordenar.
    """
    if not preco or not isinstance(preco, str):
        return float("inf")
    text = preco.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
    m = re.search(r"\d+(?:\.\d+)?", text)
    return float(m.group(0)) if m else float("inf")


def load_and_sort_by_price(filepath: str) -> List[Dict[str, str]]:
    """Lê o CSV salvo e retorna uma lista ordenada pelo preço (ascendente).

    Args:
        filepath: caminho do arquivo CSV previamente salvo por
            `save_to_csv`.

    Returns:
        Uma lista de dicionários ordenada do item mais barato para o mais
        caro.
    """
    df = pd.read_csv(filepath)
    # cria uma coluna auxiliar com o preço numérico
    df["preco_num"] = df["preco"].apply(_price_to_float)
    df_sorted = df.sort_values("preco_num", ascending=True)
    # elimina a coluna auxiliar antes de devolver
    df_sorted = df_sorted.drop(columns=["preco_num"])
    return df_sorted.to_dict(orient="records")
