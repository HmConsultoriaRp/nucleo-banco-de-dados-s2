# Monta o site Nucleo num unico HTML (CSS e JS embutidos, abre com duplo clique).
# Uso: python -I gerar.py "<caminho do html de saida>"
import json, os, re, sys, datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(AQUI, "site")
DADOS = os.path.join(AQUI, "dados")
INICIO = "2026-10-26"   # segunda-feira da semana em que a Geometria comecou (aula de 27/10/2026)


def ler(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def chave_natural(s):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)]


def ordem_origem(q):
    o = q.get("origem", "")
    if o.startswith("Lista"):
        return 0
    if o.startswith("Constru"):
        return 1
    return 2


def main(saida):
    disc = {"ga": {"semanas": {}, "questoes": []}, "lp": {"semanas": {}, "questoes": []}}
    ids = set()
    for nome in sorted(os.listdir(DADOS)):
        if not nome.endswith(".json"):
            continue
        d = json.loads(ler(os.path.join(DADOS, nome)))
        alvo = disc[d["disciplina"]]
        for s in d.get("semanas", []):
            if s["semana"] in alvo["semanas"]:
                raise SystemExit(f"semana {s['semana']} de {d['disciplina']} definida duas vezes ({nome})")
            alvo["semanas"][s["semana"]] = s
        for q in d.get("questoes", []):
            if q["id"] in ids:
                raise SystemExit(f"id repetido: {q['id']} ({nome})")
            ids.add(q["id"])
            alvo["questoes"].append(q)
    for k, v in disc.items():
        v["questoes"].sort(key=lambda q: (q["semana"], ordem_origem(q), chave_natural(q["id"])))
        v["semanas"] = [v["semanas"][s] for s in sorted(v["semanas"])]

    exs = json.loads(ler(os.path.join(AQUI, "exemplos_visualg.json")))["questoes"]
    exemplos = [{"titulo": e["titulo"], "semana": e["semana"], "codigo": e["codigo"], "entradas": e["entradas"]} for e in exs]

    agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    dados = {"geradoEm": agora, "inicio": INICIO, "disc": disc, "exemplosVisualg": exemplos}
    js_dados = "window.NUCLEO = " + json.dumps(dados, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + ";"

    html = ler(os.path.join(SITE, "template.html"))
    css = ler(os.path.join(SITE, "styles.css"))
    js = "\n".join(ler(os.path.join(SITE, f)) for f in ("visualg.js", "figura.js", "app.js"))
    for marca, conteudo in (("/*__CSS__*/", css), ("/*__DADOS__*/", js_dados), ("/*__JS__*/", js.replace("</script", "<\\/script"))):
        assert html.count(marca) == 1, marca
        html = html.replace(marca, conteudo)
    with open(saida, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)

    print("gerado:", saida, f"({len(html.encode('utf-8')) // 1024} KB)")
    for k, v in disc.items():
        por = {}
        for q in v["questoes"]:
            por.setdefault(q["semana"], [0, 0, 0])[q["nivel"] - 1] += 1
        print(k, "semanas com teoria:", [s["semana"] for s in v["semanas"]], "| questões por semana (básico, médio, avançado):", dict(sorted(por.items())), "| total", len(v["questoes"]))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2:
        raise SystemExit("uso: python -I gerar.py <html de saida>")
    main(sys.argv[1])
