---
name: devolucoes
description: Levanta todas as devoluções, reclamações e cancelamentos pendentes de todas as lojas (Mercado Livre, Shopee, TikTok Shop), recomenda a ação para cada caso e só executa após aprovação do usuário. Use nas terças e sextas ou quando o usuário pedir para "fazer as devoluções".
---

# Devoluções — todas as lojas

Contas e parâmetros: ver tabela em `CLAUDE.md`. Percorra **todas** as contas.

## 1. Levantar pendências

Janela padrão: últimos 7 dias + tudo que ainda estiver aberto.

- **Mercado Livre**: `ml_claims_search` (status aberto) → para cada uma `ml_claim_get`, `ml_claim_returns` e `ml_claim_messages`. Ver também `ml_messages_unread` para pós-venda ligado a devolução.
- **Shopee** (5 lojas): `shopee_get_return_list` → `shopee_get_return_detail` e `shopee_get_return_solutions` para cada uma. Ver cancelamentos solicitados pelo comprador nos pedidos (`shopee_search_orders`).
- **TikTok Shop** (2 lojas): `tiktok_search_returns` e `tiktok_search_cancellations` → `tiktok_return_records` quando precisar do histórico.

Para cada caso colete: loja, pedido, produto/SKU, valor, motivo alegado, evidências (fotos/mensagens), prazo para responder, status do envio de volta.

## 2. Analisar e recomendar

Para cada caso, recomende **uma** ação com justificativa de 1 linha:

- **Aceitar / reembolsar** — defeito, item errado/faltando por nossa culpa, arrependimento dentro do prazo legal (7 dias), valor baixo em que contestar custa mais que o item.
- **Oferecer solução parcial** (reembolso parcial, troca) — quando o marketplace permitir e fizer sentido.
- **Contestar** — motivo não bate com as evidências, produto devolvido diferente/danificado pelo comprador, fora do prazo.
- **Aguardar** — produto ainda em trânsito de volta; indicar quando revisar.

Destaque no topo os casos com **prazo vencendo em até 48h**.

## 3. Relatório

Monte uma planilha (skill `xlsx`) com uma linha por caso: Marketplace | Loja | Pedido | Produto | Valor | Motivo | Prazo | Recomendação | Justificativa. Adicione uma aba de resumo por loja (qtd, valor total, % por motivo) e liste os SKUs com mais devoluções.

Entregue:
1. Salve no Google Drive em `Relatórios Claude/Devoluções/AAAA-MM-DD - Devoluções`.
2. Envie email para willgusta09@gmail.com com assunto `Devoluções AAAA-MM-DD — X casos (Y urgentes)`, resumo curto e link da planilha. No email, diga que as ações aguardam aprovação na sessão do Claude Code.

## 4. Executar (só com aprovação)

Mostre no chat a lista numerada de ações propostas e **pare**. Só execute o que o usuário aprovar (ex.: "aprova 1-5, contesta o 7"). Ações disponíveis:

- ML: `ml_claim_send_message` (e ações de claim via `list_actions`).
- Shopee: `shopee_confirm_return`, `shopee_dispute_return` (motivos em `shopee_get_return_dispute_reason`), `shopee_offer_return_solution`, `shopee_accept_return_offer`, `shopee_handle_buyer_cancellation`.
- TikTok: `tiktok_approve_return`, `tiktok_reject_return` (motivos em `tiktok_return_reject_reasons`), `tiktok_approve_cancellation`, `tiktok_reject_cancellation`.

Depois de executar, confirme o resultado de cada ação e atualize a planilha com uma coluna "Executado".
