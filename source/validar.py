# Validador dos arquivos de conteudo do site Nucleo.
# Uso: python -I validar.py arquivo1.json [arquivo2.json ...]
# Sai "OK" quando nao ha ERRO. AVISO nao bloqueia, mas vale olhar.
import json, re, sys
from collections import Counter

LENTES_TXT = ["visual", "cotidiano", "trabalho", "erro", "confira", "atalho"]
LENTES = LENTES_TXT + ["receita", "conversa"]
SEM_JEITOS = ["visual", "cotidiano", "receita", "trabalho", "erro"]

PROIBIDAS = ["vamos lá", "vamos la", "ótima pergunta", "excelente", "mergulh", "desvend",
             "jornada", "fascinante", "crucial", "é importante notar", "em resumo",
             "basicamente", "simplesmente"]
SEM_ACENTO = ["nao", "voce", "voces", "questao", "questoes", "explicacao", "resolucao",
              "solucao", "tambem", "numero", "numeros", "possivel", "unico", "unica",
              "analise", "calculo", "sera", "informacao", "formula", "angulo", "triangulo",
              "distancia", "equacao", "operacao", "proximo", "proxima", "ja", "so",
              "e possivel", "logica", "funcao", "vetorial e"]
# palavras que tambem sao comandos do VisuAlg: fora de crase, so aviso
SEM_ACENTO_AVISO = ["entao", "ate", "logico", "senao", "faca"]
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-⛿✀-➿]")

erros, avisos = [], []

def tira_codigo(s):
    s = re.sub(r"`[^`]*`", " ", s)
    # termo ligado {{id|texto}}: o id é código (pode ter "unico" sem acento); confere só o texto
    return re.sub(r"\{\{[a-z0-9-]+\|([^}]*)\}\}", r"\1", s)

def checa_texto(onde, s, matematica=True):
    if not isinstance(s, str) or not s.strip():
        erros.append(f"{onde}: texto vazio")
        return
    t = tira_codigo(s)
    if s.count("`") % 2:
        erros.append(f"{onde}: crase sem par")
    if s.count("**") % 2:
        erros.append(f"{onde}: ** sem par")
    if s.count("[[") != s.count("]]"):
        erros.append(f"{onde}: [[ ]] sem par")
    if re.search(r"<[a-zA-Z/]", t):
        erros.append(f"{onde}: parece tag HTML")
    if "\\(" in t or "\\frac" in t or re.search(r"(?<!R)\$", t):
        erros.append(f"{onde}: parece LaTeX")
    if "!" in t:
        avisos.append(f"{onde}: ponto de exclamação")
    if EMOJI.search(t):
        erros.append(f"{onde}: emoji")
    low = t.lower()
    for p in PROIBIDAS:
        if p in low:
            erros.append(f"{onde}: expressão proibida '{p}'")
    palavras = re.findall(r"[a-zà-ú]+", low)
    for w in SEM_ACENTO:
        if " " in w:
            if w in low:
                avisos.append(f"{onde}: possível falta de acento '{w}'")
        elif w in palavras:
            erros.append(f"{onde}: palavra sem acento '{w}'")
    for w in SEM_ACENTO_AVISO:
        if w in palavras:
            avisos.append(f"{onde}: '{w}' fora de crase (comando do VisuAlg vai entre crases; no texto, com acento)")
    if matematica and re.search(r"(^|[\s(,\[=])-\d", t):
        avisos.append(f"{onde}: hífen usado como sinal de menos (use −)")

def n_palavras(s):
    return len(re.findall(r"\S+", s))

def checa_figura(onde, f):
    if not isinstance(f, dict):
        erros.append(f"{onde}: figura não é objeto"); return
    if f.get("modo") not in ("2d", "3d"):
        erros.append(f"{onde}: figura.modo deve ser 2d ou 3d")
    if f.get("onde") not in ("enunciado", "explicacao"):
        erros.append(f"{onde}: figura.onde deve ser enunciado ou explicacao")
    itens = f.get("itens")
    if not isinstance(itens, list) or not itens:
        erros.append(f"{onde}: figura sem itens"); return
    def coord(c):
        return isinstance(c, list) and len(c) in (2, 3) and all(isinstance(x, (int, float)) for x in c)
    for i, it in enumerate(itens):
        tp = it.get("tipo")
        if tp == "vetor" or tp == "segmento":
            if not (coord(it.get("de")) and coord(it.get("ate"))):
                erros.append(f"{onde}: figura item {i} ({tp}) com coordenada inválida")
        elif tp == "ponto":
            if not coord(it.get("em")):
                erros.append(f"{onde}: figura item {i} (ponto) com coordenada inválida")
        elif tp == "poligono":
            pts = it.get("pts")
            if not (isinstance(pts, list) and len(pts) >= 3 and all(coord(p) for p in pts)):
                erros.append(f"{onde}: figura item {i} (poligono) inválido")
        else:
            erros.append(f"{onde}: figura item {i} tipo desconhecido '{tp}'")
        if "cor" in it and it["cor"] not in (1, 2, 3, 4):
            erros.append(f"{onde}: figura item {i} cor fora de 1..4")
    if "legenda" in f:
        checa_texto(onde + ".figura.legenda", f["legenda"])

def checa_tabela(onde, t):
    if not isinstance(t, dict) or not isinstance(t.get("cab"), list) or not isinstance(t.get("linhas"), list):
        erros.append(f"{onde}: tabela precisa de cab e linhas"); return
    if t.get("onde") not in ("enunciado", "explicacao"):
        erros.append(f"{onde}: tabela.onde deve ser enunciado ou explicacao")
    for i, l in enumerate(t["linhas"]):
        if not isinstance(l, list) or len(l) != len(t["cab"]):
            erros.append(f"{onde}: tabela linha {i} com número de colunas diferente do cabeçalho")

def checa_semana(arq, s):
    onde = f"{arq}:semana {s.get('semana')}"
    for k in ["semana", "titulo", "chamada", "fonte", "previa", "blocos", "formulas", "jeitos", "lab"]:
        if k not in s:
            erros.append(f"{onde}: falta '{k}'")
    if not isinstance(s.get("blocos"), list) or not (3 <= len(s.get("blocos", [])) <= 6):
        erros.append(f"{onde}: blocos deve ter 3 a 6")
    for i, b in enumerate(s.get("blocos", []) or []):
        checa_texto(f"{onde}.blocos[{i}].texto", b.get("texto", ""))
    for i, f in enumerate(s.get("formulas", []) or []):
        for k in ("nome", "expr", "quando"):
            if not f.get(k):
                erros.append(f"{onde}.formulas[{i}]: falta {k}")
    j = s.get("jeitos", {}) or {}
    for k in SEM_JEITOS:
        if k not in j:
            erros.append(f"{onde}: jeitos da semana sem '{k}'")
        else:
            checa_texto(f"{onde}.jeitos.{k}", j[k])

def checa_questao(arq, q, disc):
    qid = q.get("id", "?")
    onde = f"{arq}:{qid}"
    for k in ["id", "semana", "nivel", "minutos", "tema", "origem", "enunciado", "alternativas", "dica", "resposta", "jeitos"]:
        if k not in q:
            erros.append(f"{onde}: falta '{k}'")
    sem = q.get("semana")
    if not isinstance(sem, int) or not 1 <= sem <= 6:
        erros.append(f"{onde}: semana inválida")
    # Questao de avaliacao pode mudar de semana sem trocar o id: o progresso salvo no navegador usa o id.
    elif disc in ("ga", "lp") and not str(qid).startswith(f"{disc}-s{sem}-") and not (
            str(q.get("origem", "")).startswith("Avaliação") and re.match(rf"{disc}-s\d+-", str(qid))):
        erros.append(f"{onde}: id deve começar com '{disc}-s{sem}-'")
    if q.get("nivel") not in (1, 2, 3):
        erros.append(f"{onde}: nivel deve ser 1, 2 ou 3")
    if not isinstance(q.get("minutos"), int) or not 1 <= q.get("minutos", 0) <= 10:
        erros.append(f"{onde}: minutos inválido")
    org = q.get("origem", "")
    if not (re.fullmatch(r"Lista [1-8] · Q\d+[a-z]?", org) or
            re.fullmatch(r"Avaliação semanal \d+ · T\d+(?:-Q\d+)? · Q\d+", org) or
            re.fullmatch(r"Avaliação · Semana \d+(?: e \d+)? · T\d+(?:-Q\d+)? · Q\d+", org) or
            org in ("Construída · conferida", "Prévia · ementa")):
        erros.append(f"{onde}: origem fora do padrão: '{org}'")
    tem_codigo = bool(q.get("codigo"))
    checa_texto(onde + ".enunciado", q.get("enunciado", ""), matematica=not tem_codigo)
    alts = q.get("alternativas", [])
    if not isinstance(alts, list) or len(alts) != 5:
        erros.append(f"{onde}: precisa de exatamente 5 alternativas")
    else:
        certas = [a for a in alts if a.get("certa") is True]
        if len(certas) != 1:
            erros.append(f"{onde}: precisa de exatamente 1 alternativa certa (tem {len(certas)})")
        textos = [str(a.get("t", "")).strip() for a in alts]
        if len(set(textos)) != 5:
            erros.append(f"{onde}: alternativas repetidas")
        for i, a in enumerate(alts):
            if not str(a.get("t", "")).strip():
                erros.append(f"{onde}: alternativa {i} vazia")
            if a.get("certa") is not True:
                if not a.get("erro"):
                    erros.append(f"{onde}: alternativa {'ABCDE'[i]} errada sem 'erro'")
                else:
                    checa_texto(f"{onde}.alt{'ABCDE'[i]}.erro", a["erro"], matematica=not tem_codigo)
    checa_texto(onde + ".dica", q.get("dica", ""), matematica=not tem_codigo)
    j = q.get("jeitos", {}) or {}
    for k in LENTES:
        if k not in j:
            erros.append(f"{onde}: jeitos sem '{k}'")
    for k in LENTES_TXT:
        if k in j:
            checa_texto(f"{onde}.jeitos.{k}", j[k], matematica=not tem_codigo)
            n = n_palavras(j[k])
            if n < 25 or n > 140:
                avisos.append(f"{onde}.jeitos.{k}: {n} palavras (alvo 35 a 110)")
    rec = j.get("receita")
    if not isinstance(rec, list) or not 3 <= len(rec) <= 8:
        erros.append(f"{onde}: receita deve ser lista de 3 a 7 passos")
    else:
        for i, p in enumerate(rec):
            checa_texto(f"{onde}.receita[{i}]", p, matematica=not tem_codigo)
    conv = j.get("conversa")
    if not isinstance(conv, list) or not 4 <= len(conv) <= 8:
        erros.append(f"{onde}: conversa deve ter 4 a 8 falas")
    else:
        for i, c in enumerate(conv):
            if c.get("quem") not in ("Você", "Monitor"):
                erros.append(f"{onde}: conversa[{i}].quem deve ser 'Você' ou 'Monitor'")
            checa_texto(f"{onde}.conversa[{i}]", c.get("fala", ""), matematica=not tem_codigo)
    vistos = Counter()
    for k in LENTES_TXT:
        for frase in re.split(r"(?<=[.?])\s+", str(j.get(k, ""))):
            f = frase.strip().lower()
            if len(f) > 40:
                vistos[f] += 1
    for f, c in vistos.items():
        if c > 1:
            erros.append(f"{onde}: frase repetida entre jeitos: '{f[:60]}...'")
    if "figura" in q and q["figura"] is not None:
        if disc == "lp":
            avisos.append(f"{onde}: figura em questão de Lógica")
        checa_figura(onde, q["figura"])
    if tem_codigo:
        if not isinstance(q.get("saida"), str):
            erros.append(f"{onde}: código sem 'saida'")
        if not isinstance(q.get("entradas", []), list):
            erros.append(f"{onde}: entradas deve ser lista")
        c = q["codigo"].lower()
        if not c.strip().startswith("algoritmo"):
            erros.append(f"{onde}: código deve começar com algoritmo")
        if "fimalgoritmo" not in c:
            erros.append(f"{onde}: código sem fimalgoritmo")
        for ruim in ("procedimento", "funcao ", "função ", "aleatorio", "cronometro", "arquivo "):
            if ruim in c:
                erros.append(f"{onde}: código usa '{ruim.strip()}', fora do subconjunto")
        if re.search(r"escreva?l?\s*\([^)]*:\s*\d", c):
            erros.append(f"{onde}: código usa formatação x:n, fora do subconjunto")
    if "tabela" in q and q["tabela"] is not None:
        checa_tabela(onde, q["tabela"])

def main(paths):
    todos_ids = Counter()
    pos = Counter()
    total = 0
    for p in paths:
        try:
            with open(p, encoding="utf-8") as f:
                d = json.load(f)
        except Exception as e:
            erros.append(f"{p}: JSON inválido: {e}")
            continue
        arq = p.replace("\\", "/").split("/")[-1]
        disc = d.get("disciplina")
        if disc not in ("ga", "lp", "exemplos"):
            erros.append(f"{arq}: disciplina deve ser 'ga' ou 'lp'")
        for s in d.get("semanas", []):
            checa_semana(arq, s)
        qs = d.get("questoes", [])
        if len(qs) > 8:
            avisos.append(f"{arq}: {len(qs)} questões num arquivo (combinado: até 6)")
        for q in qs:
            total += 1
            todos_ids[q.get("id")] += 1
            checa_questao(arq, q, disc)
            for i, a in enumerate(q.get("alternativas", [])):
                if a.get("certa") is True:
                    pos["ABCDE"[i]] += 1
    for i, c in todos_ids.items():
        if c > 1:
            erros.append(f"id repetido: {i}")
    if total >= 10:
        for letra, c in pos.items():
            if c / total > 0.30:
                avisos.append(f"letra {letra} é a certa em {c} de {total} questões (acima de 30%)")
    for a in avisos:
        print("AVISO", a)
    for e in erros:
        print("ERRO ", e)
    print(f"{total} questões; posições das certas: {dict(sorted(pos.items()))}")
    print("OK" if not erros else f"FALHOU: {len(erros)} erro(s)")
    return 0 if not erros else 1

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
