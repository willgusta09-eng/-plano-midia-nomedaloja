---
name: precificacao-ml
description: Revisa preços dos anúncios do Mercado Livre (MWUtilidades) com base no preço promocional da Shopee, com frete repassado ao comprador e o ML sempre acima da Shopee. Use quando o usuário pedir gestão de preço do ML, margem igual à Shopee ou revisão de preços do Mercado Livre.
---

# Precificação Mercado Livre a partir da Shopee

Conta ML: `meliUserId: "605375221"`. Conta Shopee de referência: `shopId: "490458132"`. Ver `CLAUDE.md`.

**Esta rotina só recomenda.** Aplicar preço no ML é alteração: só execute `update_item` depois de aprovação explícita do usuário no chat.

## Regras

- **Frete é repassado ao comprador.** Não entra no cálculo de margem do vendedor. Mas confirme nos anúncios que o envio é cobrado do comprador (frete grátis pelo ML faz o vendedor pagar).
- **Referência:** preço **promocional atual** da Shopee (`current_price` do modelo).
- **Taxas medidas:** Shopee 34,1% (comissão + taxa de serviço, medido em pedidos reais); ML Premium (gold_pro) 16%, sem taxa fixa nas faixas testadas.
- **ML sempre acima da Shopee:** nunca baixe preço do ML. Suba só se o ML estiver abaixo de Shopee promo + 10%. Os preços sobem para o próximo `,90`.
- **Custos:** `precificacao_ml/custos.csv`, custo unitário × quantidade do SKU (ex.: `10x148` = 10 × 0,30). Custos de `PETPUV3/5/6/7/8` são estimativas (usam PETPUV2) até confirmação.
- Anúncios sem par de SKU na Shopee ou sem custo ficam **fora** e vão no relatório como pendência.

## Passos

1. **Anúncios ML:** `list_items` com `meliUserId`, `status: "active"`, `com_atributos: true` (para ler `SELLER_SKU`). Pagine até o fim. Se tiver mais de 1.050, use `search_type: "scan"`.
2. **Shopee:** `shopee_list_items` (`page_size: 100`, paginando por `offset`) → `shopee_get_items_batch` com `need_model_info: true` (lotes de até 50 IDs). Para cada modelo, guarde `model_sku` e `price_info[0].current_price`.
3. **Cruzar por SKU** (sem espaços, maiúsculo). Se o mesmo SKU aparecer em vários itens da Shopee, use o primeiro e registre.
4. **Montar entrada** em JSON: `[{"anuncio", "sku", "preco_ml_atual", "preco_shopee_promo"}]`.
5. **Calcular:** `python3 precificacao_ml/calcular.py entrada.json > precos.csv`.
6. **Conferir frete** dos anúncios marcados como SUBIR com `ml_shipping_options_item` (CEP de referência do usuário). Se o comprador não pagar o envio, reporte antes de subir.
7. **Relatório (primeiro o que precisa de ação):**
   - Lista de SUBIR com preço atual → novo.
   - Pendências: sem par na Shopee, sem custo, custo estimado.
   - Números: quantos MANTER e quantos SUBIR.
8. **Aguardar aprovação.** Só após "sim" no chat, aplicar com `update_item` (um anúncio por vez) e confirmar o retorno de cada um.

## Saída

Um CSV em `precificacao_ml/` com data no nome (`AAAA-MM-DD - precos ML.csv`) e o resumo no chat. Se o usuário pedir, enviar por email (`willgusta09@gmail.com`) e salvar em `Relatórios Claude/Precificação` no Drive, conforme `CLAUDE.md`.
