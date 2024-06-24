
// push
@7
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// push
@8
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// add
// storing x in R13, updates SP
@SP
D = M - 1
@R13
M = D
@SP
M = M - 1
// performing addition
@R13
A = M
D = M
A = A - 1
M = M + D
// (optional, only for cleanness) deleting SP's trash value (y)
A = A + 1
M = 0
