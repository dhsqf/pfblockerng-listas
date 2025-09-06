# pfBlockerNG Listas Públicas

Este repositório mantém listas públicas de IPs e domínios para uso com pfBlockerNG e pfSense. As listas são atualizadas automaticamente via GitHub Actions todos os dias.

---

## 🔄 Provedores incluídos

| Provedor         | Tipo     | URL para uso no pfSense |
|------------------|----------|--------------------------|
| AWS              | IPs      | https://raw.githubusercontent.com/dhsqf/pfblockerng-listas/main/providers/aws_ips.txt  
| Anydesk          | IPs      | https://raw.githubusercontent.com/dhsqf/pfblockerng-listas/main/providers/anydesk_ips.txt  
| Microsoft OneDrive | IPs    | https://raw.githubusercontent.com/dhsqf/pfblockerng-listas/main/providers/onedrive_ips.txt  
| Cloudflare       | IPs      | https://raw.githubusercontent.com/dhsqf/pfblockerng-listas/main/providers/cloudflare_ips.txt  
| Google Services  | IPs      | https://raw.githubusercontent.com/dhsqf/pfblockerng-listas/main/providers/google_ips.txt  

---

## 📦 Como usar no pfSense

1. Acesse **Firewall > pfBlockerNG > IP/DNS Feeds**
2. Crie um novo alias do tipo **URL Table (IPs)** ou **DNSBL**
3. Cole a URL desejada da tabela acima
4. Defina o tempo de atualização (ex: 1 dia)
5. Salve e aplique as regras

---

## 🕒 Atualização automática

Cada lista é atualizada diariamente por workflows do GitHub Actions. Os arquivos são versionados e mantêm histórico de alterações.

---

## 🛠️ Tecnologias utilizadas

- Python
- GitHub Actions
- pfSense / pfBlockerNG
