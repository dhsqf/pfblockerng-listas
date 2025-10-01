import requests
import os

ARQUIVO_SAIDA = "providers/cloudflare_ips.txt"
CLOUDFLARE_IPV4_URL = "https://www.cloudflare.com/ips-v4"

def buscar_ips_cloudflare():
    print("🔄 Buscando IPs IPv4 da Cloudflare...")
    response = requests.get(CLOUDFLARE_IPV4_URL)
    response.raise_for_status()
    ipv4 = response.text.strip().splitlines()
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

def main():
    ips = buscar_ips_cloudflare()
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
