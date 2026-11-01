# Revisor adversarial - lote ga_s3: forma e voz.
# Conta palavras (teoria e jeitos), procura travessao, decimal com ponto no texto,
# hifen como menos, expressoes proibidas e frases parecidas entre jeitos.
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
PASTA = r"D:\00_HM ConsultoriaEmpresarial\HM Consultoria_Clientes Ativos\Helio Marcos Hobus\Site Estudo Banco de Dados\Claude\_gerador\dados"
PROIBIDAS = ["vamos lá", "ótima pergunta", "excelente", "mergulh", "desvend", "jornada", "fascinante",
             "crucial", "é importante notar", "em resumo", "basicamente", "simplesmente"]
avisos = []


def npal(s):
    return len(re.findall(r"\S+", s))


def textos(q):
    yield "enunciado", q["enunciado"]
    yield "dica", q["dica"]
    yield "resposta", q["resposta"]
    for i, a in enumerate(q["alternativas"]):
        yield f"alt{'ABCDE'[i]}.t", a["t"]
        if "erro" in a:
            yield f"alt{'ABCDE'[i]}.erro", a["erro"]
    for k, v in q["jeitos"].items():
        if isinstance(v, str):
            yield k, v
        elif k == "receita":
            for i, p in enumerate(v):
                yield f"receita[{i}]", p
        else:
            for i, c in enumerate(v):
                yield f"conversa[{i}]", c["fala"]
    if "figura" in q:
        yield "legenda", q["figura"].get("legenda", "")


def checa(onde, s):
    t = re.sub(r"`[^`]*`", " ", s)
    low = t.lower()
    for p in PROIBIDAS:
        if p in low:
            avisos.append(f"{onde}: proibida '{p}'")
    if "!" in t:
        avisos.append(f"{onde}: exclamação")
    if "—" in t:
        avisos.append(f"{onde}: travessão")
    if re.search(r"\d\.\d", t):
        avisos.append(f"{onde}: decimal com ponto: {re.findall(r'[0-9.]*[0-9][.][0-9]+', t)}")
    if re.search(r"(^|[\s(,\[=])-\d", t):
        avisos.append(f"{onde}: hífen como menos")
    if re.search(r"\b(o professor|professor disse|slide|página)\b", low):
        avisos.append(f"{onde}: cita professor/slide/página")


for nome in sorted(os.listdir(PASTA)):
    if not re.fullmatch(r"ga_s3_p\d\.json", nome):
        continue
    d = json.load(open(os.path.join(PASTA, nome), encoding="utf-8"))
    for s in d["semanas"]:
        for i, b in enumerate(s["blocos"]):
            n = npal(b["texto"])
            print(f"{nome} semana bloco {i}: {n} palavras")
            if not 40 <= n <= 120:
                avisos.append(f"{nome} bloco {i}: {n} palavras (40 a 120)")
            checa(f"{nome} bloco {i}", b["texto"])
        for k, v in s["jeitos"].items():
            n = npal(v)
            print(f"{nome} semana jeito {k}: {n} palavras")
            if not 50 <= n <= 120:
                avisos.append(f"{nome} jeito semana {k}: {n} palavras (50 a 120)")
            checa(f"{nome} semana {k}", v)
        for f in s["formulas"]:
            checa(f"{nome} formula {f['nome']}", f["expr"] + " " + f["quando"])
        checa(f"{nome} chamada", s["chamada"])
        checa(f"{nome} lab", s["lab"])
    for q in d["questoes"]:
        for onde, s in textos(q):
            checa(f"{q['id']}.{onde}", s)
        for k in ["visual", "cotidiano", "trabalho", "erro", "confira", "atalho"]:
            n = npal(q["jeitos"][k])
            if not 35 <= n <= 110:
                avisos.append(f"{q['id']}.{k}: {n} palavras (35 a 110)")
        r = q["jeitos"]["receita"]
        c = q["jeitos"]["conversa"]
        if not 3 <= len(r) <= 7:
            avisos.append(f"{q['id']}: receita com {len(r)} passos")
        if not 4 <= len(c) <= 8:
            avisos.append(f"{q['id']}: conversa com {len(c)} falas")
        # frases curtas: media de palavras por frase nos jeitos de texto
        tudo = " ".join(q["jeitos"][k] for k in ["visual", "cotidiano", "trabalho", "erro", "confira", "atalho"])
        frases = [f for f in re.split(r"(?<=[.?:;])\s+", tudo) if f.strip()]
        longas = [f for f in frases if npal(f) > 35]
        for f in longas:
            avisos.append(f"{q['id']}: frase longa ({npal(f)} palavras): {f[:70]}...")

print()
print("Tamanho das alternativas (caracteres sem [[ ]]); * = certa")
maiores = 0
total_q = 0
for nome in sorted(os.listdir(PASTA)):
    if not re.fullmatch(r"ga_s3_p\d\.json", nome):
        continue
    d = json.load(open(os.path.join(PASTA, nome), encoding="utf-8"))
    for q in d["questoes"]:
        tam = [len(a["t"].replace("[[", "").replace("]]", "")) for a in q["alternativas"]]
        ic = [i for i, a in enumerate(q["alternativas"]) if a.get("certa")][0]
        total_q += 1
        rank = sorted(tam, reverse=True).index(tam[ic]) + 1
        if rank == 1 and tam[ic] > 1.25 * sorted(tam, reverse=True)[1]:
            maiores += 1
            avisos.append(f"{q['id']}: certa é a mais longa com folga {tam}")
        print(f"  {q['id']}: " + " ".join(f"{'*' if i == ic else ''}{t}" for i, t in enumerate(tam)) + f"  (posição de tamanho da certa: {rank})")

print()
print("AVISOS:", len(avisos))
for a in avisos:
    print(" -", a)
