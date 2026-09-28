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

Ordene por vendas dos últimos 30 dias (os que vendiam mais primeiro — são os que mais custam ficar sem estoque). Marque como **NOVO** o que não estava zerado no email do dia anterior (procure no Gmail o último email `Estoque zerado` para comparar, se existir).

## 3. Enviar por email

Para `willgusta09@gmail.com`, assunto `Estoque zerado AAAA-MM-DD — X itens (Y novos)`.

Corpo:
1. Resumo por loja (quantidade de itens zerados).
2. Tabela com os itens, novos primeiro.
3. SKUs zerados em mais de uma loja (mesmo SKU em várias contas).
4. Contas que falharam na consulta, se houver.

Se houver mais de 50 itens, coloque no corpo só os 50 primeiros e anexe a lista completa em planilha (skill `xlsx`).

Se **nenhum** item estiver zerado, envie mesmo assim um email curto confirmando "nenhum produto com estoque 0".
