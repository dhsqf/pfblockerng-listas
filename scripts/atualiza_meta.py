"""Gera providers/meta_ips.txt (IPv4) e providers/meta_ips_v6.txt (IPv6)
a partir dos prefixos anunciados pelos ASNs da Meta, via API do RIPEstat.
"""
import ipaddress
import os
import sys
from datetime import datetime, timezone

import requests

ASNS_META = ["AS32934", "AS54115", "AS149642"]
RIPESTAT_URL = "https://stat.ripe.net/data/announced-prefixes/data.json"
SAIDA_V4 = "providers/meta_ips.txt"
SAIDA_V6 = "providers/meta_ips_v6.txt"

TIMEOUT = 30
# Se a lista nova encolher mais que isso em relação à atual, aborta
# (protege contra API fora do ar / resposta parcial derrubando o WhatsApp).
QUEDA_MAXIMA = 0.30
# Prefixos mais amplos que isso são descartados (nenhum ASN da Meta anuncia /7).
PREFIXO_MINIMO_V4 = 8
PREFIXO_MINIMO_V6 = 19

session = requests.Session()
session.headers["User-Agent"] = "pfblockerng-listas (github.com/dhsqf/pfblockerng-listas)"


def buscar_prefixos(asn: str) -> list:
    resp = session.get(
        RIPESTAT_URL,
        params={"resource": asn, "sourceapp": "pfblockerng-listas"},
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    dados = resp.json()
    if dados.get("status") != "ok":
        raise RuntimeError(f"{asn}: RIPEstat retornou status {dados.get('status')}")

    redes = []
    for item in dados["data"]["prefixes"]:
        try:
            rede = ipaddress.ip_network(item["prefix"], strict=True)
        except (KeyError, ValueError) as e:
            print(f"⚠️ {asn}: prefixo inválido ignorado: {item!r} ({e})")
            continue
        minimo = PREFIXO_MINIMO_V4 if rede.version == 4 else PREFIXO_MINIMO_V6
        if rede.prefixlen < minimo or not rede.is_global:
            print(f"⚠️ {asn}: prefixo suspeito ignorado: {rede}")
            continue
        redes.append(rede)
    print(f"📦 {asn}: {len(redes)} prefixos")
    return redes


def ler_atual(caminho: str) -> list:
    if not os.path.exists(caminho):
        return []
    with open(caminho) as f:
        return [l.strip() for l in f if l.strip() and not l.startswith("#")]


def salvar(redes: list, caminho: str, versao: int) -> bool:
    agregadas = sorted(ipaddress.collapse_addresses(redes))
    linhas = [str(r) for r in agregadas]

    atuais = ler_atual(caminho)
    if atuais and len(linhas) < len(atuais) * (1 - QUEDA_MAXIMA):
        # Compara pelo espaço coberto, não pela contagem de linhas,
        # pois a agregação naturalmente reduz o número de linhas.
        cobertura_nova = sum(r.num_addresses for r in agregadas)
        cobertura_atual = sum(
            r.num_addresses
            for r in ipaddress.collapse_addresses(ipaddress.ip_network(a) for a in atuais)
        )
        if cobertura_nova < cobertura_atual * (1 - QUEDA_MAXIMA):
            raise RuntimeError(
                f"IPv{versao}: cobertura caiu de {cobertura_atual} para {cobertura_nova} "
                f"endereços (> {QUEDA_MAXIMA:.0%}). Abortando sem sobrescrever."
            )

    if linhas == atuais:
        print(f"ℹ️ IPv{versao}: sem alterações.")
        return False

    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    cabecalho = [
        f"# Meta IPv{versao} - ASNs: {', '.join(ASNS_META)}",
        "# Fonte: RIPEstat announced-prefixes",
        f"# Gerado em: {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}",
        f"# Prefixos: {len(linhas)}",
    ]
    with open(caminho, "w") as f:
        f.write("\n".join(cabecalho + linhas) + "\n")
    print(f"✅ IPv{versao}: {len(linhas)} prefixos salvos em {caminho}")
    return True


def main() -> int:
    redes = []
    for asn in ASNS_META:
        # Falha de qualquer ASN aborta tudo: lista parcial é pior que lista velha.
        redes.extend(buscar_prefixos(asn))

    v4 = [r for r in redes if r.version == 4]
    v6 = [r for r in redes if r.version == 6]
    if not v4:
        raise RuntimeError("Nenhum prefixo IPv4 retornado. Abortando.")

    salvar(v4, SAIDA_V4, 4)
    if v6:
        salvar(v6, SAIDA_V6, 6)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"🛑 {e}")
        sys.exit(1)
