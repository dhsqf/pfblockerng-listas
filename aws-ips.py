import requests

# Baixa o JSON oficial da AWS
url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
data = requests.get(url).json()

# Lista de regiões e serviços que você quer incluir
regioes = ['sa-east-1', 'us-east-1', 'us-west-2', 'eu-west-1']
servicos = ['EC2', 'S3', 'CLOUDFRONT']

# Filtra os IPs
ips_filtrados = set()
for item in data['prefixes']:
    if item['region'] in regioes and item['service'] in servicos:
        ips_filtrados.add(item['ip_prefix'])

# Salva no formato compatível com pfSense
with open("aws_ips.txt", "w") as f:
    for ip in sorted(ips_filtrados):
        f.write(ip + "\n")
