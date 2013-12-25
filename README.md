microcodedCPU-assembler-python
==============================

A simple version of Warren's Microcoded CPU assembler - Luming

File name: massem.py

This microcoded CPU is implemented in Logisim and the CPU's design introduction can be found with the link below:
http://minnie.tuhs.org/Programs/UcodeCPU/

Originally, the assembler of this CPU is implemented in with Perl, and i rewrite it with Python.

Run this assembler with command line:

1. cd to the folder, in which it contains both massem.py and the .s file (the program in assembling language).
2. then, run in command line:  $python massem.py filename.s, note: "filename.s" is the program in assembling language
3. the output file is named as "program_luming.ram", which is consist of programs machine code


Finally, the 'basic_program_add_sub.s' and 'basic_program_mul_div.s' are used for tested.
