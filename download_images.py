"""
Módulo `download_images.py` — download de imagens de produtos.

Contém a função `download_images`, que recebe a lista de anúncios e
baixa cada imagem encontrada para um diretório especificado. Quando a
requisição à imagem falha (por falta de internet ou erro HTTP), é
gerado um arquivo em branco com o nome correspondente para que a
automação continue sem interrupções.
"""

from __future__ import annotations

import os
import re
import time
from typing import List, Dict

import requests


def _slugify(name: str, maxlen: int = 60) -> str:
    """Converte uma string em um nome de arquivo seguro.

    - Substitui caracteres não alfanuméricos por `_`.
    - Limita o comprimento a `maxlen` caracteres.
    - Garante que não retorna uma string vazia.
    """
    base = re.sub(r"[^a-zA-Z0-9_-]+", "_", name).strip("_")
    base = base if base else "imagem"
    return base[:maxlen]


def download_images(items: List[Dict[str, str]], directory: str = "imagens") -> None:
    """Baixa as imagens de cada anúncio na lista.

    Args:
        items: lista de dicionários com, no mínimo, chaves `titulo` e `imagem`.
        directory: diretório onde as imagens serão salvas. Será criado se
            necessário.
    """
    os.makedirs(directory, exist_ok=True)
    for idx, item in enumerate(items, 1):
        image_url = item.get("imagem") or ""
        title = item.get("titulo") or f"produto_{idx}"
        filename = f"{_slugify(title)}.jpg"
        filepath = os.path.join(directory, filename)

        if not image_url:
            # Não há URL; cria arquivo vazio como placeholder
            open(filepath, "wb").close()
            continue

        try:
            resp = requests.get(image_url, timeout=15)
            resp.raise_for_status()
            with open(filepath, "wb") as f:
                f.write(resp.content)
            # Pequena pausa para não sobrecarregar rede ou serviços
            time.sleep(0.05)
        except Exception as exc:
            # Se falhar (por exemplo, ambiente sem internet), cria um arquivo vazio
            open(filepath, "wb").close()
