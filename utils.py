import os


def create_wireguard_conf(user_id, sub):

    os.makedirs("configs", exist_ok=True)

    file_path = f"configs/{user_id}_{sub[0]}.conf"

    content = f"""
[Interface]
PrivateKey = {sub[5]}
Address = {sub[6]}
DNS = 1.1.1.1

[Peer]
PublicKey = {sub[7]}
Endpoint = {sub[8]}
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
"""

    with open(file_path, "w") as f:
        f.write(content)

    return file_path
