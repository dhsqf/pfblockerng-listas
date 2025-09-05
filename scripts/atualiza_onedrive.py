import requests
import os

# 🔗 Endpoint oficial da Microsoft para IPs do Microsoft 365
ENDPOINT_URL = "https://endpoints.office.com/endpoints/worldwide?clientrequestid=b10c5ed1-bad1-445f-b386-b919946339a7"

# 📄 Caminho do arquivo de saída
ARQUIVO_SAIDA = "providers/onedrive_ips.txt"

def buscar_ips_onedrive():
    print("🔄 Buscando IPs do OneDrive...")
    response = requests.get(ENDPOINT_URL)
    response.raise_for_status()
    dados = response.json()

    ips = set()
    for item in dados:
        if "OneDrive" in item.get("serviceAreaDisplayName", ""):
            for ip in item.get("ips", []):
                ips.add(ip)

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
    ips = buscar_ips_onedrive()
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
