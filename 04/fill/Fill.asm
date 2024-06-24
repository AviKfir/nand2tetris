
(START)
@R1
M=0
(BLACK_OR_WHITE)
@KBD 
D=M
@WHITE
D;JEQ
//else black 

(BLACK)
@R1
D=M
@SCREEN
A = A + D
M=-1
// -1 = 1111111111111111 (Two's complement)
@LOOP
0;JMP

(WHITE)
@R1
D=M
@SCREEN
A = A + D
M=0
@LOOP
0;JMP

(LOOP)
@8191
D=A
@R1
D = D - M
// if D == 0 -> we looped over all 8192 rows of screen memory map. So we will return to check keybord.
@START 
D;JEQ 
//else
@R1
M = M + 1
@BLACK_OR_WHITE
0;JMP







