import requests

def extrair_cidrs(data):
    # Exemplo simples: extrai CIDRs do campo 'prefixes' do JSON
    cidrs = []
    for prefix in data.get('prefixes', []):
        cidrs.append(prefix.get('ip_prefix'))
    return cidrs

def main():
    url = 'https://ipinfo.io/AS32934/json'  # ASN Meta no ipinfo.io
    response = requests.get(url)
    data = response.json()

    cidrs = extrair_cidrs(data)

    with open('meta-cidr.txt', 'w') as f:
        for cidr in cidrs:
            f.write(cidr + '\n')

if __name__ == '__main__':
    main()
