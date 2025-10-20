# Desafio 1 – Extração de Anúncios do Google

Este módulo implementa a automação solicitada para extrair **anúncios do
Google Shopping**. A solução foi desenvolvida em Python com foco em
modularidade, documentação e resiliência em ambientes sem acesso à
internet.

## Visão Geral

O objetivo é automatizar a pesquisa de um termo (por exemplo, “geladeira”)
no Google e coletar os 20 primeiros anúncios exibidos. Para cada
anúncio são extraídos:

* Título do produto
* Preço anunciado
* URL do produto (link para a loja)
* Nome da loja
* URL da imagem do produto

Em seguida, os dados são salvos em um arquivo CSV, as imagens são
baixadas localmente e os resultados são ordenados do mais barato ao
mais caro para exibição no console.

## Arquivos e Funções

### `main.py`

Ponto de entrada para a automação. Realiza as seguintes etapas:

1. Lê o termo de pesquisa da linha de comando (ou usa “geladeira” como padrão).
2. Usa `scraper.fetch_ads` para obter a lista de anúncios (via SerpApi ou dados de exemplo).
3. Salva os dados em `anuncios.csv` com `storage.save_to_csv`.
4. Baixa as imagens usando `download_images.download_images`.
5. Lê o CSV salvo, ordena por preço crescente via `storage.load_and_sort_by_price`.
6. Imprime os 20 itens mais baratos no console.
7. Salva o resultado ordenado em `anuncios_ordenados.csv`.

### `scraper.py`

Responsável por buscar os anúncios. Tenta utilizar a [SerpApi](https://serpapi.com) quando uma
chave válida (`SERPAPI_KEY`) está disponível. Caso contrário ou se houver
qualquer falha de conexão, retorna uma lista de anúncios simulados
contendo 25 itens repetidos. Esta abordagem garante que a estrutura da
automação possa ser testada sem dependências externas.

Função principal: `fetch_ads(term: str, api_key: Optional[str] = None) -> List[Dict[str,str]]`.

### `storage.py`

Concentra as operações de armazenamento e ordenação:

* `save_to_csv(items, filepath)` – grava a lista de anúncios em CSV.
* `load_and_sort_by_price(filepath)` – carrega um CSV de anúncios, converte o
  preço para número e devolve uma lista ordenada do mais barato para o mais
  caro.

### `download_images.py`

Contém a função `download_images(items, directory="imagens")`, que itera
sobre a lista de anúncios e baixa cada imagem para o diretório
especificado. Se a URL não estiver presente ou a requisição falhar
(por exemplo, falta de internet), cria um arquivo em branco para que o
processo continue sem erros.

## Executando a automação

Execute o script principal informando o termo de busca como argumento:

```bash
python main.py "geladeira"
```

Caso nenhum termo seja passado, o padrão é `"geladeira"`. O resultado
completo é salvo em `anuncios.csv`, as imagens são baixadas para a pasta
`imagens/` e o resultado ordenado é salvo em `anuncios_ordenados.csv`.

## Chave de API opcional

Se você possui uma chave válida da SerpApi, defina a variável de
ambiente `SERPAPI_KEY` (por exemplo, em um arquivo `.env`) para que a
automação busque dados reais do Google Shopping. Em ambientes sem
conexão ou sem chave, o script utilizará os dados simulados do
`scraper.py`.
## Por que Requests, Pandas e SerpApi?

Ao escolher as bibliotecas desta automação, buscamos ferramentas simples
e robustas que facilitassem a escrita de um código resiliente. A
biblioteca **Requests** é usada para baixar as imagens e consumir
APIs opcionais. Conforme a documentação oficial, Requests é “uma
biblioteca HTTP elegante e simples, construída para seres humanos”,
oferecendo uma API intuitiva para enviar requisições sem a necessidade
de lidar com detalhes de baixo nível. A simplicidade da API se
traduz em código mais legível e fácil de manter.

A gravação e leitura de dados são feitas com **Pandas**, que oferece
uma interface rica para lidar com dados tabulares e exportá‑los para
CSV com poucas linhas de código. Embora seja possível usar o módulo
`csv` da biblioteca padrão, Pandas simplifica a conversão de tipos e a
ordenação dos preços numéricos com métodos como `to_csv()` e
`sort_values()`, resultando em um código conciso. Além disso, o módulo
`python‑dotenv` é utilizado para ler variáveis de ambiente (como a
chave da SerpApi) de um arquivo `.env`, evitando expor credenciais no
código.

A solução oferece suporte opcional à **SerpApi**, que realiza as
requisições ao Google Shopping via API quando disponível. Em ambientes
sem conexão ou sem chave válida, o `scraper.py` gera dados de
exemplo, permitindo validar o fluxo da automação mesmo offline. Essa
abordagem modulariza a dependência externa e garante que o desafio
possa ser testado em qualquer ambiente.
