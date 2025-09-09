import requests
import re
import os

ARQUIVO_SAIDA = "providers/meta_ips.txt"
ASNS_META = ["AS32934", "AS54115", "AS149642"]

def extrair_blocos(asn):
    print(f"🔍 Consultando {asn} via bgp.he.net...")
    url = f"https://bgp.he.net/{asn}#_prefixes"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"⚠️ Falha ao acessar {asn}: {response.status_code}")
        return []

    blocos = re.findall(r'(\d{1,3}(?:\.\d{1,3}){3}/\d{1,2})', response.text)
    print(f"📦 {asn}: {len(blocos)} blocos encontrados")
    return blocos

def salvar_em_arquivo(lista_ips, caminho):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    conteudo = "\n".join(sorted(set(lista_ips))) + "\n"

    if os.path.exists(caminho):
        with open(caminho, "r") as f:
            if f.read().strip() == conteudo.strip():
                print("ℹ️ Nenhuma alteração detectada.")
                return False

    with open(caminho, "w") as f:
        f.write(conteudo)
    print(f"✅ IPs salvos em: {caminho}")
    return True

def main():
    todos_blocos = []
    for asn in ASNS_META:
        blocos = extrair_blocos(asn)
        todos_blocos.extend(blocos)

    if not todos_blocos:
        print("🛑 Nenhum bloco IP encontrado.")
        return

    alterado = salvar_em_arquivo(todos_blocos, ARQUIVO_SAIDA)
    if alterado:
        print("🚀 Lista atualizada com sucesso.")
    else:
        print("📁 Lista já estava atualizada.")

if __name__ == "__main__":
    main()
