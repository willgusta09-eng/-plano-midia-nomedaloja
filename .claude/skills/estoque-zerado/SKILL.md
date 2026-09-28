---
name: estoque-zerado
description: Verifica em todas as lojas (Mercado Livre, Shopee, TikTok Shop) os produtos e variações com estoque igual a 0 e envia a lista por email. Use todo dia ou quando o usuário pedir produtos sem estoque / estoque zerado.
---

# Estoque zerado — todas as lojas

Contas e parâmetros: ver tabela em `CLAUDE.md`. Percorra **todas** as contas. Esta tarefa é **somente leitura**: não pause, não reative e não altere estoque de nada.

## 1. Coletar

Considere anúncios **ativos** e também os **pausados por falta de estoque** (ignore os encerrados/excluídos). Verifique **cada variação** — um anúncio com uma cor zerada entra na lista com a variação indicada.

- **Mercado Livre**: `list_items` (status active e paused) → para anúncios com variações use `ml_list_item_variations`. Registre o `logistic_type` (FULL = estoque no armazém do ML).
- **Shopee** (4 lojas): `shopee_list_items` / `shopee_get_items_batch` → para itens com variações `shopee_get_models`.
- **TikTok Shop** (2 lojas): `tiktok_search_products` e `tiktok_search_inventory`.

Use `list_actions` / `describe_action` se algum parâmetro não estiver claro. Pagine até o fim — não pare na primeira página.

## 2. Montar a lista

Uma linha por anúncio/variação com estoque 0: Marketplace | Loja | ID do anúncio | Título | Variação | SKU | Status | Logística (ML) | Vendas últimos 30 dias (se disponível).

Ordene por vendas dos últimos 30 dias (os que vendiam mais primeiro — são os que mais custam ficar sem estoque). Marque como **NOVO** o que não estava zerado no email do dia anterior: tente buscar no Gmail o último email `Estoque zerado` para comparar. O conector Gmail pode não ter permissão de leitura — se a busca falhar, **não trave**: omita a marcação NOVO e diga no email "comparação com ontem indisponível".

## 3. Planilha (sempre)

Gere um arquivo **`Estoque zerado AAAA-MM-DD.xlsx`** com a skill `xlsx` (openpyxl), mesmo que a lista seja curta:

- Aba **Itens zerados** — uma linha por anúncio/variação: `Novo | Marketplace | Loja | ID do anúncio | Título | Variação | SKU | Status | Logística | Vendas 30d | Link do anúncio`. Novos primeiro, depois por vendas 30d.
- Aba **Resumo por loja** — `Marketplace | Loja | Itens zerados | Novos`, com linha TOTAL (`=SUM`).
- Aba **SKU em várias lojas** — `SKU | Título | Lojas zeradas | Qtd lojas`.
- Cabeçalho em negrito com fundo cinza claro, congelado (`freeze_panes = "A2"`), filtro automático, colunas com largura ajustada. IDs e SKUs como **texto** (para não virarem notação científica); vendas como número.

## 4. Enviar por email

Envie com `send_message` do conector Gmail para `willgusta09@gmail.com`, assunto `Estoque zerado AAAA-MM-DD — X itens (Y novos)`, **com a planilha anexada**: campo `attachments` com `filename` = nome do arquivo, `mimeType` = `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` e `content` = o arquivo em base64 (`base64 -w0 arquivo.xlsx`). Confira na resposta que o envio foi feito; se o anexo falhar, tente de novo uma vez e, se ainda falhar, envie sem anexo dizendo isso no corpo.

Corpo (HTML curto em `htmlBody`):
1. Resumo por loja (quantidade de itens zerados e novos).
2. Os 20 itens mais importantes (novos primeiro, depois por vendas 30d) — "lista completa na planilha anexa".
3. SKUs zerados em mais de uma loja.
4. Contas que falharam na consulta, se houver.

Se **nenhum** item estiver zerado, envie um email curto confirmando "nenhum produto com estoque 0" (sem anexo).
