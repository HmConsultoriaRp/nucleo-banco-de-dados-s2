# -*- coding: utf-8 -*-
# Revisor ga_s1: renderiza a pagina 1 da Lista 1 em alta resolucao e recorta
# a faixa dos hexagonos (Q6) e o paralelepipedo (Q5) para conferir as setas.
# Uso: python -I rev_ga_s1_render_pdf.py <pasta_saida>
import os, sys
import pypdfium2 as pdfium

sys.stdout.reconfigure(encoding="utf-8")
saida = sys.argv[1]
os.makedirs(saida, exist_ok=True)

base = r"D:\00_HM ConsultoriaEmpresarial\HM Consultoria_Clientes Ativos\Helio Marcos Hobus"
pasta = None
for nome in os.listdir(base):
    if nome.startswith("Geometria anal"):
        pasta = os.path.join(base, nome)
arq = None
for nome in os.listdir(pasta):
    if nome.startswith("Lista 1"):
        arq = os.path.join(pasta, nome)
print("PDF:", arq)

pdf = pdfium.PdfDocument(arq)
pg = pdf[0]
w, h = pg.get_size()
escala = 6
img = pg.render(scale=escala).to_pil()
print("tamanho", img.size, "pagina pt", w, h)
W, H = img.size
# faixa dos hexagonos: entre ~67% e ~80% da altura (na imagem de 1275 px de altura, 855 a 975)
fx = img.crop((int(W * 0.20), int(H * 0.665), int(W * 0.80), int(H * 0.785)))
fx.save(os.path.join(saida, "hexagonos.png"))
# cada hexagono separado
larg = fx.size[0]
for i in range(5):
    x0 = int(larg * i / 5)
    x1 = int(larg * (i + 1) / 5)
    fx.crop((x0, 0, x1, fx.size[1])).save(os.path.join(saida, f"hex_{'abcde'[i]}.png"))
# paralelepipedo
pp = img.crop((int(W * 0.37), int(H * 0.45), int(W * 0.63), int(H * 0.63)))
pp.save(os.path.join(saida, "paralelepipedo.png"))
print("ok")
