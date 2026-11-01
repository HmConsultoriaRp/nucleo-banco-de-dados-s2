# Le o journal do workflow e resume os relatorios dos revisores.
# Uso: python -I ler_relatorios.py <journal.jsonl> [--detalhe]
import json, sys

sys.stdout.reconfigure(encoding="utf-8")
detalhe = "--detalhe" in sys.argv
linhas = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
rotulo = {}
for l in linhas:
    if l.get("type") == "started":
        rotulo[l["key"]] = l.get("label")
vistos = {}
for l in linhas:
    if l.get("type") == "result" and str(rotulo.get(l["key"], "")).startswith("revisar:"):
        vistos[rotulo[l["key"]]] = l["result"]
for lab in sorted(vistos):
    r = vistos[lab]
    if not isinstance(r, dict):
        print(lab, "-> sem resultado", r)
        continue
    print(f"=== {lab}: {r.get('questoes')} questões, {r.get('conferidas_por_codigo')} conferidas por código, "
          f"{len(r.get('corrigidas', []))} correções, validador_ok={r.get('validador_ok')}")
    for p in r.get("problemas_abertos", []):
        print("  ABERTO:", p)
    if detalhe:
        for c in r.get("corrigidas", []):
            print(f"  - {c['id']}: {c['problema'][:160]}")
    print("  RESUMO:", r.get("resumo", "")[:500])
