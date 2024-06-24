
// push
@10
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// pop
@LCL
D = M
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
@21
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// push
@22
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// pop
@ARG
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

// pop
@ARG
D = M
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
@36
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
@42
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// push
@45
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
@5
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

// pop
@THAT
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
@510
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// pop
@5
D = A
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
@LCL
D = M
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
@THAT
D = M
@5
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
@ARG
D = M
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
@THIS
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

// push
@THIS
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
@5
D = A
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
