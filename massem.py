#   read in a text file of assembling language and then parse it to machine code
#   regular expressions
import re
import sys

#   Table of opcode names, the values and their arguments
#   A hash table implemented with dictionary

Opcode = {
	'add':  [ 0, 'dst'  ],
	'sub':  [ 1, 'dst'  ],
	'mul':  [ 2, 'dst'  ],
	'div':  [ 3, 'dst'  ],
	'rem':  [ 4, 'dst'  ],
	'and':  [ 5, 'dst'  ],
	'or':   [ 6, 'dst'  ],
	'xor':  [ 7, 'dst'  ],
	'nand': [ 8, 'dst'  ],
	'nor':  [ 9, 'dst'  ],
	'not':  [ 10, 'ds'  ],
	'lsl':  [ 11, 'dst' ],
	'lsr':  [ 12, 'dst' ],
	'asr':  [ 13, 'dst' ],
	'rol':  [ 14, 'dst' ],
	'ror':  [ 15, 'dst' ],
	'addi': [ 16, 'dsi' ],
	'subi': [ 17, 'dsi' ],
	'muli': [ 18, 'dsi' ],
	'divi': [ 19, 'dsi' ],
	'remi': [ 20, 'dsi' ],
	'andi': [ 21, 'dsi' ],
	'ori':  [ 22, 'dsi' ],
	'xori': [ 23, 'dsi' ],
	'nandi':[ 24, 'dsi' ],
	'nori': [ 25, 'dsi' ],
	'lsli': [ 26, 'dsi' ],
	'lsri': [ 27, 'dsi' ],
	'asri': [ 28, 'dsi' ],
	'roli': [ 29, 'dsi' ],
	'rori': [ 30, 'dsi' ],
	'addc': [ 31, 'dstI'],
	'subc': [ 32, 'dstI'],
	'jeq':  [ 33, 'sti' ],
	'jne':  [ 34, 'sti' ],
	'jgt':  [ 35, 'sti' ],
	'jle':  [ 36, 'sti' ],
	'jlt':  [ 37, 'sti' ],
	'jge':  [ 38, 'sti' ],
	'jeqz': [ 39, 'si'  ],
	'jnez': [ 40, 'si'  ],
	'jgtz': [ 41, 'si'  ],
	'jlez': [ 42, 'si'  ],
	'jltz': [ 43, 'si'  ],
	'jgez': [ 44, 'si'  ],
	'jmp':  [ 45, 'i'   ],
	'beq':  [ 46, 'stI' ],
	'bne':  [ 47, 'stI' ],
	'bgt':  [ 48, 'stI' ],
	'ble':  [ 49, 'stI' ],
	'blt':  [ 50, 'stI' ],
	'bge':  [ 51, 'stI' ],
	'beqz': [ 52, 'sI'  ],
	'bnez': [ 53, 'sI'  ],
	'bgtz': [ 54, 'sI'  ],
	'blez': [ 55, 'sI'  ],
	'bltz': [ 56, 'sI'  ],
	'bgez': [ 57, 'sI'  ],
	'br':   [ 58, 'I'   ],
    #   the below code need to be modified
	#   'jsr':  [ 59, 'i',	'$Mcode[$PC]+= 7<<3; # sp' ],
    #   modify above code as below: 
    'jsr':  [ 59, 'i',	'$Mcode[$PC]+= 7<<3; # sp' ],
	#   'rts':  [ 60, '', 	'$Mcode[$PC]+= 7<<3; # sp' ],
    #   modify above code as below: 
    'rts':  [ 60, '', 	'$Mcode[$PC]+= 7<<3; # sp' ],
	'inc':  [ 61, 's'   ],
	'dec':  [ 62, 's'   ],
	'li':   [ 63, 'di'  ],
	'lw':   [ 64, 'di'  ],
	'sw':   [ 65, 'di'  ],
	'lwi':  [ 66, 'dX'  ],
	'swi':  [ 67, 'dX'  ],
    #   the below code need to be modified
	#'push': [ 68, 'd',	'$Mcode[$PC]+= 7<<3; # sp' ],
    #   modify above code as below:
    'push': [ 68, 'd',	'$Mcode[$PC]+= 7<<3; # sp' ],
	#'pop':  [ 69, 'd',	'$Mcode[$PC]+= 7<<3; # sp' ],
    #   modify above code as below:
    'pop':  [ 69, 'd',	'$Mcode[$PC]+= 7<<3; # sp' ],
	'move': [ 70, 'ds'  ],
	'clr':  [ 71, 's'   ],
	'neg':  [ 72, 's'   ],
	'lwri': [ 73, 'dS' ],
	'swri': [ 74, 'dS' ],
}

Label = {}  # declare Hash of label -> PC values as a dictionary
Mcode = {}  # declare Machine code for each PC value as the Key of this dictionary
Origline = {}   # declare Original line as an dictionary
Ltype = []  # Type of label? undef is not, 1 is abs, 2 is rel
PC=0        # Current program counter


def pre_process(contents):
    # declare global varibles
    global PC
    global Label
    global Mcode
    global Origline
    global Ltype
    global Opcode
    
    lines = contents.split("\n") # return a list of strings, splited by "\n" in previous file
    p = re.compile('(\s*#.*)')  # regular expression object for finding comments
    labelRegEx = re.compile('(.*):\s+(.*)') # regular expression object for finding labels
    
    for line in lines:
        #print line
        line = line.strip() # take off spaces around a line
        
        matches = p.search(line)
        
        if matches:
            newline = line[0:matches.start()] # the new line is original line without comments
        else:
            newline = line
            
        if len(newline)>0:
            hadImmed=False
            Origline[PC] = newline
            
            matches = labelRegEx.search(newline)
            print 'PC:', PC, ' ', newline
            
            if matches:
                # print 'has a label', matches.group(1), matches.group(2)
                # the "matches" get whatever strings matches regular expressions, so "group(1) is the first 'label block'"
                # group(1) is the first '(.*)' of '(.*):\s+(.*)'
                Label[matches.group(1)] = PC
                # if it is the label line, the newline should be trimed off the label -> then it can be splitted to op and arg
                newline = matches.group(2)
                
            # currently the 'newline' is in the form of 'li	r1, 100'
            # split the line into opcode and arguments, putting into a list of two elements (opcode and arguments)
            opcode_arg_list = re.split('\s+', newline, 1)
            print 'the opcode and arg list is: ', opcode_arg_list
            # check if the opcode is in the Opcode dictionary
            check_opcode = opcode_arg_list[0]
            try:
                check_opcode in Opcode
            except ValueError:
                print "The opcode is invalid"
            
            opcode = opcode_arg_list[0]
    
            # now the 'opcode_arg_list' is in the form of '['li', 'r1, 100']'
            # Fill in the opcode of the machine instruction
            Mcode[PC] = Opcode[opcode][0] << 9 # shift 3 regs
                
            # Run any code associated with this instruction
            # eval($Opcode{$opcode}->[2]) if (defined($Opcode{$opcode}->[2]));
            
            # Get the arguments as a list
            arg_string = opcode_arg_list[1]
            arg_list = re.split(',\s*', arg_string, 1)
            print 'the argument list is:', arg_list
            
            # Check if the number of arguments is correct
            num_args = len(arg_list)
            try:
                num_args == len(Opcode[opcode][1])
            except ValueError:
                print "The number of arguments is invalid"
            
        # start from here:
            # Process the arguments
            
            
            # at the end of each loop for parsing the lines, add 1 to PC value
            PC += 1        
            
    
    
    
#   input file from command line
#   open and read the input file which is the assembling language
IN = sys.argv[-1]
f = open(IN, "rb")
contents = f.read()
        
        
def main():
    print '\nrun pre_processing\n'
    print 'pre_processed result is as below:\n'
    pre_process(contents)
    print 'pre_processing finished'

if __name__ == '__main__':
    main()
    











