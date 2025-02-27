from binascii import unhexlify, hexlify
import hmac
import hashlib
from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad


key_encrypt_0 = unhexlify("5234f60f846bb1d5f059c70e75434be689f41113ef56e2bf69253fad6a30ab5fa449204f52f64a0265fd5744a9489f41cefd95a1d642830e9cf9cdce13c55245")[:16] # first 4 strings in  <tls-auth> section
key_hmac_0 = unhexlify("270cf7d367ddc6b56eb1ba749be40e4280cdf7cfbad178348a0e057f1fdc87f0e5ba84717475b868a7fd617fee8c561cb4575d983534ef71dd8aaa48a53ed469")[:20] # analog 2
key_encrypt_1 = unhexlify("0ae85faf4522f7defd89ba373a0d22eef9356e487fdfa0796b0b1fc393fd3ab552db7a1ed691ddd50eeb7be2cc32d91252df93987f4878ec42a12e3a7cda5a40")[:16] # analog 3
key_hmac_1 = unhexlify("b1aa850a05821b300359a796313cbcec4076483ec7692708c32d323ed080beba60c58d9281fb5d27c688ac271d3b6d151695093291fb788dbbfefb8b7c7f9bef")[:20] # analog 4
key_hmac = key_hmac_1 # this is because of "direction", so to one direction is first pair and v.v.
key_encrypt = key_encrypt_1
packet = unhexlify("91861a4479c376d3013cdcd7f3e657ac093048cdb3a40775fc5804f68842ef06288a9343acb298562aaa4c92c10aae2213441619c3df0d8b89a0f13f5dd69d1eaa0e22667938b68e38a1238e39b76b889b7b6e5dbadd8f3a264f6fc9bb9c225de387d5d17914b2e2853d7fbb706da429f596721ab394febe7e52875183f0e9e10ec16042398c4116c2069ef18f06da45b55581a9997d1f54def143b053226727934404be44379a0172d1b618bbf1b676b60f57889e734af6b54291d07d9c7e13573cc81e")
hmac_result = hmac.new(key_hmac, packet[20:], hashlib.sha1).hexdigest()
print("HMAC = %s" % hmac_result)
iv = packet[20:28]
encrypted_part = packet[28:]
decrypted = Blowfish.new(key_encrypt, mode=Blowfish.MODE_CBC, IV=iv).decrypt(encrypted_part)
print("Открытый текст: %s" % hexlify(decrypted).decode())
packet_id = decrypted[:4]
timestamp = decrypted[4:8]
decrypted_data = decrypted[8:-decrypted[-1]]  # Убираем packet_id и timestamp из начала и паддинг с конца
print("ID пакета: %s" % hexlify(packet_id).decode())
print("Временная метка: %s" % hexlify(timestamp).decode())
print("Содержимое пакета: %s" % hexlify(decrypted_data).decode())
print("Содержимое пакета: %s" % decrypted_data)
