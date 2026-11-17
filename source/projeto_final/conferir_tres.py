# Projeto final: roda cada exemplo em Portugol (interpretador do site), Python (local) e C
# (Compiler Explorer, godbolt.org: envia so o codigo do exemplo e as entradas de teste),
# compara as saidas byte a byte e, se as tres baterem, grava saidas.json (usado pelo gerar.mjs).
# Uso: py -I conferir_tres.py            (precisa de node no PATH e de internet para o C)
#      py -I conferir_tres.py --sem-c    (nao grava: so confere Portugol x Python)
import datetime
import json
import os
import platform
import subprocess
import sys
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
SEM_C = "--sem-c" in sys.argv
COMPILADOR = ("cg141", "gcc 14.1 (Compiler Explorer)")

ENTRADAS = {
    "estoque": ["7", "3", "Caderno", "30", "10", "15.00", "Caneta azul", "8", "20", "2.50", "Mochila", "4", "2", "129.90"],
    "boletim": ["3", "Ana", "8.5", "7", "Bruno", "11", "5", "3.5", "Carla", "2", "4.5"],
    "orcamento": ["0", "4500", "1500", "980.50", "610", "520"],
    "lanchonete": ["1", "2", "7", "3", "2", "5", "1", "0", "50", "60"],
}


def portugol(nome):
    ent = os.path.join(AQUI, "_entradas.json")
    with open(ent, "w", encoding="utf-8") as f:
        json.dump(ENTRADAS[nome], f)
    try:
        out = subprocess.run(["node", os.path.join(AQUI, "rodar_portugol.js"), os.path.join(AQUI, nome + ".alg"), ent],
                             capture_output=True, text=True, encoding="utf-8", check=True).stdout
    finally:
        os.remove(ent)
    return json.loads(out)


def python(nome):
    r = subprocess.run([sys.executable, "-I", os.path.join(AQUI, nome + ".py")],
                       input="\n".join(ENTRADAS[nome]) + "\n", capture_output=True, text=True, encoding="utf-8")
    return r.stdout, r.stderr, r.returncode


def c(nome):
    with open(os.path.join(AQUI, nome + ".c"), encoding="utf-8") as f:
        fonte = f.read()
    corpo = {
        "source": fonte,
        "options": {
            "userArguments": "-O0 -Wall -std=c11",
            "executeParameters": {"args": [], "stdin": "\n".join(ENTRADAS[nome]) + "\n"},
            "compilerOptions": {"executorRequest": True},
            "filters": {"execute": True},
            "tools": [],
            "libraries": [],
        },
        "lang": "c",
        "allowStoreCodeDebug": False,
    }
    req = urllib.request.Request("https://godbolt.org/api/compiler/" + COMPILADOR[0] + "/compile",
                                 data=json.dumps(corpo).encode("utf-8"),
                                 headers={"Content-Type": "application/json", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        r = json.loads(resp.read().decode("utf-8"))
    saida = "\n".join(x["text"] for x in r.get("stdout", []))
    if r.get("stdout"):
        saida += "\n"
    avisos = "\n".join(x["text"] for x in r.get("buildResult", {}).get("stderr", []))
    return saida, avisos, r.get("code")


falhas = 0
saidas = {}
for nome in ENTRADAS:
    pt = portugol(nome)
    py_out, py_err, py_code = python(nome)
    ok = pt["erro"] is None and pt["erroTela"] is None and py_code == 0 and pt["saida"] == py_out
    linha = nome + ": Portugol x Python " + ("iguais" if pt["saida"] == py_out else "DIFERENTES")
    if py_code != 0:
        linha += " | Python parou: " + py_err.strip()[:200]
    if pt["erro"]:
        linha += " | Portugol parou: " + str(pt["erro"])
    if not SEM_C:
        c_out, c_avisos, c_code = c(nome)
        ok = ok and c_code == 0 and c_out == pt["saida"] and not c_avisos.strip()
        linha += " | C " + ("igual" if c_out == pt["saida"] else "DIFERENTE") + (" | avisos do compilador: " + c_avisos[:300] if c_avisos.strip() else " | sem avisos")
    print(linha)
    if not ok:
        falhas += 1
    saidas[nome] = {"entradas": ENTRADAS[nome], "saida": pt["saida"], "tela": pt["tela"]}

if falhas:
    print(str(falhas) + " exemplo(s) com diferenca: saidas.json NAO foi gravado")
    sys.exit(1)
if SEM_C:
    print("conferido sem o C: saidas.json NAO foi gravado (rode sem --sem-c)")
    sys.exit(0)
dados = {
    "conferido": {
        "data": datetime.date.today().strftime("%d/%m/%Y"),
        "portugol": "interpretador VisuAlg do site",
        "python": "Python " + platform.python_version(),
        "c": COMPILADOR[1],
    },
    "exemplos": saidas,
}
with open(os.path.join(AQUI, "saidas.json"), "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=1)
print("saidas.json gravado: " + str(len(saidas)) + " exemplos, as tres linguagens iguais")
