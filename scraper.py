"""
Módulo `scraper.py` — responsável por obter anúncios do Google Shopping.

Este módulo tenta utilizar a API oficial do SerpApi quando uma chave
(`SERPAPI_KEY`) é definida e existe conexão com a internet. Se a chave
não estiver presente ou a conexão falhar (por exemplo, em ambientes
isolados sem internet), um conjunto de dados de exemplo é retornado.

A função principal exposta é `fetch_ads`, que recebe um termo de
pesquisa e retorna uma lista de dicionários com os campos:

* `titulo`   – título do produto;
* `preco`    – preço em string (formato brasileiro);
* `url`      – link para o produto na loja;
* `loja`     – nome da loja anunciante;
* `imagem`   – URL da imagem do produto.

Os dados retornados por esta função serão utilizados posteriormente
para salvar em CSV, baixar imagens e ordenar por preço.

"""

from __future__ import annotations

import os
import json
import logging
from typing import List, Dict, Optional

import requests

# Configura log básico para este módulo
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Endpoint para a API do SerpApi
SERPAPI_ENDPOINT = "https://serpapi.com/search.json"

# Carrega a chave da API de variável de ambiente, caso exista
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "").strip()


def _sample_data() -> List[Dict[str, str]]:
    """Retorna uma lista de 25 anúncios simulados.

    Esses dados servem como fallback quando não é possível acessar a
    API real. Os valores são fictícios, mas seguem o formato de saída
    esperado.
    """
    exemplos = [
        {
            "titulo": "Geladeira Consul Frost Free 340 litros",
            "preco": "R$ 1.899,00",
            "url": "https://www.lojaexemplo.com/produto2",
            "loja": "Loja Exemplo 2",
            "imagem": "https://via.placeholder.com/150?text=Produto2",
        },
        {
            "titulo": "Geladeira Brastemp Frost Free Duplex 375 litros",
            "preco": "R$ 2.199,00",
            "url": "https://www.lojaexemplo.com/produto1",
            "loja": "Loja Exemplo 1",
            "imagem": "https://via.placeholder.com/150?text=Produto1",
        },
        {
            "titulo": "Geladeira Electrolux Frost Free Inverse 454 litros",
            "preco": "R$ 3.299,00",
            "url": "https://www.lojaexemplo.com/produto3",
            "loja": "Loja Exemplo 3",
            "imagem": "https://via.placeholder.com/150?text=Produto3",
        },
        {
            "titulo": "Geladeira Samsung Side by Side 501 litros",
            "preco": "R$ 4.499,00",
            "url": "https://www.lojaexemplo.com/produto4",
            "loja": "Loja Exemplo 4",
            "imagem": "https://via.placeholder.com/150?text=Produto4",
        },
        {
            "titulo": "Geladeira LG Smart Inverter 437 litros",
            "preco": "R$ 3.999,00",
            "url": "https://www.lojaexemplo.com/produto5",
            "loja": "Loja Exemplo 5",
            "imagem": "https://via.placeholder.com/150?text=Produto5",
        },
    ]
    # Repete os 5 exemplos para totalizar 25 itens (5x5)
    dados: List[Dict[str, str]] = []
    for i in range(5):
        for item in exemplos:
            # Cria uma cópia para não referenciar o mesmo dict
            dados.append(item.copy())
    return dados


def fetch_ads(term: str, api_key: Optional[str] = None) -> List[Dict[str, str]]:
    """Busca anúncios do Google Shopping via SerpApi ou retorna dados simulados.

    Args:
        term: O termo de pesquisa (produto) a ser buscado no Shopping.
        api_key: Chave de API opcional para usar a SerpApi. Se `None` ou vazia,
            tenta ler da variável de ambiente `SERPAPI_KEY`. Se mesmo assim
            estiver vazia ou ocorrer erro na chamada HTTP, dados mock são
            retornados.

    Returns:
        Uma lista de dicionários, conforme descrito no docstring do módulo.
    """
    # Determina a chave: parâmetro tem precedência sobre env
    chave = api_key or SERPAPI_KEY

    # Caso não exista chave, retorna dados simulados
    if not chave:
        logger.warning("SERPAPI_KEY ausente. Utilizando dados de exemplo.")
        return _sample_data()

    # Monta parâmetros da requisição
    params = {
        "q": term,
        "tbm": "shop",
        "gl": "br",
        "hl": "pt",
        "api_key": chave,
    }

    try:
        resp = requests.get(SERPAPI_ENDPOINT, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        results = data.get("shopping_results", [])
        anuncios: List[Dict[str, str]] = []
        for obj in results:
            titulo = obj.get("title", "")
            preco = obj.get("price") or obj.get("extracted_price") or ""
            # Converte preço numérico para string no formato brasileiro, se necessário
            preco_str: str
            if isinstance(preco, (int, float)):
                preco_str = f"R$ {preco:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            else:
                preco_str = str(preco)
            url_produto = obj.get("product_link") or obj.get("link") or ""
            loja = obj.get("source") or obj.get("merchant") or ""
            imagem = obj.get("thumbnail") or obj.get("image") or ""
            anuncios.append(
                {
                    "titulo": titulo,
                    "preco": preco_str,
                    "url": url_produto,
                    "loja": loja,
                    "imagem": imagem,
                }
            )
        if not anuncios:
            logger.warning("Nenhum resultado retornado pela API. Utilizando dados de exemplo.")
            return _sample_data()
        return anuncios
    except Exception as exc:
        # Qualquer erro (conexão, JSON inválido etc.) resulta em fallback
        logger.error("Erro ao acessar SerpApi: %s", exc)
        return _sample_data()
