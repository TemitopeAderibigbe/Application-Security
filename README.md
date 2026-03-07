CS 3235: Application Security - Buffer Overflow Exploitation
Overview
This repository contains my solutions for the Application Security course project at Georgia Tech, focusing on understanding and exploiting buffer overflow vulnerabilities in x86_64 binaries.
 Educational Purpose Only: This project was completed as part of CS 3235 coursework to understand security vulnerabilities and defensive measures. All techniques should only be used in authorized security research and testing.
Project Structure
Lab 1: GDB Fundamentals
Introduction to memory layout, assembly analysis, and GDB debugging techniques.
Skills Developed:

x86_64 assembly language analysis
GDB debugging and memory inspection
Understanding stack frame layout
Little-endian vs big-endian byte ordering
Locating functions and understanding call conventions

Key Tasks:

Analyzed compiled binaries to locate function addresses
Examined stack memory during program execution
Practiced endianness conversions for exploit development

[View detailed write-up](https://docs.google.com/document/d/1x-F4evrRbWoNU34qojijxL2nvTYrAALDq9e8G1i0CBY/edit?usp=sharing)
Project Part 1: Basic Buffer Overflow Attacks
Exploited three vulnerable C programs using classical buffer overflow techniques.
Targets:

Target 1: String-based buffer overflow
Target 2: Command-line argument overflow with shellcode injection
Target 3: Environment variable-based overflow

Skills Developed:

Crafting buffer overflow exploits
Shellcode injection techniques
Stack smashing to control program execution
Obtaining root shells through privilege escalation


Project Part 2: Advanced Exploitation Techniques
Advanced buffer overflow attacks with modern defenses.
Targets:

Target 4: Integer overflow leading to buffer overflow
Target 5: Bypassing DEP (Data Execution Prevention) without shellcode
Target 6: Defeating ASLR (Address Space Layout Randomization)
Target 7: Return-Oriented Programming (ROP) chains

Skills Developed:

Integer overflow exploitation
Return-to-libc attacks
NOP sled techniques for variable stack positions
ROP gadget chaining
Syscall-based exploitation (setuid, execve)


Technical Environment

Architecture: x86_64
OS: Ubuntu Linux (custom VM)
Compiler: GCC with security features disabled (-fno-stack-protector, -z execstack)
Tools: GDB, Python 3, ROPgadget


Key Learnings

Memory Safety is Critical: Understanding how buffer overflows occur highlights why languages with memory safety (Rust, Go) and modern compiler protections are essential.
Defense in Depth: Modern systems use multiple layers (DEP, ASLR, stack canaries) because no single defense is perfect.
Attack Surface Analysis: Even "simple" bugs like integer overflows can cascade into serious vulnerabilities.
Ethical Responsibility: These techniques demonstrate why security research must be conducted responsibly and only in authorized contexts.


Note on Code Availability
Per academic integrity policies, exploit code is not publicly shared. This README documents the concepts and skills developed without providing working exploits that could be misused.
If you're a recruiter or educator interested in seeing technical work samples, please contact me directly.

Skills Demonstrated

Low-level systems programming
Assembly language analysis (Intel syntax)
Debugger proficiency (GDB)
Exploit development methodology
Security research techniques
Python scripting for binary exploitation


Course Information
Course: CS 3235 - Introduction to Information Security
Institution: Georgia Institute of Technology
Semester: Spring 2026
