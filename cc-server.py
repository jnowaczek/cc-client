#!/usr/bin/env python
import base64
import logging
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

PORT = 8000
SECRET_KEY = "a cheeky nando's"


class GetHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        logging.error(self.headers)
        if self.headers.get('X-CRSF-TOKEN') and self.headers.get('Proxy-Authorization'):
            iv = self.headers.get('Proxy-Authorization')
            ct = self.headers.get('X-CRSF-TOKEN')

            iv = iv.partition('basic ')[2]

            iv = base64.b64decode(iv)
            print(iv)

            print('Initialization vector: {}\n'.format(iv))
            print('Encrypted data: {}'.format(ct))

            cipher = AES.new(bytes(SECRET_KEY, 'utf-8'), AES.MODE_CBC, bytes(iv))
            pt = unpad(cipher.decrypt(base64.b64decode(ct)), AES.block_size)
            print('Decrypted message: \'{}\''.format(pt))
        SimpleHTTPRequestHandler.do_GET(self)


Handler = GetHandler
httpd = TCPServer(("", PORT), Handler)

httpd.serve_forever()
