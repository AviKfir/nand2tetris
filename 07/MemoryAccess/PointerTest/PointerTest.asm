
// push
@3030
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// pop
@3
D = A
@0
D = D + A
@13
M = D
// pop from stack (saving in D) 
@SP
AM = M - 1
D = M
// (optional, only for cleanness) deleting SP's trash value (y)
M = 0
@13
A = M
M = D

// push
@3040
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// pop
@3
D = A
@1
D = D + A
@13
M = D
// pop from stack (saving in D) 
@SP
AM = M - 1
D = M
// (optional, only for cleanness) deleting SP's trash value (y)
M = 0
@13
A = M
M = D

// push
@32
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// pop
@THIS
D = M
@2
D = D + A
@13
M = D
// pop from stack (saving in D) 
@SP
AM = M - 1
D = M
// (optional, only for cleanness) deleting SP's trash value (y)
M = 0
@13
A = M
M = D

// push
@46
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// pop
@THAT
D = M
@6
D = D + A
@13
M = D
// pop from stack (saving in D) 
@SP
AM = M - 1
D = M
// (optional, only for cleanness) deleting SP's trash value (y)
M = 0
@13
A = M
M = D

// push
@3
D = A
@0
D = D + A
A = D
D = M
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// push
@3
D = A
@1
D = D + A
A = D
D = M
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

// push
@THIS
D = M
@2
D = D + A
A = D
D = M
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// sub
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
M = M - D
// (optional, only for cleanness) deleting SP's trash value (y)
A = A + 1
M = 0

// push
@THAT
D = M
@6
D = D + A
A = D
D = M
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
