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

def conteudo_arquivo_existente(caminho):
    if not os.path.exists(caminho):
        return ""
    with open(caminho, "r") as f:
        return f.read()

def salvar_em_arquivo(nome_arquivo, lista_ips):
    lista_unica = sorted(set(lista_ips))
    novo_conteudo = "\n".join(lista_unica) + "\n"
    conteudo_antigo = conteudo_arquivo_existente(nome_arquivo)

    if novo_conteudo != conteudo_antigo:
        with open(nome_arquivo, "w") as f:
            f.write(novo_conteudo)
        print(f"✅ IPs atualizados e salvos em: {nome_arquivo}")
        return True  # houve alteração
    else:
        print("ℹ️ IPs não mudaram. Arquivo permanece o mesmo.")
        return False  # sem alteração

def atualizar_git(arquivo):
    subprocess.run(["git", "add", arquivo])
    commit_msg = f"Atualização automática: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    resultado = subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, text=True)

    if "nothing to commit" in resultado.stdout.lower():
        print("ℹ️ Nenhuma alteração detectada pelo Git. Nada para enviar.")
    else:
        subprocess.run(["git", "push"])
        print("🚀 Alterações enviadas para o GitHub.")

def main():
    dados = baixar_dados_aws()
    todos_ips = []
    for servico, regiao in FILTROS.items():
        ips = filtrar_ips(dados, servico, regiao)
        print(f"🔍 {servico} ({regiao if regiao else 'Global'}): {len(ips)} IPs")
        todos_ips.extend(ips)

    houve_alteracao = salvar_em_arquivo(ARQUIVO_SAIDA, todos_ips)
    if houve_alteracao:
        atualizar_git(ARQUIVO_SAIDA)
    else:
        print("🛑 Nenhuma atualização necessária no GitHub.")

if __name__ == "__main__":
    main()
