// video 4.10 exercise 

// if R1 > R2
@R1
D=M
@R2
D = D - M
@ONE
D;JGT
//else (R1 <= R2)
@R2
D=M 
// @finally: the reason is to jump over (ONE). We skip because we just executed 'else', so we want to avoide (ONE). 
@FINALLY
0;JMP
(ONE)
@R1
D=M
(FINALLY)
// we now put the current D inside M(R0).
@R0 
M=D
// infinite loop to avoide NOP slide
(END)
@END
0;JMP

