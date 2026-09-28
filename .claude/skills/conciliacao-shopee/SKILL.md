---
name: conciliacao-shopee
description: Conciliação financeira das 4 lojas Shopee — compara o que caiu (repasses/carteira) com as vendas do mês até a data e detalha cada gasto (comissão, taxa de serviço, frete, cupons, Ads, multas, devoluções). Use às quintas ou quando o usuário pedir conciliação, repasse ou "quanto caiu da Shopee".
---

# Conciliação Shopee — mês até a data

Lojas: as 4 contas Shopee da tabela em `CLAUDE.md`. Tarefa **somente leitura**. **Nunca invente número**: todo valor na planilha vem de uma chamada; o que for estimado é marcado como estimado.

**Período:** do dia 1 do mês até ontem (quarta), fuso America/Sao_Paulo. Se o mês começou há menos de 3 dias, use o mês anterior completo.

## Limites da API (medidos em 28/09/2026 — respeite)

- Datas em **epoch de segundos do ano correto**. Calcule com Python, nunca de cabeça:
  `python3 -c "from datetime import datetime; from zoneinfo import ZoneInfo as Z; print(int(datetime(2026,9,1,tzinfo=Z('America/Sao_Paulo')).timestamp()))"`
- `shopee_get_wallet_transactions`: janela **máx. 15 dias**, `page_size` máx. 50, paginar com `page_no` enquanto `more=true`.
- `shopee_get_escrow_list` (repasses por pedido, compacto): `page_size` 100. Se vier `more=true` sem cursor, **divida a janela ao meio** e repita até cada pedaço vir com `more=false` (na MWUtilidades use janelas de 1 dia).
- `shopee_get_income_overview`: `params = {income_status: 1, release_time_from, release_time_to}` → `released_amount`. **Sem janela devolve valor acumulado sem sentido** (já retornou R$ 899 mil) — sempre passe as datas.
- `shopee_sales_summary(start_date, end_date)`: se `parcial=true`, chame de novo com `end_date = continuar_de` e some até `parcial=false`.
- `shopee_get_escrow_detail_batch`: até 50 `order_sn` por chamada, ~2,5 mil tokens por pedido — **caro**. Use conforme a seção 2.
- **Não use** `generate/get_income_report` nem `generate/get_income_statement`: retornam `PAYMENT_DOCUMENT_ID_NOT_FOUND` nesta integração.

## 1. Um agente por loja

Dispare **4 subagentes em paralelo** (ferramenta Agent, um por loja), cada um com estas instruções e o `shopId`. Cada subagente grava o resultado em `/tmp/conciliacao/<shopId>.json` e devolve só um resumo curto. Assim nenhum contexto estoura.

Cada subagente coleta:

1. **Vendas**: `shopee_sales_summary` no período (paginando) → bruto total e por status. Vendas válidas = todos os status menos `CANCELLED` e `UNPAID`. Guarde a lista `order_sn, total_amount, status` em CSV `/tmp/conciliacao/<shopId>_vendas.csv`.
2. **O que caiu (por pedido)**: `shopee_get_escrow_list` no período → `order_sn, payout_amount, escrow_release_time` em `/tmp/conciliacao/<shopId>_repasses.csv`. Some `payout_amount`.
3. **Conferência**: `shopee_get_income_overview` no mesmo período. Se diferir da soma do passo 2 em mais de 1%, registre a divergência (não escolha um lado).
4. **Gastos fora dos pedidos**: `shopee_get_wallet_transactions` com `money_flow: "MONEY_OUT"`, em janelas de 15 dias → agrupe por `transaction_type`/`description` (recarga de Ads `SPM_DEDUCT`, saques, multas, ajustes, reembolsos). Saques **não são gasto** — liste à parte.
5. **Detalhe das taxas por pedido** (`shopee_get_escrow_detail_batch` sobre os `order_sn` do passo 2):
   - Loja com **até 300 repasses** no período: busque **todos** → taxas exatas.
   - Loja com **mais de 300**: busque uma **amostra de 150 pedidos** espalhados pelo período (a cada N-ésimo da lista ordenada por data) → calcule a % de cada taxa sobre `order_selling_price` e aplique ao bruto dos pedidos repassados. Marque essas linhas como **"estimado por amostra de 150 pedidos"**.
   - Campos: comissão `commission_fee`; taxa de serviço `service_fee`; taxa de transação `seller_transaction_fee` + `credit_card_transaction_fee`; frete `actual_shipping_fee` − `shopee_shipping_rebate` − `buyer_paid_shipping_fee` (se positivo é custo); cupom do vendedor `voucher_from_seller`; moedas `seller_coin_cash_back`; afiliados `order_ams_commission_fee`; devolução `seller_return_refund` + `reverse_shipping_fee`; líquido `escrow_amount`. Guarde por pedido em `/tmp/conciliacao/<shopId>_taxas.csv`.
   - O **desconto do vendedor** (`seller_discount`) não é gasto pago à Shopee: mostre separado, como informação.
6. Grave o JSON com: bruto, qtd pedidos, total caiu, overview, cada categoria de gasto (valor, % das vendas, exato/estimado), gastos fora dos pedidos, saques, pedidos vendidos no período ainda **não repassados** (vendas − repasses por `order_sn`), repasses de pedidos de **meses anteriores**, e lista de pedidos anormais (repasse 0 em pedido concluído, líquido < 40% do bruto, ajuste negativo).

Se uma loja falhar, o subagente grava o erro no JSON e as demais seguem.

## 2. Consolidar (agente principal)

Leia os 4 JSON/CSV com Python e monte a planilha. Conciliação por loja:

`Vendas válidas − taxas dos pedidos = líquido esperado` → compare com `caiu na carteira` → explique a diferença com: a receber (vendido e não repassado), repasse de meses anteriores, devoluções, ajustes. O que não fechar vai para **Divergências** com o valor.

## 3. Planilha

Skill `xlsx` → Google Drive `Relatórios Claude/Financeiro/AAAA-MM-DD - Conciliação Shopee` (converter para Google Sheets). Uma tabela por aba, cabeçalho na linha 1 congelado com filtro, números reais (`"R$ "#,##0.00`, `0.0%`), nada de texto em célula numérica — observações na coluna `Obs`.

1. **Resumo** — uma linha por loja + TOTAL: `Loja | Pedidos | Vendas válidas | Comissão | Taxa de serviço | Taxa de transação | Frete | Cupons | Afiliados | Devoluções | Total taxas pedidos | % taxas | Ads | Multas/ajustes | Líquido esperado | Caiu na carteira | Diferença | A receber | Base (exato/amostra) | Obs`.
2. **Gastos** — `Loja | Tipo de gasto | Valor | % das vendas | Exato/Estimado | Obs`, ordenado por valor.
3. **Pedidos** — lojas com taxas exatas: uma linha por pedido com todas as taxas. Loja por amostra: a amostra, com `Obs = amostra`.
4. **Repasses** — todos os `order_sn` repassados no período com valor e data (de todas as lojas).
5. **Carteira (saídas)** — `Loja | Data | Tipo | Descrição | Valor`.
6. **Divergências** — `Loja | Pedido | Problema | Valor | Obs`.

## 4. Email

Para `willgusta09@gmail.com`, assunto `Conciliação Shopee DD/MM–DD/MM — Vendas R$ X | Caiu R$ Y | Taxas Z%`, **com a planilha anexada** (`attachments`, base64, mimeType xlsx) e link do Drive.

Corpo (HTML curto): o que exige atenção (divergências, pedidos sem repasse) → tabela resumo por loja → 5 maiores gastos → nota dizendo quais lojas estão com taxas estimadas por amostra.

Se alguma loja não fechar, **envie mesmo assim** com o que foi apurado e a lista do que faltou — nunca deixe de salvar e enviar.
