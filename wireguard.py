import random
import string

def create_wireguard_config(user_id):

    private_key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    return f"""
[Interface]
PrivateKey = {private_key}
Address = 10.0.0.{random.randint(2,250)}/24
DNS = 1.1.1.1

[Peer]
PublicKey = SERVER_PUBLIC_KEY
Endpoint = SERVER_IP:51820
AllowedIPs = 0.0.0.0/0
"""
