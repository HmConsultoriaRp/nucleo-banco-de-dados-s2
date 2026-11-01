# Varre os arquivos do lote lp_s34 atras de bytes de controle (exceto quebra de linha, retorno e tab)
# e confere que cada arquivo e UTF-8 valido e JSON valido.
import os, sys, json
sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(os.path.dirname(AQUI), "dados")
alvos = [os.path.join(DADOS, f) for f in sorted(os.listdir(DADOS)) if f.startswith("lp_s34_")]
alvos += [os.path.join(AQUI, f) for f in sorted(os.listdir(AQUI)) if f.startswith("lp_s34_")]
ruim = 0
for p in alvos:
    b = open(p, "rb").read()
    ctrl = [i for i, x in enumerate(b) if x < 0x20 and x not in (0x0A, 0x0D, 0x09)]
    try:
        t = b.decode("utf-8")
        utf = True
    except UnicodeDecodeError:
        utf = False
    js = "-"
    if p.endswith(".json") and utf:
        try:
            json.loads(t); js = "ok"
        except Exception as e:
            js = "ERRO"
    bom = b.startswith(b"\xef\xbb\xbf")
    print(os.path.basename(p), "bytes", len(b), "controle", len(ctrl), "utf8", utf, "bom", bom, "json", js)
    if ctrl or not utf or js == "ERRO" or bom:
        ruim += 1
print("OK" if not ruim else "PROBLEMA em %d arquivo(s)" % ruim)
