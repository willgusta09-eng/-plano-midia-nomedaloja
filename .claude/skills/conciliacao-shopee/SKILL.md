---
name: conciliacao-shopee
description: Conciliação financeira das 4 lojas Shopee — compara o saldo que caiu (repasses/carteira) com as vendas do mês até a data e detalha cada gasto (comissão, taxa de serviço, frete, cupons, Ads, multas, devoluções). Use às quintas ou quando o usuário pedir conciliação, repasse ou "quanto caiu da Shopee".
---

# Conciliação Shopee — mês até a data

Lojas: as 4 contas Shopee da tabela em `CLAUDE.md` (MWUtilidades, Djenyelle, M.AShopping, WMUtilidadesBR), cada uma separada + total. Tarefa **somente leitura**.

**Período:** do dia 1 do mês atual até ontem (quarta-feira). Se o mês começou há menos de 3 dias, faça também o mês anterior completo, em abas separadas.

Use `list_actions` / `describe_action` para confirmar parâmetros. Pagine tudo até o fim — conciliação com dado parcial é inútil; se não conseguir tudo, diga exatamente o que ficou faltando.

## 1. Coletar (por loja)

- **Vendas do período**: `shopee_search_orders` / `shopee_list_orders` (pedidos criados no período, todos os status) → valor bruto, status (concluído, enviado, cancelado, devolvido, não pago).
- **Repasse por pedido (escrow)**: `shopee_get_escrow_list` no período + `shopee_get_escrow_detail_batch` (ou `shopee_get_escrow_detail`) → para cada pedido: valor pago pelo comprador, comissão, taxa de serviço, taxa de transação, frete (cobrado do vendedor / subsídio), cupom e desconto do vendedor, moedas, ajustes, **valor líquido repassado**.
- **Carteira (o que caiu de fato)**: `shopee_get_wallet_transactions` no período → todos os lançamentos: repasses de pedidos, recargas/débitos de Ads, saques, ajustes, multas, reembolsos, estornos.
- **Resumo oficial**: `shopee_get_income_overview` / `shopee_get_income_detail` e, se disponível, `shopee_generate_income_report` / `shopee_get_income_report` para bater o total.
- **Outros custos**: `shopee_get_penalties` (multas), `shopee_get_return_list` (devoluções no período), gasto de Ads no período (`shopee_ads_daily_performance`, `shopee_ads_gms_performance`).

## 2. Conciliar

Por loja:

1. **Vendas brutas** (pedidos válidos) − **cada custo** = **líquido esperado**.
2. **Líquido esperado** vs **total que caiu na carteira** (repasses de pedidos no período) → **diferença**.
3. Explique a diferença: pedidos vendidos ainda não liberados (a receber, com data prevista), pedidos liberados no período mas vendidos no mês anterior, devoluções/estornos, ajustes, multas.
4. Liste pedidos com **repasse anormal**: líquido < 60% do bruto, repasse zerado em pedido concluído, taxa de frete alta, ajuste negativo.

Gastos a separar sempre (uma linha cada, em R$ e em % das vendas brutas):
comissão · taxa de serviço (programas de frete grátis / cashback) · taxa de transação · frete pago pelo vendedor · cupons e descontos do vendedor · Ads (manual/auto) · GMV Max · multas · devoluções/reembolsos · ajustes · outros (descrever cada um).

## 3. Planilha

Skill `xlsx`, salve no Google Drive em `Relatórios Claude/Financeiro/AAAA-MM-DD - Conciliação Shopee` (crie as pastas se não existirem), convertendo para Google Sheets. Uma tabela por aba, cabeçalho na linha 1 congelado com filtro, números de verdade com formato `"R$ "#,##0.00` e `0.0%` (nada de texto dentro de células numéricas; observações na coluna `Obs`).

1. **Resumo** — uma linha por loja + TOTAL: `Loja | Pedidos | Vendas brutas | Comissão | Taxa de serviço | Taxa de transação | Frete | Cupons/descontos | Ads | GMV Max | Multas | Devoluções | Ajustes/outros | Total custos | % custos | Líquido esperado | Caiu na carteira | Diferença | A receber | Obs`.
2. **Gastos** — `Loja | Tipo de gasto | Valor | % das vendas | Qtd lançamentos | Obs`, ordenado por valor.
3. **Pedidos** — uma linha por pedido: `Loja | Pedido | Data venda | Status | Bruto | Comissão | Taxa serviço | Taxa transação | Frete | Cupom | Ajustes | Líquido | Data repasse | Obs`.
4. **Carteira** — todos os lançamentos: `Loja | Data | Tipo | Descrição | Pedido | Valor | Saldo`.
5. **Divergências** — pedidos anormais e diferenças sem explicação: `Loja | Pedido | Problema | Valor | Obs`.

## 4. Email

Para `willgusta09@gmail.com`, assunto `Conciliação Shopee DD/MM–DD/MM — Vendas R$ X | Caiu R$ Y | Custos Z%`.

Corpo: tabela resumo por loja (vendas, custos, % custos, caiu, diferença, a receber) · os 5 maiores gastos do período · divergências que precisam de atenção · link da planilha. Primeiro o que exige ação, depois os números.
