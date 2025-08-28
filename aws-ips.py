import requests

# Baixa o JSON oficial da AWS
url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
data = requests.get(url).json()

# Filtra IPs do serviço EC2 na região sa-east-1 (São Paulo)
ips = [item['ip_prefix'] for item in data['prefixes']
       if item['service'] == 'EC2' and item['region'] == 'sa-east-1']

# Salva em formato compatível com pfSense
with open("aws_ec2_ips.txt", "w") as f:
    for ip in ips:
        f.write(ip + "\n")
