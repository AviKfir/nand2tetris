// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// put zero in R2 (my result line) just in case.
@R2
M=0

(STOPPING_CONDITION)
// if R0 is greater than 0 -> do loop
@R0
D=M
@LOOP
D;JGT
// else
@END
0;JMP

(LOOP)
@R1
D=M
@R2
M = M + D
@R0
M = M - 1
@STOPPING_CONDITION
0;JMP


(END)
@END
0;JMP