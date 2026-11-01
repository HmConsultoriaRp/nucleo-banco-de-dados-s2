# -*- coding: utf-8 -*-
# Confere os tamanhos combinados no BRIEF para o lote ga_s1:
# jeitos de texto 35 a 110 palavras; receita 3 a 7 passos; conversa 4 a 8 falas;
# blocos da teoria 40 a 120 palavras; jeitos da teoria 50 a 120 palavras.
# Uso: python -I ga_s1_palavras.py
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(os.path.dirname(AQUI), "dados")


def np(s):
    return len(re.findall(r"\S+", s))


fora = []
for nome in sorted(f for f in os.listdir(DADOS) if f.startswith("ga_s1_p") and f.endswith(".json")):
    with open(os.path.join(DADOS, nome), encoding="utf-8") as fh:
        d = json.load(fh)
    for s in d["semanas"]:
        for b in s["blocos"]:
            n = np(b["texto"])
            if not 40 <= n <= 120:
                fora.append(f"{nome} bloco '{b['titulo']}': {n}")
        for kk, t in s["jeitos"].items():
            n = np(t)
            if not 50 <= n <= 120:
                fora.append(f"{nome} teoria.{kk}: {n}")
    for q in d["questoes"]:
        j = q["jeitos"]
        for kk in ["visual", "cotidiano", "trabalho", "erro", "confira", "atalho"]:
            n = np(j[kk])
            if not 35 <= n <= 110:
                fora.append(f"{q['id']}.{kk}: {n}")
        if not 3 <= len(j["receita"]) <= 7:
            fora.append(f"{q['id']}.receita: {len(j['receita'])} passos")
        if not 4 <= len(j["conversa"]) <= 8:
            fora.append(f"{q['id']}.conversa: {len(j['conversa'])} falas")
for f in fora:
    print("FORA", f)
print("OK" if not fora else f"{len(fora)} fora do alvo")
