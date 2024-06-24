
// push
@111
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// push
@333
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// push
@888
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// pop
@StaticTest.8
D = A
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

// pop
@StaticTest.3
D = A
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

// pop
@StaticTest.1
D = A
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
@StaticTest.3
D = M
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// push
@StaticTest.1
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
@StaticTest.8
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
