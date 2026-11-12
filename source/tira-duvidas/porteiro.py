"""Ponte entre a atividade na nuvem do Tira-duvidas e o porteiro (Apps Script).

Uso, sempre a partir da raiz do repositorio e exatamente assim (sao os dois
unicos comandos liberados em .claude/settings.json):

    python3 source/tira-duvidas/porteiro.py pendentes
    python3 source/tira-duvidas/porteiro.py responder

A senha vem da variavel de ambiente NUCLEO_CHAVE. So este programa a usa;
ele nunca a imprime nem a grava. Ele so fala com o endereco URL abaixo.

Pasta da rodada (fora do git, ver .gitignore): rodada-tira-duvidas/
    pendentes.json        escrito por "pendentes"
    imagens/<id>.png|jpg  prints das duvidas
    respostas/<id>.json   escritos pela atividade: {"id", "status", "transcricao", "resposta"}
    enviadas/<id>.json    respostas que o porteiro aceitou
"""
import base64
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request

URL = "https://script.google.com/macros/s/AKfycbyjUWCd3Zj4cpITJxpE8DoygjSrt87cKzhVRWWOPEKkNkFWVJcyOs0sIjzs1KprkdCf/exec"
RAIZ = pathlib.Path(__file__).resolve().parents[2]
RODADA = RAIZ / "rodada-tira-duvidas"
LIMITE = 10
STATUS = ("respondida", "fora_do_tema", "sem_resposta")
ID_OK = re.compile(r"^D\d{4,}$")
MAX_TRANSCRICAO = 2000
MAX_RESPOSTA = 6000


def chave():
    c = os.environ.get("NUCLEO_CHAVE", "")
    if not c:
        sys.exit("NUCLEO_CHAVE ausente no ambiente: pare a rodada e registre o problema.")
    return c


def post(dados):
    req = urllib.request.Request(URL, data=json.dumps(dados).encode("utf-8"),
                                 headers={"Content-Type": "text/plain;charset=utf-8"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, ValueError) as e:
        # So o tipo do erro: a mensagem nunca leva o corpo do pedido (onde esta a senha).
        return {"ok": False, "erro": "falha de rede ou resposta invalida (" + type(e).__name__ + ")"}


def pendentes():
    j = post({"acao": "pendentes", "chave": chave(), "limite": LIMITE})
    if not j.get("ok"):
        sys.exit("erro do porteiro: " + str(j.get("erro")))
    (RODADA / "imagens").mkdir(parents=True, exist_ok=True)
    (RODADA / "respostas").mkdir(exist_ok=True)
    itens = []
    for it in j.get("itens", []):
        if not ID_OK.match(str(it.get("id", ""))):
            continue
        if it.get("imagem"):
            ext = ".png" if it.get("tipoImagem") == "image/png" else ".jpg"
            p = RODADA / "imagens" / (it["id"] + ext)
            p.write_bytes(base64.b64decode(it["imagem"]))
            it["imagem"] = p.relative_to(RAIZ).as_posix()
        else:
            it["imagem"] = ""
        it.pop("tipoImagem", None)
        itens.append(it)
    (RODADA / "pendentes.json").write_text(json.dumps(itens, ensure_ascii=False, indent=2), encoding="utf-8")
    lista = ", ".join(i["id"] + (" (com print)" if i["imagem"] else "") for i in itens)
    print(len(itens), "pendente(s):", lista or "nenhuma")
    print("Detalhes em rodada-tira-duvidas/pendentes.json")


def problema_de(arq, r, validos, c):
    rid = str(r.get("id", ""))
    if rid not in validos:
        return "id fora das pendentes desta rodada"
    if arq.stem != rid:
        return "o nome do arquivo deve ser <id>.json"
    if r.get("status") not in STATUS:
        return "status invalido (use respondida, fora_do_tema ou sem_resposta)"
    if not str(r.get("resposta", "")).strip():
        return "resposta vazia"
    for campo in ("transcricao", "resposta"):
        if c in str(r.get(campo, "")):
            return "BLOQUEADO: o texto continha a senha"
    return None


def responder():
    c = chave()
    arq_pend = RODADA / "pendentes.json"
    if not arq_pend.exists():
        sys.exit("Rode antes: python3 source/tira-duvidas/porteiro.py pendentes")
    validos = {str(i.get("id", "")) for i in json.loads(arq_pend.read_text(encoding="utf-8"))}
    pasta = RODADA / "respostas"
    arquivos = sorted(pasta.glob("*.json")) if pasta.exists() else []
    if not arquivos:
        sys.exit("Nenhuma resposta em rodada-tira-duvidas/respostas/.")
    enviadas = RODADA / "enviadas"
    enviadas.mkdir(exist_ok=True)
    ok = falhas = 0
    for arq in arquivos:
        try:
            r = json.loads(arq.read_text(encoding="utf-8"))
        except (ValueError, UnicodeDecodeError):
            print(arq.name, "-> NAO ENVIADA: JSON invalido")
            falhas += 1
            continue
        if not isinstance(r, dict):
            print(arq.name, "-> NAO ENVIADA: o arquivo deve ter um objeto JSON")
            falhas += 1
            continue
        problema = problema_de(arq, r, validos, c)
        if problema:
            print(arq.name, "-> NAO ENVIADA:", problema)
            falhas += 1
            continue
        j = post({"acao": "responder", "chave": c, "id": r["id"], "status": r["status"],
                  "transcricao": str(r.get("transcricao", ""))[:MAX_TRANSCRICAO],
                  "resposta": str(r.get("resposta", ""))[:MAX_RESPOSTA]})
        if j.get("ok"):
            arq.replace(enviadas / arq.name)
            print(r["id"], "-> ok")
            ok += 1
        else:
            print(r["id"], "-> ERRO do porteiro:", j.get("erro"))
            falhas += 1
    print("enviadas:", ok, "| falhas:", falhas)
    if falhas:
        sys.exit(1)


def main(argv):
    if len(argv) != 2 or argv[1] not in ("pendentes", "responder"):
        sys.exit("uso: python3 source/tira-duvidas/porteiro.py pendentes|responder")
    pendentes() if argv[1] == "pendentes" else responder()


if __name__ == "__main__":
    main(sys.argv)
