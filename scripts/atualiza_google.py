import requests
import os

# 🔗 Endpoint oficial dos IPs públicos do Google
GOOGLE_IP_URL = "https://www.gstatic.com/ipranges/goog.json"

# 📄 Caminho do arquivo de saída
ARQUIVO_SAIDA = "providers/google_ips.txt"

def buscar_ips_google():
    print("🔄 Buscando IPs dos serviços Google...")
    response = requests.get(GOOGLE_IP_URL)
    response.raise_for_status()
    dados = response.json()

    ips = set()
    for item in dados.get("prefixes", []):
        ip = item.get("ipv4Prefix") or item.get("ipv6Prefix")
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
    ips = buscar_ips_google()
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
