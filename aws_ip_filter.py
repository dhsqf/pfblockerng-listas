import requests
import os
import subprocess
from datetime import datetime

# 🔗 Fonte oficial da AWS
AWS_URL = "https://ip-ranges.amazonaws.com/ip-ranges.json"

# 🎯 Filtros por serviço e região
FILTROS = {
    "EC2": "sa-east-1",
    "S3": "sa-east-1",
    "CLOUDFRONT": None
}

# 📄 Nome do arquivo de saída
ARQUIVO_SAIDA = "todos_ips_filtrados.txt"

def baixar_dados_aws():
    print("🔄 Baixando dados da AWS...")
    response = requests.get(AWS_URL)
    response.raise_for_status()
    return response.json()

def filtrar_ips(data, servico, regiao=None):
    return [prefix['ip_prefix'] for prefix in data['prefixes']
            if prefix['service'] == servico and (regiao is None or prefix['region'] == regiao)]

def salvar_em_arquivo(nome_arquivo, lista_ips):
    lista_unica = sorted(set(lista_ips))
    with open(nome_arquivo, "w") as f:
        for ip in lista_unica:
            f.write(ip + "\n")
    print(f"✅ IPs salvos em: {nome_arquivo}")
    return nome_arquivo

def arquivo_foi_modificado(caminho):
    resultado = subprocess.run(["git", "status", "--porcelain", caminho], capture_output=True, text=True)
    return bool(resultado.stdout.strip())

def atualizar_git(arquivo):
    if arquivo_foi_modificado(arquivo):
        subprocess.run(["git", "add", arquivo])
        commit_msg = f"Atualização automática: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_msg])
        subprocess.run(["git", "push"])
        print("🚀 Alterações enviadas para o GitHub.")
    else:
        print("ℹ️ Nenhuma alteração detectada. Nada para enviar.")

def main():
    dados = baixar_dados_aws()
    todos_ips = []
    for servico, regiao in FILTROS.items():
        ips = filtrar_ips(dados, servico, regiao)
        print(f"🔍 {servico} ({regiao if regiao else 'Global'}): {len(ips)} IPs")
        todos_ips.extend(ips)
    arquivo = salvar_em_arquivo(ARQUIVO_SAIDA, todos_ips)
    atualizar_git(arquivo)

if __name__ == "__main__":
    main()
