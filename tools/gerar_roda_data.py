# -*- coding: utf-8 -*-
"""
Gerador de dados da Roda Cíclica.

Lê a planilha "BASE DE DADOS" (modelo V10) e gera o arquivo
`roda-ciclica-data.js` (define `window.RODA_DATA`) usado pela página
`roda-ciclica.html`. Roda nos dois projetos (raiz e v2) ao mesmo tempo.

USO:
    python tools/gerar_roda_data.py ["caminho/para/BASE DE DADOS.xlsx"]

Se nenhum caminho for passado, usa o V10 padrão em Downloads.
A roda NÃO precisa ser redesenhada quando os dados mudam: basta
atualizar a planilha e rodar este script de novo.
"""
import sys, os, io, json

try:
    import openpyxl
except ImportError:
    sys.exit("Falta o openpyxl. Rode: python -m pip install openpyxl")

# -- caminhos ---------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)                       # .../agrocete-site
DEFAULT_XLSX = os.path.join(
    os.path.expanduser("~"), "Downloads", "BASE DE DADOS - V10.xlsx"
)
XLSX = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_XLSX

# Onde gravar o data.js (os dois projetos):
TARGETS = [
    os.path.join(REPO, "roda-ciclica-data.js"),
    os.path.join(REPO, "v2", "roda-ciclica-data.js"),
]

# Nomes/categoria/descrição das 10 dores macro do anel 3.
# A planilha V10 não traz coluna de NOME para a dor macro; estes textos
# vêm da curadoria da V05 (mesmos IDs D01..D10, mesma semântica).
# Se a planilha um dia ganhar uma coluna NOME na aba CONTEUDO_DOR, ela
# passa a ter prioridade (ver lógica abaixo).
DOR_MACRO = {
    "D01": {"name": "FBN baixa / nódulo fraco",            "category": "Biológico",          "desc": "Baixa formação ou sustentação de nodulação"},
    "D02": {"name": "Arranque e vigor inicial",            "category": "Estabelecimento",    "desc": "Emergência/desenvolvimento inicial abaixo do esperado"},
    "D03": {"name": "Raiz limitada / aproveitamento de P", "category": "Nutrição / raiz",    "desc": "Baixa exploração radicular e menor aproveitamento de fósforo"},
    "D04": {"name": "Micros limitando",                    "category": "Nutrição",           "desc": "Micronutrientes limitando ritmo de crescimento"},
    "D05": {"name": "B/Mo não acompanhando demanda",       "category": "Reprodutivo",        "desc": "Demanda por B e Mo acima do suprimento"},
    "D06": {"name": "Co/Mo inconsistentes",                "category": "Biológico / nutrição","desc": "Resposta irregular por Co/Mo"},
    "D07": {"name": "Desequilíbrio de Mg",                 "category": "Nutrição",           "desc": "Magnésio não sustentando fotossíntese e enchimento"},
    "D08": {"name": "Perdas na pulverização",              "category": "Operacional",        "desc": "Deriva, espuma, cobertura e deposição abaixo do ideal"},
    "D09": {"name": "Resíduo no pulverizador",             "category": "Operacional",        "desc": "Risco de fitotoxidade ou contaminação cruzada"},
    "D10": {"name": "Pegamento e retenção reprodutiva",    "category": "Reprodutivo",        "desc": "Abortamento, baixo pegamento ou menor retenção"},
}


def load():
    wb = openpyxl.load_workbook(XLSX, data_only=True, read_only=True)

    def rows(sheet):
        ws = wb[sheet]
        data = list(ws.iter_rows(values_only=True))
        if not data:
            return [], []
        hdr = [("" if c is None else str(c).strip()) for c in data[0]]
        out = []
        for r in data[1:]:
            if all(c is None or str(c).strip() == "" for c in r):
                continue
            out.append(r)
        return hdr, out

    def cell(r, i):
        if i is None or i < 0 or i >= len(r):
            return ""
        v = r[i]
        return "" if v is None else (v if isinstance(v, (int, float)) else str(v).strip())

    def col(hdr, name):
        return hdr.index(name) if name in hdr else None

    # ---- CULTURAS ----
    hdr, rs = rows("CULTURAS")
    cid, cname, cativo = col(hdr, "CULTURA_ID"), col(hdr, "CULTURA"), col(hdr, "ATIVO_NA_RODA")
    cultures, name_to_cid = [], {}
    for r in rs:
        _id = cell(r, cid)
        _nm = cell(r, cname)
        name_to_cid[_nm] = _id
        name_to_cid[_id] = _id
        if str(cell(r, cativo)).upper() == "S":
            cultures.append({"id": _id, "name": _nm})

    # ---- ESTADIOS ----
    hdr, rs = rows("ESTADIOS")
    eid, ecult, enome, eordem, eativo = (
        col(hdr, "ESTADIO_ID"), col(hdr, "CULTURA"), col(hdr, "ESTADIO"),
        col(hdr, "ORDEM_NO_ANEL"), col(hdr, "ATIVO_NA_RODA"),
    )
    stages = []
    for r in rs:
        if str(cell(r, eativo)).upper() not in ("S", ""):
            continue
        try:
            order = int(float(cell(r, eordem) or 0))
        except (ValueError, TypeError):
            order = 0
        stages.append({
            "id": cell(r, eid),
            "cultureId": name_to_cid.get(cell(r, ecult), cell(r, ecult)),
            "name": cell(r, enome),
            "order": order,
        })

    # ---- PRODUTOS ----
    hdr, rs = rows("PRODUTOS")
    pid, pexib, pcat, pativo, pobs = (
        col(hdr, "PRODUTO_ID"), col(hdr, "NOME_EXIBICAO"), col(hdr, "CATEGORIA"),
        col(hdr, "ATIVO_NA_RODA"), col(hdr, "OBS"),
    )
    products = []
    for r in rs:
        if str(cell(r, pativo)).upper() != "S":
            continue
        products.append({
            "id": cell(r, pid),
            "name": cell(r, pexib) or cell(r, pid),
            "category": cell(r, pcat),
            "obs": cell(r, pobs),
        })

    # ---- RELACIONAMENTOS ----
    hdr, rs = rows("RELACIONAMENTOS")
    rc, re_, rd, rp, rprio, rwhy, rnote = (
        col(hdr, "CULTURA_ID"), col(hdr, "ESTADIO_ID"), col(hdr, "DOR_ID"),
        col(hdr, "PRODUTO_ID"), col(hdr, "PRIORIDADE"),
        col(hdr, "JUSTIFICATIVA_CURTA"), col(hdr, "OBS_INTERFACE"),
    )
    relationships = []
    for r in rs:
        try:
            prio = int(float(cell(r, rprio) or 3))
        except (ValueError, TypeError):
            prio = 3
        relationships.append({
            "cultureId": cell(r, rc),
            "stageId": cell(r, re_),
            "dorId": cell(r, rd),
            "productId": cell(r, rp),
            "priority": prio,
            "why": cell(r, rwhy),
            "note": cell(r, rnote),
        })

    # ---- CONTEUDO_ESTAGIO ----
    hdr, rs = rows("CONTEUDO_ESTAGIO")
    e_idx = col(hdr, "ESTADIO_ID")
    conteudoEstagio = {}
    for r in rs:
        key = cell(r, e_idx)
        if not key:
            continue
        conteudoEstagio[key] = {hdr[i]: cell(r, i) for i in range(len(hdr)) if hdr[i]}

    # ---- CONTEUDO_DOR (10 dores macro) ----
    hdr, rs = rows("CONTEUDO_DOR")
    d_idx = col(hdr, "DOR_ID")
    nome_idx = col(hdr, "NOME") if "NOME" in hdr else None  # futuro
    conteudoDor, dor_ids = {}, []
    for r in rs:
        key = cell(r, d_idx)
        if not key:
            continue
        dor_ids.append(key)
        conteudoDor[key] = {hdr[i]: cell(r, i) for i in range(len(hdr)) if hdr[i]}

    # ---- DORES MACRO (anel 3) ----
    dors = []
    for did in dor_ids:
        macro = DOR_MACRO.get(did, {})
        nome_planilha = ""
        if nome_idx is not None:
            nome_planilha = conteudoDor.get(did, {}).get("NOME", "")
        dors.append({
            "id": did,
            "name": nome_planilha or macro.get("name", did),
            "category": macro.get("category", ""),
            "desc": macro.get("desc", ""),
        })

    # ---- CARD_PRODUTO ----
    hdr, rs = rows("CARD_PRODUTO")
    cp_p, cp_c = col(hdr, "PRODUTO_ID"), col(hdr, "CULTURA_ID")
    cardProduto = {}
    for r in rs:
        pkey, ckey = cell(r, cp_p), cell(r, cp_c)
        if not pkey or not ckey:
            continue
        cardProduto["%s__%s" % (pkey, ckey)] = {hdr[i]: cell(r, i) for i in range(len(hdr)) if hdr[i]}

    # ---- ALIASES_BUSCA ----
    hdr, rs = rows("ALIASES_BUSCA")
    aliases = []
    for r in rs:
        row = {hdr[i]: cell(r, i) for i in range(len(hdr)) if hdr[i]}
        if row.get("TERMO_DIGITADO"):
            aliases.append(row)

    return {
        "cultures": cultures,
        "stages": stages,
        "dors": dors,
        "products": products,
        "relationships": relationships,
        "conteudoEstagio": conteudoEstagio,
        "conteudoDor": conteudoDor,
        "cardProduto": cardProduto,
        "aliases": aliases,
    }


def main():
    if not os.path.exists(XLSX):
        sys.exit("Planilha não encontrada: %s" % XLSX)
    data = load()
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    header = (
        "/* Gerado automaticamente por tools/gerar_roda_data.py\n"
        "   Fonte: %s\n"
        "   NÃO editar à mão — altere a planilha e rode o gerador. */\n"
    ) % os.path.basename(XLSX)
    body = header + "window.RODA_DATA = " + payload + ";\n"

    for path in TARGETS:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(body)
        print("escrito:", path)

    print("\nResumo:")
    print("  culturas:        %d" % len(data["cultures"]))
    print("  estádios:        %d" % len(data["stages"]))
    print("  dores macro:     %d" % len(data["dors"]))
    print("  produtos:        %d" % len(data["products"]))
    print("  relacionamentos: %d" % len(data["relationships"]))
    print("  conteudoEstagio: %d" % len(data["conteudoEstagio"]))
    print("  conteudoDor:     %d" % len(data["conteudoDor"]))
    print("  cardProduto:     %d" % len(data["cardProduto"]))
    print("  aliases:         %d" % len(data["aliases"]))


if __name__ == "__main__":
    main()
