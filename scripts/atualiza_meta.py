import requests
import os

# 📄 Caminho do arquivo de saída
ARQUIVO_SAIDA = "providers/meta_ips.txt"

# 🔢 Lista de ASNs da Meta
ASNS_META = ["AS32934", "AS54115", "AS149642"]

# 🔗 Endpoint base da API ipinfo.io (gratuito até certo limite)
API_BASE = "https://ipinfo.io/{asn}/json"

def buscar_ips_meta():
    print("🔄 Buscando IPs da Meta via ipinfo.io...")
    ips = set()

    for asn in ASNS_META:
        url = API_BASE.format(asn=asn)
        print(f"🔍 Consultando {asn}...")
        response = requests.get(url)
        if response.status_code != 200:
            print(f"⚠️ Falha ao consultar {asn}: {response.status_code}")
            continue

        data = response.json()
        for prefix in data.get("prefixes", []):
            ip = prefix.get("netblock")
            if ip:
                ips.add(ip)

    print(f"🔢 Total de IPs encontrados: {len(ips)}")
    return sorted(ips)

def salvar_em_arquivo(lista_ips, caminho):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    conteudo = "\n".join(lista_ips) + "\n"

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
    ips = buscar_ips_meta()
    if not ips:
        print("🛑 Nenhum IP encontrado.")
        return

    alterado = salvar_em_arquivo(ips, ARQUIVO_SAIDA)
    if alterado:
        print("🚀 Lista atualizada com sucesso.")
    else:
        print("📁 Lista já estava atualizada.")

if __name__ == "__main__":
    main()
