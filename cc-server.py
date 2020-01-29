#!/usr/bin/env python
import base64
import logging
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

PORT = 8000
SECRET_KEY = "a cheeky nando's"

connection_state = 0
iv = ''
ct = []


class GetHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        global connection_state, iv, ct
        # logging.error(self.headers)

        if self.headers.get('Expect'):
            connection_state = 1
            iv = self.headers.get('X-CRSF-TOKEN')
            print('Received AES IV: {}'.format(iv))
            iv = base64.b64decode(iv)
        elif connection_state == 1 and not self.headers.get('Pragma'):
            if self.headers.get('X-CRSF-TOKEN'):
                ct.append(self.headers.get('X-CRSF-TOKEN'))
                print('Received encrypted data: {}'.format(ct[-1]))

        elif self.headers.get('Pragma'):
            cipher = AES.new(bytes(SECRET_KEY, 'utf-8'), AES.MODE_CBC, bytes(iv))

            with open(r'output', 'wb+') as output:
                for block in ct:
                    pt = unpad(cipher.decrypt(base64.b64decode(block)), AES.block_size)
                    print('Decrypted block: \'{}\''.format(pt[-1]))
                    output.write(pt)

            connection_state = 0
            iv = ''
            ct = []
        SimpleHTTPRequestHandler.do_GET(self)


Handler = GetHandler
httpd = TCPServer(("", PORT), Handler)

httpd.serve_forever()
