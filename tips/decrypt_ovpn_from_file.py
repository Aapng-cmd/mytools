from binascii import unhexlify, hexlify
import hmac
import hashlib
from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad
import pyshark


key_encrypt_0 = unhexlify("cdf2f818a298eebaa3b14a36443562e3c556da1decabffb35421899985218360728c257f0c8edd6fddb029e76fe9ac8375d200bd6a585c2f69df89b2ceee4820")[:16]
key_hmac_0 = unhexlify("80e841b0284b952c9582a080c856d191aec77d364e204f5968011121160fcf2979931ff0b4ed773255621c58bb5d1a4fe52d7f42749c71e09f18d84d5aca8c5e")[:20]
key_encrypt_1 = unhexlify("187ece4ea1cec89318f49be2e52e519c9a8c855abf178a3628074a3faa07b53a8b25898641afcc8fac038b1848fc776e4079f06a874075eb01e870c5d9940cbd")[:16]
key_hmac_1 = unhexlify("5f602fab7ff859063efaeb600cbdf190ce5ccc87240a91cd57160237be72df3d8c29ed580d968efb51eb914ed206051bff8c4201e94060b54fe229abc81a1fde")[:20]

# packet = unhexlify("00000e96b1c14f8b3e1ee9441027c3640e6054feb0b3a37039843592239f620ce4bfad345d1f3e9be5c7a27e1547f9fc248d7fa81367eebb5f7e8fb7802a2a05c49a5f8e90d2076d87b4554a8ca162c44c8b346b7b97f3b4e5c3")

cap = pyshark.FileCapture('openvpn_traf.pcapng')


for packet_i in cap:
    if packet_i['ip'].dst == "10.0.0.2":
        key_hmac = key_hmac_0
        key_encrypt = key_encrypt_0
    else:
        key_hmac = key_hmac_1
        key_encrypt = key_encrypt_1
    
    # packet = unhexlify(input("packet >> "))
    try:
        packet = packet_i['openvpn'].data.replace(":", "")
    except AttributeError:
        # print(packet_i)
        # print(dir(packet_i))
        print(packet_i['openvpn'])
        continue
    packet = unhexlify(packet)
    hmac_result = hmac.new(key_hmac, packet[20:], hashlib.sha1).hexdigest()
    print("\n==============")
    print("Destination:", packet_i['ip'].dst)
    print("HMAC = %s" % hmac_result)

    iv = packet[20:28]
    encrypted_part = packet[28:]
    encrypted_part += b"\x07" * (8 - len(encrypted_part) % 8)
    print(iv)
    print(encrypted_part, len(encrypted_part))

    decrypted = Blowfish.new(key_encrypt, mode=Blowfish.MODE_CBC, IV=iv).decrypt(encrypted_part)
    print("Открытый текст: %s" % hexlify(decrypted).decode())

    packet_id = decrypted[:4]
    timestamp = decrypted[4:8]
    decrypted_data = decrypted[8:-decrypted[-1]]  # Убираем packet_id и timestamp из начала и паддинг с конца
    print("ID пакета: %s" % hexlify(packet_id).decode())
    print("Временная метка: %s" % hexlify(timestamp).decode())
    print("Содержимое пакета HEX: %s" % hexlify(decrypted_data).decode())
    print("Содержимое пакета: %s" % decrypted_data)
    print("===========")
