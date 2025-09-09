import requests
import os

ARQUIVO_SAIDA = "providers/fastly_ips.txt"
FASTLY_URL = "https://api.fastly.com/public-ip-list"

def buscar_ips_fastly():
    print("🔄 Buscando IPs IPv4 da Fastly...")
    response = requests.get(FASTLY_URL)
    response.raise_for_status()
    data = response.json()

    ipv4 = data.get("addresses", [])
    print(f"📦 IPv4 encontrados: {len(ipv4)}")
    return sorted(ipv4)

def salvar_em_arquivo(ips, caminho):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    conteudo = "\n".join(ips) + "\n"

    if os.path.exists(caminho):
        with open(caminho, "r") as f:
            if f.read().strip() == conteudo.strip():
                print("ℹ️ Nenhuma alteração detectada.")
                return False

    with open(caminho, "w") as f:
        f.write(conteudo)
    print(f"✅ IPs salvos em: {caminho}")
    return True

if __name__ == "__main__":
    ips = buscar_ips_fastly()
    if not ips:
        print("🛑 Nenhum IP encontrado.")
    else:
        salvar_em_arquivo(ips, ARQUIVO_SAIDA)
