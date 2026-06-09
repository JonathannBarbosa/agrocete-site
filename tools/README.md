# Roda Cíclica — ferramentas

A página interativa fica em `roda-ciclica.html` (na raiz e em `v2/`). Cada
projeto tem o **visual do seu site** (A = claro/verde; B = azul/cinza com padrões
de interface da plataforma), mas a mesma lógica e os mesmos dados. Pensada para
site, tablet, totem e feira (touch).

O visual de cada tema é gerado por `tools/_build_roda_html.py` (a partir da base
funcional em Downloads). Só é preciso rodá-lo se for mudar o visual; para
conteúdo, use apenas o gerador de dados abaixo.

## Atualizar o conteúdo (sem redesenhar a roda)

Toda a roda é alimentada por `roda-ciclica-data.js` (`window.RODA_DATA`), gerado
a partir da planilha **BASE DE DADOS** (modelo V10). Para atualizar:

1. Edite a planilha (abas: CULTURAS, ESTADIOS, DORES macro em CONTEUDO_DOR,
   PRODUTOS, RELACIONAMENTOS, CONTEUDO_ESTAGIO, CARD_PRODUTO, ALIASES_BUSCA).
2. Regerar os dados nos dois projetos:

   ```
   python tools/gerar_roda_data.py "caminho/para/BASE DE DADOS.xlsx"
   ```

   Sem argumento, usa `~/Downloads/BASE DE DADOS - V10.xlsx`.

Os anéis não dependem de quantidade fixa de itens: adicionar estádios, dores ou
produtos na planilha já reflete na roda após regerar.

### Nome das dores macro
A planilha V10 não traz coluna de NOME para as 10 dores macro (anel 3). Os nomes
ficam em `DOR_MACRO` dentro de `gerar_roda_data.py`. Se a aba `CONTEUDO_DOR`
ganhar uma coluna `NOME`, ela passa a ter prioridade automaticamente.

## Reconstruir o HTML (raro)

`_build_roda_html.py` monta o `roda-ciclica.html` a partir da base visual da V05
(em Downloads), reaplicando as melhorias de lógica/touch. Só é necessário se for
mudar a base visual da roda — para conteúdo, use apenas o gerador de dados acima.
