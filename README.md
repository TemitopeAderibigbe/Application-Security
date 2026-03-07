```markdown
# Buffer Overflow Exploitation & Low-Level Security Research

> A comprehensive exploration of memory corruption vulnerabilities, exploit development, and modern defensive techniques in x86_64 systems.

![Security](https://img.shields.io/badge/Security-Research-red)
![Architecture](https://img.shields.io/badge/Architecture-x86__64-blue)
![Language](https://img.shields.io/badge/Language-C%20%7C%20Python%20%7C%20Assembly-green)

---

## Project Overview

After learning about major security breaches like Heartbleed and the Equifax data leak, I wanted to understand **how** these attacks actually work at the machine level. This project gave me hands-on experience with memory corruption, exploit development, and the defensive techniques used to prevent them.

**⚠️ Educational Purpose**: All techniques demonstrated here are for authorized security research and learning in controlled environments.

---

## 📚 Table of Contents

- [Lab: GDB & Memory Analysis Fundamentals](#lab-gdb--memory-analysis-fundamentals)
- [Project: Exploit Development](#project-exploit-development)
  - [Part 1: Classic Buffer Overflows](#part-1-classic-buffer-overflows)
  - [Part 2: Advanced Exploitation Techniques](#part-2-advanced-exploitation-techniques)
- [Technical Stack](#technical-stack)
- [Key Learnings](#key-learnings)
- [What's Next](#whats-next)

---

## 🔬 Lab: GDB & Memory Analysis Fundamentals

### Overview
Built a foundation in low-level debugging, assembly analysis, and memory forensics - essential skills for understanding how exploits work.

### What I Did

#### Task 1-3: Assembly Code Analysis
- Disassembled compiled binaries to locate function addresses and calls
- Distinguished between call instruction addresses vs. function entry points
- Analyzed standard library function linking in compiled executables

**Key Insight**: Understanding the difference between "where a function is called" vs. "where a function begins" is crucial for exploit development.

#### Task 4-5: Runtime Stack Inspection
- Set breakpoints and examined stack memory during execution
- Located specific data on the stack using GDB's `x/` command
- Found string literals and local variables at runtime

**Technique Learned**: Systematic memory examination to locate return addresses and local variables - essential for crafting exploits.

#### Task 6-7: Endianness & Memory Representation
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

**Why This Matters**: When injecting shellcode or overwriting addresses, you must account for little-endian byte ordering on x86_64.

### Skills Developed
- ✅ x86_64 assembly language reading
- ✅ GDB debugging proficiency
- ✅ Stack frame analysis
- ✅ Memory layout understanding
- ✅ Endianness conversions

[View detailed lab write-up](./docs/lab_writeup.md)

---

## 💥 Project: Exploit Development

Building on the lab foundations, I developed working exploits against vulnerable C programs to understand attack vectors and defensive measures.

---

## Part 1: Classic Buffer Overflows

### Target 1: String-Based Overflow
**Vulnerability**: Unsafe `gets()` function allows unbounded input into a fixed-size buffer.

**Attack Strategy**:
- Analyzed stack layout to find offset to return address
- Crafted input to overwrite return address with target function address
- Redirected execution flow to bypass authentication

**Key Code**:
```python
# Calculate padding to reach return address
padding = b'A' * offset
target_address = struct.pack('<Q', 0x401234)  # Little-endian 64-bit address
payload = padding + target_address
```

**Learning**: Even simple input validation failures can lead to complete control flow hijacking.

---

### Target 2: Shellcode Injection
**Vulnerability**: Command-line argument overflow with executable stack.

**Attack Strategy**:
- Injected x86_64 shellcode to spawn `/bin/sh`
- Overwrote return address to point to shellcode on stack
- Gained root shell through privilege escalation

**Shellcode Overview**:
```assembly
; Compact /bin/sh shellcode
xor rsi, rsi        ; argv = NULL
xor rdx, rdx        ; envp = NULL
mov rax, 59         ; syscall number for execve
syscall             ; Execute /bin/sh
```

**Challenge**: Finding exact stack address where shellcode lands required careful GDB analysis.

---

### Target 3: Environment Variable Exploitation
**Vulnerability**: Buffer overflow triggered through environment variables.

**Attack Strategy**:
- Placed shellcode in environment variable
- Calculated environment variable stack address
- Overwrote return address to jump to shellcode in env

**Why Different**: Environment variables are stored at predictable stack locations, making them reliable shellcode storage.

---

## Part 2: Advanced Exploitation Techniques

### Target 4: Integer Overflow → Buffer Overflow
**Vulnerability**: Integer overflow in allocation size calculation.

**The Bug**:
```c
size_t count;
fread(&count, sizeof(size_t), 1, f);  // Attacker-controlled!
unsigned int *buf = alloca(count * sizeof(unsigned int));
```

**Attack Strategy**:
- Chose `count = 0x4000000000000010`
- When multiplied by 4: `0x4000000000000010 * 4 = 0x0000000000000040` (wraps to 64 bytes)
- `alloca()` allocates only 64 bytes
- Loop tries to read `count` integers → massive overflow!

**Math Behind It**:
```python
count = 0x4000000000000010
# count * 4 in 64-bit wraps around:
# 0x10000000000000040 → 0x0000000000000040 = 64 bytes

# But loop iterates 'count' times, writing way past buffer end
```

**Key Learning**: Integer overflows can cascade into memory corruption vulnerabilities.

---

### Target 5: Bypassing DEP (Data Execution Prevention)
**Challenge**: Stack is marked non-executable. Can't execute injected shellcode.

**Solution**: Return-to-libc attack
- Found existing code that calls `system()`
- Set up stack to call `system("/bin/sh")`
- No shellcode needed - used existing executable code!

**Stack Layout**:
```
[padding] [system_addr] [return_addr] [ptr_to_"/bin/sh"]
```

**Why This Works**: DEP only prevents executing stack data, not jumping to existing executable code.

---

### Target 6: Defeating ASLR (Address Space Layout Randomization)
**Challenge**: Stack position randomized by 0-256 bytes each execution.

**Solution**: NOP Sled technique
- Created large "slide" of NOP instructions before shellcode
- Return address points anywhere in NOP sled
- Execution "slides" down to shellcode regardless of exact offset

**Visualization**:
```
Stack:
[buffer] [NOPs NOPs NOPs NOPs] [shellcode] [saved rbp] [return addr]
         ^----- 256 bytes ----^
         Any address in here works!
```

**Success Rate**: 100% - as long as return address hits NOP sled, exploit works.

---

### Target 7: Return-Oriented Programming (ROP)
**Challenge**: DEP enabled. No easy `system()` function available.

**Solution**: Chain together existing code "gadgets" to make syscalls
- Found gadgets using ROPgadget tool
- Built chain to execute: `setuid(0); execve("/bin/sh", 0, 0);`
- No shellcode injection - pure code reuse!

**ROP Chain Structure**:
```python
# Gadget 1: pop rdi; ret    <- Load argument for setuid
# Gadget 2: pop rax; ret    <- Load syscall number
# Gadget 3: syscall         <- Make setuid(0) call
# Gadget 4: pop rdi; ret    <- Load /bin/sh path
# Gadget 5: pop rsi; ret    <- Load NULL for argv
# Gadget 6: pop rdx; ret    <- Load NULL for envp  
# Gadget 7: pop rax; ret    <- Load syscall 59 (execve)
# Gadget 8: syscall         <- Execute /bin/sh
```

**Most Complex**: Required understanding of:
- x86_64 calling conventions
- Linux syscall interface
- Gadget chaining techniques
- Stack manipulation

---

## 🛠️ Technical Stack

| Category | Technologies |
|----------|-------------|
| **Languages** | C, Python 3, x86_64 Assembly (Intel syntax) |
| **Architecture** | Intel x86_64 |
| **Tools** | GDB, ROPgadget, pwntools, objdump |
| **Environment** | Linux VM (custom security research environment) |
| **Compilation** | GCC with `-fno-stack-protector -z execstack` |

---

## 🧠 Key Learnings

### 1️⃣ Memory Safety is Critical
Even small bugs (off-by-one errors, integer overflows) can cascade into complete system compromise. This is why:
- Memory-safe languages (Rust, Go) are essential for security-critical code
- Input validation must be comprehensive
- Bounds checking should be automatic, not manual

### 2️⃣ Defense in Depth Works
Modern systems stack multiple protections because **no single defense is perfect**:
- **Stack Canaries**: Detect buffer overflows
- **DEP/NX**: Prevent shellcode execution
- **ASLR**: Randomize memory layout
- **CFI**: Validate control flow transfers

Attackers must bypass ALL of them - defenders only need ONE to work.

### 3️⃣ The Attacker's Advantage
- Defenders must protect against **all possible attacks**
- Attackers only need to find **one weakness**
- This asymmetry drives the need for secure-by-default systems

### 4️⃣ Low-Level Understanding Matters
Even when writing high-level code:
- Understanding compilation helps you write more secure code
- Knowing assembly aids in debugging subtle issues
- Memory layout knowledge prevents common vulnerabilities

---

## 🔮 What's Next

Building on this foundation, I'm exploring:

- [ ] **Modern Exploit Mitigations**
  - Control Flow Integrity (CFI)
  - Intel CET (Control-flow Enforcement Technology)
  - ARM Pointer Authentication Codes (PAC)

- [ ] **Vulnerability Discovery**
  - Fuzzing with AFL/libFuzzer
  - Static analysis tools
  - Symbolic execution

- [ ] **Binary Hardening**
  - Compiler hardening flags
  - Position-Independent Executables (PIE)
  - RELRO (Relocation Read-Only)

- [ ] **Real-World Security**
  - CTF competitions
  - Bug bounty programs
  - Open-source security audits

---

## 📫 Let's Connect

Interested in discussing security research, low-level systems, or how these concepts apply to real-world development?

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](your-linkedin)
[![Email](https://img.shields.io/badge/Email-Contact-red)](mailto:your-email)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-green)](your-website)

---

## ⚖️ Ethical Notice

This work was completed in a controlled educational environment. All techniques should **only** be used for:
- ✅ Authorized security research
- ✅ Defensive security testing  
- ✅ Educational purposes in controlled environments

**Never** use these techniques against systems you don't own or have explicit permission to test.

### Academic Integrity
If you're working on similar coursework, **please solve problems yourself**. Understanding these concepts requires hands-on practice, not copying solutions. Using this code for academic assignments constitutes plagiarism.

---

## 📄 License

This project is shared for educational and portfolio purposes. Please respect academic integrity policies and use responsibly.
