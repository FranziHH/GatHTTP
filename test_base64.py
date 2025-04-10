#!/usr/bin/env python

import base64

data = b'Hello, World!'
encoded_data = base64.b64encode(data)
print(encoded_data.decode())

decoded_data = base64.b64decode(encoded_data)
print(decoded_data.decode())
