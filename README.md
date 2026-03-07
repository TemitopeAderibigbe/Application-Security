# Buffer Overflow Exploitation & Low-Level Security Research

A comprehensive exploration of memory corruption vulnerabilities, exploit development, and modern defensive techniques in x86_64 systems.

**Educational Purpose**: All techniques demonstrated here are for authorized security research and learning in controlled environments.

---

## Lab: GDB & Memory Analysis Fundamentals

Built a foundation in low-level debugging, assembly analysis, and memory forensics - essential skills for understanding how exploits work.

### Assembly Code Analysis
- Disassembled compiled binaries to locate function addresses and calls
- Distinguished between call instruction addresses vs. function entry points
- Analyzed standard library function linking in compiled executables

### Runtime Stack Inspection
- Set breakpoints and examined stack memory during execution
- Located specific data on the stack using GDB's `x/` command
- Systematically searched for return addresses and local variables

### Endianness & Memory Representation
- Examined how multi-byte values are stored in x86_64 (little-endian)
- Compared raw byte representation vs. interpreted values
- Practiced converting between big-endian and little-endian formats

**Example**:
```gdb
(gdb) x/1gx $rbp-0x8          # Big-endian display
0x7ffffff6ffc8: 0xdeadbeeeeeeeeeef

(gdb) x/8bx $rbp-0x8          # Little-endian (actual memory)
0x7ffffff6ffc8: 0xef 0xee 0xee 0xee 0xee 0xbe 0xad 0xde
```


**Key Takeaway**: When injecting shellcode or overwriting addresses, you must account for little-endian byte ordering on x86_64.

[Lab Write-Up](https://docs.google.com/document/d/1x-F4evrRbWoNU34qojijxL2nvTYrAALDq9e8G1i0CBY/edit?usp=sharing)
---

## Project Part 1: Classic Buffer Overflows

### Target 1: String-Based Overflow
Exploited unsafe `gets()` function to overwrite return address and redirect execution flow.

**Technique**: Stack layout analysis to calculate exact offset to return address, then crafted input to hijack control flow.

### Target 2: Shellcode Injection
Injected x86_64 shellcode to spawn `/bin/sh` with root privileges.

**Technique**: 
- Placed shellcode on executable stack
- Overwrote return address to point to shellcode
- Gained root shell through privilege escalation

### Target 3: Environment Variable Exploitation
Used environment variables as reliable shellcode storage locations.

**Technique**: Calculated environment variable stack addresses and redirected execution to shellcode stored in environment.

---

## Project Part 2: Advanced Exploitation Techniques

### Target 4: Integer Overflow → Buffer Overflow
Chained integer overflow with buffer overflow to achieve code execution.

**The Vulnerability**:
```c
size_t count;
fread(&count, sizeof(size_t), 1, f);  // Attacker-controlled
unsigned int *buf = alloca(count * sizeof(unsigned int));
```

**Technique**:
- Chose `count = 0x4000000000000010`
- When multiplied by 4: wraps to `0x40` (64 bytes)
- `alloca()` allocates only 64 bytes, but loop reads `count` integers
- Result: massive buffer overflow

### Target 5: Bypassing DEP (Data Execution Prevention)
Executed code when stack is marked non-executable.

**Technique**: Return-to-libc attack
- Located existing `system()` function in memory
- Set up stack to call `system("/bin/sh")`
- No shellcode needed - reused existing executable code

### Target 6: Defeating ASLR (Address Space Layout Randomization)
Exploited target with randomized stack position (0-256 byte offset).

**Technique**: NOP sled
- Created large "slide" of NOP instructions before shellcode
- Return address points anywhere in NOP sled
- Execution slides down to shellcode regardless of exact offset
- 100% success rate

### Target 7: Return-Oriented Programming (ROP)
Built ROP chain to make syscalls without injecting shellcode.

**Technique**:
- Found code gadgets using ROPgadget tool
- Chained gadgets to execute: `setuid(0); execve("/bin/sh", 0, 0);`
- Pure code reuse - no shellcode injection

**ROP Chain**:
```python
# Chain gadgets to set registers and make syscalls
pop_rdi + 0x0           # setuid(0)
pop_rax + 105           # syscall number for setuid
syscall_gadget
pop_rdi + binsh_addr    # execve("/bin/sh", ...)
pop_rsi + 0x0
pop_rdx + 0x0
pop_rax + 59            # syscall number for execve
syscall_gadget
```

---

## Technical Stack

**Languages**: C, Python 3, x86_64 Assembly (Intel syntax)  
**Architecture**: Intel x86_64  
**Tools**: GDB, ROPgadget, objdump  
**Environment**: Linux VM (custom security research environment)

---

## Key Learnings

### Memory Safety is Critical
Even small bugs (off-by-one errors, integer overflows) can cascade into complete system compromise. This demonstrates why memory-safe languages and automatic bounds checking are essential for security-critical code.

### Defense in Depth Works
Modern systems stack multiple protections (Stack Canaries, DEP, ASLR) because no single defense is perfect. Attackers must bypass all of them; defenders only need one to work.

### Low-Level Understanding Matters
Understanding how high-level code compiles to assembly helps write more secure software and debug subtle vulnerabilities.

---

## Ethical Notice

This work was completed in a controlled educational environment. All techniques should only be used for authorized security research, defensive testing, and educational purposes.
