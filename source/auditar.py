# Auditor de cobertura: confere se todo item das Listas 1-3 do Prof. Danilo virou questao,
# e mostra a distribuicao por semana e nivel e a posicao da alternativa certa.
# Uso: python -I auditar.py
import json, os, sys
from collections import Counter, defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(AQUI, "dados")

ESPERADO = {
    "Lista 1": ["1a", "1b", "1c", "1d", "2", "3", "4", "5a", "5b", "6a", "6b", "6c", "6d", "6e", "7", "8a", "8b",
                "9a", "9b", "9c", "9d", "9e", "10a", "10b", "10c"],
    "Lista 2": ["1" + c for c in "abcdefghijklmn"] + ["2", "3", "4", "5a", "5b", "6", "7", "8", "9a", "9b", "9c", "10", "11",
                                                     "12a", "12b", "12c", "12d"],
    "Lista 3": ["1a", "1b", "1c", "2", "3", "4"] + ["5" + c for c in "abcdefghij"],
    "Lista 4": ["1a", "1b", "1c", "2", "3", "4", "5", "6", "7"],
    "Lista 5": ["1a", "1b", "1c", "2", "3", "4", "5", "6", "7", "8", "9"],
    "Lista 6": ["1", "2", "3", "4", "5a", "5b"] + ["6" + c for c in "abcdef"] + ["7", "8", "9", "10a", "10b"],
    "Lista 7": ["1" + c for c in "abcdef"] + ["2", "3", "4", "5", "6", "7", "8"],
    "Lista 8": ["1" + c for c in "abcdefghi"] + ["2", "3a", "3b", "4", "5", "6", "7", "8"] +
               ["9" + c for c in "abcdefghij"] + ["10" + c for c in "abcdefghij"] + ["11"],
}


def main():
    qs = []
    for nome in sorted(os.listdir(DADOS)):
        if nome.endswith(".json"):
            with open(os.path.join(DADOS, nome), encoding="utf-8") as f:
                d = json.load(f)
            for q in d["questoes"]:
                q["_disc"] = d["disciplina"]
                qs.append(q)
    ok = True
    vistos = Counter(q["origem"] for q in qs)
    for lista, itens in ESPERADO.items():
        faltam = [i for i in itens if vistos[f"{lista} · Q{i}"] == 0]
        dup = [i for i in itens if vistos[f"{lista} · Q{i}"] > 1]
        n = sum(1 for i in itens if vistos[f"{lista} · Q{i}"])
        print(f"{lista}: {n}/{len(itens)} itens com questão" + (f" | FALTAM {faltam}" if faltam else "") + (f" | REPETIDOS {dup}" if dup else ""))
        ok = ok and not faltam and not dup
    extras = [o for o in vistos if o.startswith("Lista") and o.split(" · Q")[1] not in ESPERADO.get(o.split(" · ")[0], [])]
    if extras:
        print("Origem de lista que não existe no PDF:", extras)
        ok = False
    tab = defaultdict(lambda: [0, 0, 0])
    pos = Counter()
    cod = Counter()
    for q in qs:
        tab[(q["_disc"], q["semana"])][q["nivel"] - 1] += 1
        for i, a in enumerate(q["alternativas"]):
            if a.get("certa"):
                pos["ABCDE"[i]] += 1
        if q.get("codigo"):
            cod[q["_disc"]] += 1
    print("\nPor semana (básico, médio, avançado):")
    for k in sorted(tab):
        print(f"  {k[0]} S{k[1]}: {tab[k]} = {sum(tab[k])}")
    print("\nTotal:", len(qs), "| com código VisuAlg:", dict(cod), "| posição da certa:", dict(sorted(pos.items())))
    print("\nCOBERTURA OK" if ok else "\nCOBERTURA COM FALHA")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
