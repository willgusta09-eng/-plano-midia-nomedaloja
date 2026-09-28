---
name: ads-diario
description: Análise diária das métricas de Ads e GMV Max de todas as lojas (Shopee Ads e GMV Max, Mercado Ads, TikTok Shop), comparando ontem com a média dos 7 dias anteriores e recomendando ajustes. Use todo dia ou quando o usuário pedir análise de Ads/GMV Max.
---

# Ads e GMV Max — análise diária

Contas e parâmetros: ver tabela em `CLAUDE.md`. Percorra **todas** as contas; lojas sem Ads ativo entram só com vendas.

Período: **ontem** (dia fechado) + parcial de hoje, comparado com a **média dos 7 dias anteriores**.

## 1. Coletar

- **Shopee** (todas as lojas; Ads ativo em MWUtilidades e Djenyelle):
  - Ads manuais/auto: `shopee_ads_campaigns`, `shopee_ads_daily_performance`, `shopee_ads_campaign_daily`.
  - GMV Max: `shopee_ads_gms_performance`, `shopee_ads_gms_items`.
  - Saldo: `shopee_ads_balance`. Vendas totais: `shopee_sales_summary`, `shopee_sales_by_item`.
- **Mercado Livre**: `ml_ads_campaigns`, `ml_ads_campaigns_metrics`, `ml_ads_metrics` (e `ml_ads_items` para os anúncios).
- **TikTok Shop** (2 lojas): `tiktok_analytics_shop`, `tiktok_analytics_products`; se precisar, `get-tiktok-shop-performance` do conector AfterShip.

## 2. Métricas por loja e por campanha

Investimento, GMV/receita atribuída, **ROAS** (e ACOS = 1/ROAS), impressões, cliques, CTR, CPC, pedidos, conversão, custo por pedido, % do GMV total da loja vindo de Ads. No GMV Max: ROAS alvo vs realizado e consumo do orçamento.

## 3. Alertas (vão no topo do relatório)

- ROAS de ontem **30% abaixo** da média de 7 dias, ou abaixo do ROAS alvo.
- Campanha que gastou e **não vendeu**.
- Orçamento esgotando cedo (limitando entrega) em campanha com ROAS bom → candidata a aumento.
- Saldo de Ads baixo (menos de 3 dias de gasto médio).
- Queda de GMV total da loja > 20% vs média.
- Conta que falhou na coleta.

## 4. Recomendações

Até 5 ações concretas, priorizadas por impacto em R$ (ex.: "Djenyelle — GMV Max: subir ROAS alvo de 6 para 7, ROAS realizado 4,1 nos últimos 3 dias"). **Não execute** nenhuma alteração; só recomende. Se o usuário aprovar no chat, use `shopee_ads_edit_campaign`, `shopee_ads_gms_edit`, `shopee_ads_pause_campaign`, `ml_ads_update_campaign` etc.

## 5. Entregar

1. Planilha (skill `xlsx`) com abas: Resumo (por loja), Campanhas, GMV Max, Alertas. Salve no Google Drive em `Relatórios Claude/Ads/AAAA-MM-DD - Ads`.
2. Email para willgusta09@gmail.com, assunto `Ads AAAA-MM-DD — Invest R$ X | GMV Ads R$ Y | ROAS Z`, com: alertas, tabela resumo por loja (invest, GMV, ROAS, variação vs 7d) e as recomendações, mais o link da planilha.
