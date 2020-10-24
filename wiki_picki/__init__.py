from flask import Flask
app = Flask(__name__)

app.secret_key = b'\x17x\x84\x98\xb0\x99\xa2/\x90\xa7\xa7]k\xc7\xcb\x12'

import wiki_picki.views
