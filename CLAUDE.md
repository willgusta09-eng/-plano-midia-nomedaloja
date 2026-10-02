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
| Shopee | Kelvyn | `shopId: "836653758"` |
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
