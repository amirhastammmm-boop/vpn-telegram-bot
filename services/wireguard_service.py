def generate_wireguard_config():
    config = """[Interface]
PrivateKey = AUTO_PRIVATE_KEY
Address = 10.0.0.2/32
DNS = 1.1.1.1

[Peer]
PublicKey = SERVER_PUBLIC_KEY
Endpoint = server_ip:51820
AllowedIPs = 0.0.0.0/0
"""
    return config
