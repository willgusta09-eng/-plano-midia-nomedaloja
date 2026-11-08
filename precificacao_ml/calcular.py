"""Calcula preço recomendado no Mercado Livre a partir de preço Shopee promocional.

Entrada (JSON, lista): [{"anuncio", "sku", "preco_ml_atual", "preco_shopee_promo"}]
Custos vêm de custos.csv (custo unitário × quantidade do SKU, ex.: 10x148 = 10 × 0,30).
Regras:
- Taxa Shopee medida: 34,1% do preço (comissão + taxa de serviço).
- Taxa ML Premium (gold_pro): 16%. Frete é repassado ao comprador (não entra no cálculo).
- Nunca baixa preço do ML. Sobe só se o ML estiver abaixo de Shopee promo + 10%.
Uso: python3 calcular.py entrada.json > saida.csv
"""
import csv, json, math, re, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
TAKE_SHOPEE, FEE_ML, MARKUP = 0.341, 0.16, 0.10


def carregar_custos():
    with open(os.path.join(HERE, "custos.csv"), encoding="utf-8") as f:
        return {r["sku_base"].upper(): float(r["custo_unitario"].replace(",", "."))
                for r in csv.DictReader(f, delimiter=";")}


def custo(sku, tabela):
    s = re.sub(r"\s+", "", sku).upper()
    m = re.match(r"^(\d+)X(.+)$", s)
    qtd, base = (int(m.group(1)), m.group(2)) if m else (1, s)
    if base.startswith("PETPUV"):
        base = "PETPUV2"  # estimativa até confirmar custo de cada variante
    if base == "109A":
        base = "5251"
    if base == "BRANCO1-23CM":
        base = "5225"
    if base not in tabela:
        return None
    return round(qtd * tabela[base], 2)


def arredonda_90(x):
    return math.ceil(x - 0.90) + 0.90


def main(caminho):
    tabela = carregar_custos()
    itens = json.load(open(caminho, encoding="utf-8"))
    w = csv.writer(sys.stdout, delimiter=";")
    w.writerow(["anuncio", "sku", "custo", "shopee_promo", "margem_shopee_%",
                "ml_atual", "ml_recomendado", "margem_ml_%_recomendado", "acao"])
    for it in itens:
        c = custo(it["sku"], tabela)
        if c is None:
            w.writerow([it["anuncio"], it["sku"], "", "", "", "", "", "", "SEM CUSTO"])
            continue
        psh = float(it["preco_shopee_promo"])
        ml = float(it["preco_ml_atual"])
        m_sh = (psh * (1 - TAKE_SHOPEE) - c) / psh
        piso = arredonda_90(psh * (1 + MARKUP))
        novo = max(ml, piso)
        acao = "SUBIR" if novo > ml else "MANTER"
        m_ml = (novo * (1 - FEE_ML) - c) / novo
        w.writerow([it["anuncio"], it["sku"], f"{c:.2f}", f"{psh:.2f}", f"{m_sh*100:.1f}",
                    f"{ml:.2f}", f"{novo:.2f}", f"{m_ml*100:.1f}", acao])


if __name__ == "__main__":
    main(sys.argv[1])
