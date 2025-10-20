"""
Script principal para o Desafio 1 – Extração de anúncios do Google Shopping.

Como rodar:

    python main.py [termo_de_busca]

Se nenhum termo for fornecido, o padrão "geladeira" será utilizado. O
script obtém a lista de anúncios (via SerpApi ou dados simulados),
salva o resultado em CSV, baixa as imagens, ordena por preço e
imprime os 20 itens mais baratos.
"""

from __future__ import annotations

import os
import sys
from typing import List, Dict

from scraper import fetch_ads
from storage import save_to_csv, load_and_sort_by_price
from download_images import download_images


def print_top(items: List[Dict[str, str]], n: int = 20) -> None:
    """Imprime os n primeiros itens na tela, mostrando título, preço e loja."""
    for i, item in enumerate(items[:n], 1):
        titulo = item.get("titulo", "")
        preco = item.get("preco", "")
        loja = item.get("loja", "")
        print(f"{i:02d}. {titulo} — {preco} ({loja})")


def main() -> None:
    # Lê o termo de busca da linha de comando ou usa "geladeira"
    termo = " ".join(sys.argv[1:]).strip() or "geladeira"

    print(f"Buscando anúncios para: {termo!r}")
    anuncios = fetch_ads(termo)
    if not anuncios:
        print("Nenhum anúncio encontrado.")
        return

    # Salva todos os anúncios brutos
    save_to_csv(anuncios, "anuncios.csv")
    print(f"Dados brutos salvos em 'anuncios.csv'.")

    # Baixa imagens (se disponíveis)
    download_images(anuncios, directory="imagens")
    print(f"Imagens baixadas na pasta 'imagens'.")

    # Ordena por preço (crescente) e salva o resultado
    anuncios_ordenados = load_and_sort_by_price("anuncios.csv")
    save_to_csv(anuncios_ordenados, "anuncios_ordenados.csv")
    print(f"Dados ordenados salvos em 'anuncios_ordenados.csv'.")

    print("\nTop 20 produtos mais baratos:\n")
    print_top(anuncios_ordenados, n=20)


if __name__ == "__main__":
    main()