# Operação das lojas — MWUtilidades

Repositório de operação e plano de mídia das lojas de marketplace. Idioma de trabalho: **português (Brasil)**. Fuso horário: **America/Sao_Paulo**. Valores em **R$**.

## Contas (conector Marktplace Connect)

Sempre passe o parâmetro da conta em cada chamada — não confie na conta "atual". Se algo mudar, rode `list_accounts` e atualize esta tabela.

| Marketplace | Loja | Parâmetro |
|---|---|---|
| Mercado Livre | MWUtilidades LTDA | `meliUserId: "605375221"` |
| Shopee | MWUtilidades LTDA (tem Ads) | `shopId: "490458132"` |
| Shopee | Djenyelle (tem Ads) | `shopId: "1611191705"` |
| Shopee | M.AShopping | `shopId: "1664670165"` |
| Shopee | WMUtilidadesBR | `shopId: "1730988368"` |
| TikTok Shop | MWUtilidades | ver `list_accounts` |
| TikTok Shop | NovatrendShop | ver `list_accounts` |

Use `list_actions` / `describe_action` para confirmar nome e parâmetros de uma ação antes de adivinhar.

## Rotinas

| Tarefa | Quando | Skill |
|---|---|---|
| Devoluções e reclamações | Terça e sexta, 9h | `/devolucoes` (`.claude/skills/devolucoes/SKILL.md`) |
| Métricas de Ads e GMV Max | Todo dia, 12h | `/ads-diario` (`.claude/skills/ads-diario/SKILL.md`) |
| Produtos com estoque 0 | Todo dia, 8h | `/estoque-zerado` (`.claude/skills/estoque-zerado/SKILL.md`) |

## Entrega dos relatórios

- **Email**: enviar para `willgusta09@gmail.com` pelo conector Gmail.
- **Google Drive**: salvar na pasta `Relatórios Claude` (criar se não existir), subpastas `Devoluções`, `Ads` e `Estoque`. Nome do arquivo: `AAAA-MM-DD - <tarefa>`.

## Regras gerais

- **Nunca** aceitar, recusar, contestar ou reembolsar devolução sem aprovação explícita do usuário no chat. Primeiro analisar e propor.
- **Nunca** alterar orçamento, ROAS alvo, pausar ou criar campanha sem aprovação explícita. Relatórios só recomendam.
- Se uma conta falhar (token expirado, erro de API), registrar no relatório e seguir com as demais — não abortar tudo. Reconexão é em marketplaces.tiops.com.br.
- Relatórios curtos e acionáveis: primeiro o que precisa de ação, depois os números.

## Custos de produtos Shopee (geral)

Fonte: tabela de custos enviada pelo usuário. Chave: SKU. Custo unitário em R$. Multiplicar pela quantidade do SKU (ex.: `10x148` = 10 × 0,30). `PETPUV3/5/6/7/8` usam o custo do `PETPUV2` até confirmação.

| SKU | Produto | Custo (R$) |
|---|---|---|
| 100 | CORDÃO DE MOTO HONDA | 2.00 |
| 4300 | FACÃO 12' (25CM) | 9.64 |
| 1507 | LAMINA 30MM 24 DENTES | 0.78 |
| 5221 | MÃO FRANCESA 19CM BRANCA | 1.53 |
| 5225 | MÃO FRANCESA 23CM BRANCA | 1.85 |
| 5251 | SUPORTE 10X12 BRANCO | 0.45 |
| 5252 | SUPORTE 15X20 BRANCO | 0.86 |
| 5253 | SUPORTE 20X25 BRANCO | 1.17 |
| 103 | GEL MASSAGEM ARNICA | 2.68 |
| 148 | BUCHA MAGICA | 0.30 |
| PETPUV2 | PULVERIZADOR MANUAL | 3.98 |
| 5230 | MÃO FRANCESA 29CM BRANCO | 2.23 |
| 149 | FUNIL FLEXIVEL | 3.00 |
| 150 | BOMBONIERE | 5.25 |
| 153+1211 | OLHO MAGICO PRATA + BROCA 9/16 | 4.21 |
| PRETA19CM | MÃO FRANCESA 19CM PRETA | 1.54 |
| PRETA23CM | MÃO FRANCESA 23CM PRETA | 1.86 |
| PRETA29CM | MÃO FRANCESA 29CM PRETA | 2.23 |
| 160 | CORDA ELASTICA 120CMX8MM | 4.75 |
| PNEU-8 | REPARO DE PNEU | 3.14 |
| PRETA10X12 | SUPORTE 10X12 PRETO | 0.47 |
| PRETA15X20 | SUPORTE 15X20 PRETO | 0.76 |
| PRETA20X25 | SUPORTE 20X25 PRETO | 1.06 |
| 5222+1211 | OLHO MAGICO DOURADO + BROCA 9/16 | 4.21 |
| FACAO14 | FACAO 14' | 10.75 |
| FACAO16 | FACAO 16' | 11.04 |
| FACAO18 | FACAO 18' | 11.80 |
| 6905 | PULVERIZADOR 5L FERTAK | 43.88 |
| 1601 | BOMBA DE AR 30CM | 5.56 |
| 6906 | PULVERIZADOR 350ML FERTAK | 5.92 |
| 5240 | MÃO FRANCESA 38,5CM BRANCA | 4.29 |
| PRETA38,5 | MÃO FRANCESA 38,5CM PRETA | 4.29 |
| 5254 | SUPORTE 25X30CM BRANCO | 1.67 |
| 8506 | GRAMPO 106/ 6MM | 1.68 |
| 8508 | GRAMPO 106/8MM | 1.61 |
| 8510 | GRAMPO 106/10MM | 2.12 |
| 8512 | GRAMPO 106/12MM | 2.21 |
| 8514 | GRAMPO 106/14MM | 2.40 |
| 1600 | BOMBA DE AR 50CM | 7.08 |
| 1625 | BOIA DE NIVEL 25A FERTAK | 15.91 |
| 8501 | GRAMPEADOR | 31.20 |
| 8504 | GRAMPO T 1.2X10X2.0 MM | 2.21 |
| 8507 | GRAMPO U 1.2X12X6.3 | 3.60 |
| 6913 | PULVERIZADOR 500ML | 4.39 |
| 6900 | PULVERIZADOR 1000ML | 6.13 |
| 3DSHREK | SHREKA | 0.85 |
| 31205 | VEDA ROSCA | 0.62 |
| 142 | PARAFUSO + BUCHA | 0.06 |
| 1657 | ABRAÇADEIRA DE METAL | 0.31 |
| 8200 | CHAVE TESTE 100-240V 140MM | 1.38 |
| 3406 | FITA DUPLA FACE | 2.46 |
| BFH1266 | KIT 3 PINCEL BESTFER | 3.92 |
| BFH2623 | KIT BORRACHA VEDAÇÃO BESTFER (50PCS) | 4.13 |
| 9234 | FAQUEIRO | 42.63 |
| 8715 | RODO MOP | 8.43 |
| 8735 | RODO GRANDE | 6.88 |
| 1892 | FRUTEIRA | 13.56 |
| 1351 | PANELA COM FRITADEIRA | 55.06 |
| 75367 | TESOURA DE PODA | 8.60 |
| 6301 | NIVEL DE MÃO 30CM | 6.26 |
| 9159 | SABONETEIRA | 5.61 |
| RD1199 | BOMBA DE AR PETRIN | 3.80 |
| RD2067 | PULVERIZADOR 570ML | 2.66 |
| 3DDUMMY | DUMMY (IMPRESSO 3D) | 3.92 |
| 3DGHOST | FANTASMA (IMPRESSO 3D) | 2.91 |
| 3DARVORE | ÁRVORE DE NATAL (IMPRESSO 3D) | 1.80 |
| 3DGHOSTFACE | GHOSTFACE (IMPRESSO 3D) | 2.91 |
| 3DNATALFLOCO | Feliz Natal (Floco) | 5.26 |
| 3DNATALARVORE | Feliz Natal (Arvore) | 3.50 |
| PRETA25X30 | Mão Francesa Preta 25x30 | 1.41 |
| 100617 | Pulverizador 650ml | 3.61 |
| 8217 | BOCAL BRANCO TERMOPLASTICO BR E27 | 1.63 |
| 8227 | BOCAL PRETO TERMOPLASTICO PR E27 | 1.66 |
| 1701 | CADEADO BIKE CHAVE 120 CM X 06 MM | 7.32 |
| 5211 | SUP PARA TRILHO SIMPLES BRANCO 200 MM | 1.70 |
| 5212 | SUP PARA TRILHO SIMPLES BRANCO 250 MM | 2.27 |
| 5213 | SUP PARA TRILHO SIMPLES BRANCO 300 MM | 2.55 |
| MB7125 | CADEADO BIKE 80X10CM | 4.84 |
| MB8139 | PROTETOR ADESIVO P/ MOVEIS | 1.40 |
| MB9293 | CHAVE Y CANHAO 8 10 12MM | 2.26 |
| MB9336 | CLIP DE MOLA C/ 4 3 | 4.29 |
| CN0355 | SUPORTE P/ FACAS | 17.04 |
| 3DESPIRAL | SENSORIAL ESPIRAL | 8.52 |
| 3DCUBO | SENSORIAL CUBO | 3.36 |
| 3DOVO | SENSORIAL OVO | 6.60 |
| 3DLIXEIRA | LIXEIRA 3D | 8.56 |
| MB9266 | ESCOVA DE AÇO C/ HASTE 3PÇS | 4.80 |
| 3DGANCHO | GANCHO ORGANIZADOR 3D | 0.60 |
| 3DHEADSET | SUPORTE HEADSET 3D | 6.48 |
| GANCHO-COLINA | Ganchos Multiuso Em Formato S | 0.40 |
| BOLEIRA-36CM | BOLEIRA 36cm | 15.00 |
| BOLEIRA-29CM | BOLEIRA 29CM | 12.00 |
| BOLEIRA-24CM | BOLEIRA 24CM | 9.00 |
| BOLEIRA-20.3CM | BOLEIRA 21CM | 7.50 |
| TAMPA-MICROONDAS-COLINA | TAMPA DE MICRO-ONDAS | 6.00 |
| TAMPA-BOLEIRA-30CM-COLINA | TAMPA DE BOLEIRA 30CM | 10.00 |
| TAMPA-BOLEIRA-25CM-COLINA | TAMPA DE BOLEIRA 25CM | 8.00 |
