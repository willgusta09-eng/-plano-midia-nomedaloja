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

### Planilha — layout obrigatório

Gere com a skill `xlsx` (openpyxl) e salve no Google Drive em `Relatórios Claude/Ads/AAAA-MM-DD - Ads`, convertendo para Google Sheets. **Uma tabela por aba**, nunca seções empilhadas na mesma aba. Abas, nesta ordem e com estas colunas exatas:

1. **Alertas** — `Severidade | Loja | Canal | Alerta | Ação sugerida`. Severidade: ALTA, MÉDIA, INFO (nessa ordem).
2. **Resumo** — uma linha por loja + canal: `Loja | Canal | Invest ontem | GMV Ads ontem | ROAS ontem | Invest média 7d | GMV Ads média 7d | ROAS média 7d | Var ROAS | Var GMV Ads | GMV total loja ontem | GMV total média 7d | Var GMV loja | Saldo Ads | Obs`. Linha final **TOTAL** com fórmulas (`=SUM`, ROAS = GMV/Invest).
3. **Campanhas** — todas as lojas com Ads, top 10 por investimento de cada loja + uma linha "Demais" somada: `Marketplace | Loja | Campanha | ID | Invest | GMV | ROAS | Pedidos | Cliques | CTR | CPC | Obs`.
4. **GMV Max** — `Loja | ID campanha | ROAS alvo | Orçamento diário | Invest ontem | GMV ontem | ROAS ontem | Pedidos ontem | Invest média 7d | GMV média 7d | ROAS média 7d | Pedidos média 7d | Obs`.
5. **Recomendações** — `Prioridade | Loja | Campanha | Ação | Motivo | Impacto estimado (R$)`.

Regras de formatação:
- Células numéricas são **números de verdade**, nunca texto: nada de `~`, `R$`, `%`, `est.` ou `n/c` dentro da célula. Valores estimados ou indisponíveis → célula vazia e a explicação na coluna **Obs**.
- Formatos: R$ `"R$ "#,##0.00`; percentuais como fração com formato `0%` (ex.: -0,11 → -11%); ROAS `0.00`; pedidos `0`.
- Cabeçalho na linha 1, negrito, fundo cinza claro, congelado (`freeze_panes = "A2"`), filtro automático ligado, largura de coluna ajustada ao conteúdo (máx. ~50).
- Formatação condicional: variações negativas em vermelho, positivas em verde; linhas ALTA da aba Alertas com fundo vermelho claro.
- Datas no formato DD/MM/AAAA. O dia analisado e a janela da média (ex.: 27/09 vs 20–26/09) vão no nome do arquivo e no email, não em linhas extras da planilha.

### Email

Email para willgusta09@gmail.com, assunto `Ads AAAA-MM-DD — Invest R$ X | GMV Ads R$ Y | ROAS Z`, com: alertas, tabela resumo por loja (invest, GMV, ROAS, variação vs 7d) e as recomendações, mais o link da planilha.
