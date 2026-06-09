# -*- coding: utf-8 -*-
"""
Monta `roda-ciclica.html` para CADA projeto com o estilo visual do respectivo
site, partindo da base funcional da V05 (Downloads):

  • Projeto A (raiz)  -> tema claro/quente da marca (verde + papel), fontes Grotesk.
  • Projeto B (v2)    -> azul/cinza da marca renderizado com os padrões de
                          interface da plataforma (fonte de sistema, materiais
                          translúcidos, cantos amplos, controles em cápsula).

Mantém intactas as melhorias de LÓGICA já validadas (dados V10, consistência
cíclica, anel vazio) e a camada touch. Só o VISUAL muda por projeto.
"""
import os, re, io, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SRC = os.path.join(os.path.expanduser("~"), "Downloads", "Roda_ciclica_V05 (1).html")

# ---------------------------------------------------------------------------
# Geometria compartilhada (estrutura provada da V05) — toda cor vem de tokens.
# ---------------------------------------------------------------------------
RODA_CSS = r"""
  * { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: var(--font-body);
    background: var(--page-bg);
    background-attachment: fixed;
    color: var(--text);
    min-height: 100vh;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
  }
  .wrap {
    max-width: 1600px; margin: 0 auto; padding: 20px;
    display: grid; grid-template-columns: minmax(680px, 1.2fr) minmax(360px, .8fr);
    gap: 18px; min-height: 100vh;
  }
  .panel {
    background: var(--panel-bg);
    border: 1px solid var(--panel-border);
    border-radius: var(--radius-panel);
    box-shadow: var(--panel-shadow);
    overflow: hidden; position: relative;
    backdrop-filter: var(--panel-blur, none);
    -webkit-backdrop-filter: var(--panel-blur, none);
  }
  .left-panel { display: grid; grid-template-rows: auto 1fr auto; }
  .header { padding: 22px 24px 12px; border-bottom: 1px solid var(--hairline); }
  .eyebrow {
    color: var(--accent-ink); font-size: 12px; font-weight: 700;
    letter-spacing: .12em; text-transform: uppercase;
    font-family: var(--font-label, var(--font-body));
  }
  h1 {
    margin: 8px 0 8px; font-size: var(--h1-size, 28px); line-height: 1.05;
    font-family: var(--font-display); font-weight: var(--display-weight, 700);
    letter-spacing: var(--display-tracking, -0.01em); color: var(--text);
  }
  .sub { margin: 0; color: var(--muted); font-size: 15px; max-width: 860px; }
  .wheel-wrap { padding: 8px 20px 0; display: grid; place-items: center; position: relative; }
  #wheel { width: min(100%, 920px); height: min(78vh, 920px); display: block; }
  .helper {
    display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap;
    padding: 0 24px 22px; color: var(--muted); font-size: 13px;
  }
  .legend { display: flex; gap: 10px; flex-wrap: wrap; }
  .legend .pill, .chip {
    background: var(--chip-bg); border: 1px solid var(--chip-border);
    color: var(--chip-text); border-radius: var(--radius-chip, 999px);
    padding: 8px 12px; font-size: 12px; line-height: 1; white-space: nowrap;
  }
  .legend .pill strong { color: var(--accent-ink); }
  .right-panel { display: grid; grid-template-rows: auto auto 1fr auto; }
  .toolbar { padding: 18px 20px 14px; display: grid; gap: 12px; border-bottom: 1px solid var(--hairline); }
  .search { display: flex; gap: 10px; }
  .search input {
    flex: 1; background: var(--input-bg); border: 1px solid var(--input-border);
    color: var(--text); border-radius: var(--radius-control); padding: 14px 14px;
    font-size: 14px; outline: none; font-family: var(--font-body);
  }
  .search input::placeholder { color: var(--faint); }
  .search input:focus { border-color: var(--accent); box-shadow: 0 0 0 4px var(--focus-ring); }
  button {
    cursor: pointer; border: 0; border-radius: var(--radius-control);
    padding: var(--btn-pad, 12px 14px); background: var(--btn-bg); color: var(--btn-text);
    font-weight: 600; font-family: var(--font-body);
    transition: transform .18s var(--ease, ease), filter .18s, background .18s;
  }
  button:hover { filter: brightness(1.05); }
  button:active { transform: translateY(1px); }
  button.secondary { background: var(--btn2-bg); border: 1px solid var(--btn2-border); color: var(--text); }
  .selection { padding: 0 20px 14px; display: flex; gap: 8px; flex-wrap: wrap; }
  .selection .chip button {
    padding: 0; background: transparent; border: 0; margin-left: 8px;
    font-size: 12px; color: var(--accent-ink);
  }
  .content { padding: 16px 20px 20px; overflow: auto; }
  .content h2 {
    margin: 0 0 10px; font-size: 24px; line-height: 1.1;
    font-family: var(--font-display); font-weight: var(--display-weight, 700);
    letter-spacing: var(--display-tracking, -0.01em);
  }
  .content p.lead { margin: 0 0 16px; color: var(--muted); }
  .cards { display: grid; gap: 12px; }
  .card {
    background: var(--card-bg); border: 1px solid var(--card-border);
    border-radius: var(--radius-card); padding: 14px 14px;
    backdrop-filter: var(--card-blur, none); -webkit-backdrop-filter: var(--card-blur, none);
  }
  .card h3 { margin: 0 0 8px; font-size: 15px; color: var(--card-title); }
  .card ul { margin: 0; padding-left: 18px; color: var(--text); }
  .card li { margin: 0 0 6px; color: var(--card-text); }
  .list-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
  .list-chips .chip { cursor: pointer; transition: transform .15s ease, box-shadow .15s ease, background .15s ease; }
  .list-chips .chip:hover { transform: translateY(-1px); box-shadow: 0 0 0 1px var(--chip-border), 0 8px 20px var(--glow-soft); }
  .footer-note { padding: 12px 20px 18px; color: var(--muted); font-size: 12px; border-top: 1px solid var(--hairline); }
  .tooltip {
    position: fixed; z-index: 10; pointer-events: none;
    background: var(--tooltip-bg); border: 1px solid var(--tooltip-border);
    color: var(--tooltip-text); border-radius: 12px; padding: 10px 12px;
    font-size: 12px; box-shadow: var(--panel-shadow); max-width: 280px;
    opacity: 0; transform: translateY(6px); transition: opacity .12s ease, transform .12s ease;
    backdrop-filter: var(--panel-blur, none); -webkit-backdrop-filter: var(--panel-blur, none);
  }
  .tooltip.show { opacity: 1; transform: translateY(0); }
  .tt-sub { margin-top: 4px; color: var(--tooltip-sub); }
  .svg-label { font-size: 10px; fill: var(--label-fill); user-select: none; pointer-events: none; letter-spacing: 0.01em; }
  .svg-label.small { font-size: 8px; fill: var(--label-fill); opacity: .85; }
  .center-title { text-anchor: middle; fill: var(--center-title-fill); font-weight: 800; letter-spacing: .05em; font-family: var(--font-display); }
  .center-sub { text-anchor: middle; fill: var(--center-sub-fill); font-size: 12px; }
  .ring-segment { cursor: pointer; transition: filter .15s ease, transform .15s ease, opacity .15s ease; }
  .ring-segment.dim { opacity: var(--dim-opacity, 0.26); }
  .ring-segment.active {
    filter: drop-shadow(0 0 7px var(--glow-strong)) drop-shadow(0 0 16px var(--glow-soft)) brightness(var(--active-bright, 1.18));
  }
  .ring-segment.selected {
    filter: drop-shadow(0 0 10px var(--glow-strong)) drop-shadow(0 0 24px var(--glow-soft)) brightness(var(--selected-bright, 1.3));
  }
  .ring-segment:hover { filter: drop-shadow(0 0 10px var(--glow-soft)) brightness(1.12); }
  .grid-2 { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 12px; }
  .muted { color: var(--muted); }
  .tag {
    display: inline-block; background: var(--chip-bg); color: var(--chip-text);
    border: 1px solid var(--chip-border); padding: 4px 8px; border-radius: 999px;
    font-size: 11px; margin-right: 6px; margin-bottom: 6px;
  }
  @media (max-width: 1180px) {
    .wrap { grid-template-columns: 1fr; }
    #wheel { height: min(70vh, 860px); }
  }
  /* --- Touch / mobile / totem (aditivo) --- */
  #wheel { touch-action: manipulation; }
  .ring-segment { -webkit-tap-highlight-color: transparent; -webkit-touch-callout: none; }
  @media (hover: none) {
    .list-chips .chip:hover { transform: none; box-shadow: none; }
    .ring-segment:hover { filter: none; }
    .tooltip { display: none !important; }
  }
  @media (max-width: 720px) {
    .wrap { padding: 12px; gap: 12px; }
    .header { padding: 16px 16px 10px; }
    h1 { font-size: 22px; }
    .sub { font-size: 13px; }
    #wheel { height: min(86vw, 560px); }
    .toolbar { padding: 14px 14px 12px; }
    .search { flex-wrap: wrap; }
    .search input { flex: 1 1 100%; }
    .search button { flex: 1; }
    .content { padding: 14px 14px 18px; }
    .grid-2 { grid-template-columns: 1fr; }
    .list-chips .chip, .selection .chip { padding: 10px 14px; font-size: 13px; }
    button { padding: 14px 16px; }
  }
"""

# ---------------------------------------------------------------------------
# Tema A — site raiz (claro/quente, verde da marca, tipografia Grotesk)
# ---------------------------------------------------------------------------
TOKENS_A = r"""
  @import url('https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;600;700;800&family=Hanken+Grotesk:wght@400;500;600;700;800&display=swap');
  :root{
    --font-display:"Schibsted Grotesk", system-ui, sans-serif;
    --font-body:"Hanken Grotesk", system-ui, sans-serif;
    --font-label:"Hanken Grotesk", sans-serif;
    --display-weight:600; --display-tracking:-0.022em;
    --ease:cubic-bezier(.22,.61,.36,1);

    --page-bg:
      radial-gradient(circle at 18% 12%, rgba(47,158,94,.07), transparent 26%),
      radial-gradient(circle at 88% 8%, rgba(177,106,64,.05), transparent 22%),
      linear-gradient(180deg, #FBFAF5 0%, #F4F1E8 100%);
    --text:#16271E; --muted:#4A5A50; --faint:#7A857C;
    --accent:#2F9E5E; --accent-ink:#0B3D24;
    --hairline:rgba(20,40,30,.13);

    --panel-bg:#FFFFFF; --panel-border:rgba(20,40,30,.10);
    --panel-shadow:0 1px 2px rgba(16,40,30,.05), 0 30px 60px -34px rgba(16,40,30,.30);
    --panel-blur:none; --card-blur:none;

    --chip-bg:rgba(47,158,94,.10); --chip-border:rgba(47,158,94,.30); --chip-text:#0B3D24;
    --input-bg:#FFFFFF; --input-border:rgba(20,40,30,.18); --focus-ring:rgba(47,158,94,.16);
    --btn-bg:#16271E; --btn-text:#FFFFFF; --btn-pad:12px 16px;
    --btn2-bg:#FFFFFF; --btn2-border:rgba(20,40,30,.18);
    --card-bg:#FBFAF7; --card-border:rgba(20,40,30,.10); --card-title:#0B3D24; --card-text:#2B3A31;
    --tooltip-bg:#FFFFFF; --tooltip-border:rgba(20,40,30,.14); --tooltip-text:#16271E; --tooltip-sub:#4A5A50;

    --label-fill:#FFFFFF; --center-title-fill:#16271E; --center-sub-fill:#4A5A50;
    --glow-soft:rgba(47,158,94,.28); --glow-strong:rgba(47,158,94,.45);

    --radius-panel:26px; --radius-card:16px; --radius-control:12px; --radius-chip:999px;
    --h1-size:28px; --dim-opacity:0.22; --active-bright:1.16; --selected-bright:1.28;
  }
"""

WHEEL_A = {
    "base": "['#37A96D','#2F9E5E','#289257','#43B176','#23864E']",
    "glow": "#2F9E5E", "center": "#FFFFFF",
    "stops": ("#FFFFFF", "#F3F8F4", "#E9F1EB"),
    "centerStroke": "rgba(47,158,94,0.32)",
    "segStroke": "rgba(255,255,255,0.55)",
}

# ---------------------------------------------------------------------------
# Tema B — site v2 (azul/cinza da marca + padrões de interface da plataforma)
# fonte de sistema, materiais translúcidos, cantos amplos, cápsulas.
# ---------------------------------------------------------------------------
TOKENS_B = r"""
  :root{
    --font-display: system-ui, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    --font-body: system-ui, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    --font-label: system-ui, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    --display-weight:600; --display-tracking:-0.022em;
    --ease:cubic-bezier(.22,.61,.36,1);

    --page-bg:
      radial-gradient(circle at 16% 10%, rgba(4,79,139,.06), transparent 26%),
      radial-gradient(circle at 90% 6%, rgba(10,132,255,.05), transparent 22%),
      linear-gradient(180deg, #F8FAFC 0%, #EEF2F7 100%);
    --text:#172230; --muted:#4C5A68; --faint:#8A95A3;
    --accent:#044F8B; --accent-ink:#06335C;
    --hairline:rgba(18,42,78,.12);

    --panel-bg:rgba(255,255,255,.72); --panel-border:rgba(18,42,78,.10);
    --panel-shadow:0 1px 1px rgba(10,35,70,.04), 0 12px 34px -18px rgba(10,35,70,.28);
    --panel-blur:saturate(180%) blur(20px);
    --card-blur:saturate(160%) blur(12px);

    --chip-bg:rgba(4,79,139,.08); --chip-border:rgba(4,79,139,.18); --chip-text:#06335C;
    --input-bg:rgba(118,138,160,.14); --input-border:transparent; --focus-ring:rgba(4,79,139,.20);
    --btn-bg:#044F8B; --btn-text:#FFFFFF; --btn-pad:12px 18px;
    --btn2-bg:rgba(118,138,160,.16); --btn2-border:transparent;
    --card-bg:rgba(255,255,255,.66); --card-border:rgba(18,42,78,.08); --card-title:#06335C; --card-text:#2A3744;
    --tooltip-bg:rgba(255,255,255,.82); --tooltip-border:rgba(18,42,78,.12); --tooltip-text:#172230; --tooltip-sub:#4C5A68;

    --label-fill:#FFFFFF; --center-title-fill:#06335C; --center-sub-fill:#4C5A68;
    --glow-soft:rgba(10,132,255,.20); --glow-strong:rgba(10,132,255,.32);

    --radius-panel:22px; --radius-card:18px; --radius-control:12px; --radius-chip:999px;
    --h1-size:31px; --dim-opacity:0.24; --active-bright:1.10; --selected-bright:1.18;
  }
"""

# Refinos de interface da plataforma para B — aplicados DEPOIS do CSS base
# (precisam vencer a cascata). Controles em cápsula, eyebrow com mais tracking.
EXTRA_B = r"""
  /* controles em cápsula e tipografia da plataforma */
  button { border-radius: 999px; font-weight: 600; }
  .eyebrow { letter-spacing: .14em; font-weight: 600; }
  .selection .chip { padding: 7px 14px; }
"""
EXTRA_A = ""

WHEEL_B = {
    "base": "['#0A5FA6','#044F8B','#0B6BB5','#073F70','#1277C0']",
    "glow": "#0A84FF", "center": "#FFFFFF",
    "stops": ("#FFFFFF", "#F2F6FB", "#E7EEF6"),
    "centerStroke": "rgba(4,79,139,0.30)",
    "segStroke": "rgba(255,255,255,0.55)",
}

THEMES = {
    "A": {"tokens": TOKENS_A, "extra": EXTRA_A, "wheel": WHEEL_A, "out": os.path.join(REPO, "roda-ciclica.html")},
    "B": {"tokens": TOKENS_B, "extra": EXTRA_B, "wheel": WHEEL_B, "out": os.path.join(REPO, "v2", "roda-ciclica.html")},
}


def must_replace(text, old, new, label):
    if text.count(old) != 1:
        sys.exit("FALHA (%s): âncora aparece %d vezes." % (label, text.count(old)))
    return text.replace(old, new)


def build(theme_key):
    cfg = THEMES[theme_key]
    w = cfg["wheel"]
    with io.open(SRC, "r", encoding="utf-8") as f:
        html = f.read()

    # (a) substitui TODO o <style> pela folha do tema
    # ordem: tokens (:root) -> CSS base (geometria) -> refinos do tema (vencem a cascata)
    style = "<style>\n" + cfg["tokens"] + RODA_CSS + cfg["extra"] + "</style>"
    html = re.sub(r"<style>.*?</style>", lambda m: style, html, count=1, flags=re.S)

    # (b) cores do SVG por tema
    new_palette = (
        "const ringPalette = {\n"
        "  base: %s,\n"
        "  glow: '%s',\n"
        "  center: '%s'\n"
        "};" % (w["base"], w["glow"], w["center"])
    )
    html = re.sub(r"const ringPalette = \{.*?\};", lambda m: new_palette, html, count=1, flags=re.S)

    html = must_replace(
        html,
        '      <stop offset="0%" stop-color="#0f2a49"/>\n'
        '      <stop offset="75%" stop-color="#09192c"/>\n'
        '      <stop offset="100%" stop-color="#06111d"/>',
        '      <stop offset="0%%" stop-color="%s"/>\n'
        '      <stop offset="75%%" stop-color="%s"/>\n'
        '      <stop offset="100%%" stop-color="%s"/>' % w["stops"],
        "center gradient",
    )
    html = must_replace(html,
        "bgCircle.setAttribute('stroke', 'rgba(114,199,255,0.18)');",
        "bgCircle.setAttribute('stroke', '%s');" % w["centerStroke"], "center ring stroke")
    html = must_replace(html,
        "path.setAttribute('stroke', 'rgba(173,216,255,0.10)');",
        "path.setAttribute('stroke', '%s');" % w["segStroke"], "segment stroke")
    html = must_replace(html,
        '`<div style="margin-top:4px;color:#95acc5;">${sub}</div>`',
        '`<div class="tt-sub">${sub}</div>`', "tooltip sub")

    # (c) DATA externa + loader
    m = re.search(r"^const DATA = \{.*\};\s*$", html, flags=re.M)
    if not m:
        sys.exit("FALHA: linha 'const DATA = {...};' não encontrada.")
    loader = (
        "const DATA = window.RODA_DATA;\n"
        "if (!DATA) {\n"
        "  document.getElementById('content').innerHTML =\n"
        "    '<h2>Dados não carregados</h2><p class=\"lead\">O arquivo "
        "<code>roda-ciclica-data.js</code> não foi encontrado ao lado desta página. "
        "Rode <code>python tools/gerar_roda_data.py</code> para gerá-lo.</p>';\n"
        "  throw new Error('RODA_DATA ausente');\n"
        "}"
    )
    html = html[:m.start()] + loader + html[m.end():]
    html = must_replace(html,
        '<div id="tooltip" class="tooltip"></div>\n\n<script>',
        '<div id="tooltip" class="tooltip"></div>\n\n'
        '<script src="roda-ciclica-data.js"></script>\n<script>', "include data.js")

    # (d) lógica cíclica robusta
    new_enforce = """function enforceConsistency(lastChanged) {
  // Estádio e cultura precisam ser coerentes.
  if (state.stageId) {
    const stageCulture = DATA.stages.find(s => s.id === state.stageId)?.cultureId;
    if (stageCulture) {
      if (lastChanged === 'cultureId' && state.cultureId && state.cultureId !== stageCulture) {
        state.stageId = null;
      } else {
        state.cultureId = stageCulture;
      }
    }
  }
  const matches = () => DATA.relationships.some(rel =>
    (!state.cultureId || rel.cultureId === state.cultureId) &&
    (!state.stageId   || rel.stageId   === state.stageId) &&
    (!state.dorId     || rel.dorId     === state.dorId) &&
    (!state.productId || rel.productId === state.productId)
  );
  if (matches()) return;
  // A seleção recém-clicada é o novo foco e nunca é descartada.
  const order = ['productId', 'dorId', 'stageId', 'cultureId'];
  for (const key of order) {
    if (key === lastChanged) continue;
    if (!state[key]) continue;
    if (key === 'cultureId' && state.stageId) continue;
    state[key] = null;
    if (matches()) return;
  }
  if (!matches() && state.productId && state.cultureId &&
      DATA.cardProduto[`${state.productId}__${state.cultureId}`]) {
    return;
  }
}"""
    html = re.sub(
        r"function enforceConsistency\(lastChanged\) \{.*?\nfunction renderSelectionChips\(\) \{",
        lambda m2: new_enforce + "\n\nfunction renderSelectionChips() {",
        html, count=1, flags=re.S)

    # (e) anel vazio: banda fraca em vez de sumir
    html = must_replace(html,
        "  const step = 360 / total;\n",
        "  const step = 360 / total;\n"
        "  if (!items.length) {\n"
        "    const ph = document.createElementNS('http://www.w3.org/2000/svg', 'path');\n"
        "    ph.setAttribute('d', makeArcPath(450, 450, radiusInner, radiusOuter, 0.001, 359.999));\n"
        "    ph.setAttribute('fill', ringPalette.base[0]);\n"
        "    ph.setAttribute('opacity', selectionLabel().length ? '0.12' : '0.22');\n"
        "    group.appendChild(ph);\n"
        "    return group;\n"
        "  }\n",
        "empty ring guard")

    html = html.replace("Base carregada da planilha corrigida.",
                        "Base carregada de roda-ciclica-data.js (gerado da planilha).")

    out = cfg["out"]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with io.open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("[%s] escrito: %s (%d bytes)" % (theme_key, out, len(html.encode("utf-8"))))


if __name__ == "__main__":
    if not os.path.exists(SRC):
        sys.exit("Base visual não encontrada: %s" % SRC)
    build("A")
    build("B")
    print("ok")
