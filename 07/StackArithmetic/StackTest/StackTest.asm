
// push
@17
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// push
@17
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// eq
@SP
A = M - 1
A = A - 1
D = M
// if x > 0, need to check if y < 0
@CHECK_NEG1
D;JGT
// else: x <= 0, so need to check if y > 0
@SP
A = M - 1
D = M
@OVERFLOW1.1
// if y > 0, overflow risk confirmed
D;JGT
@CONTINUE1
0;JMP
(CHECK_NEG1)
@SP
A = M - 1
D = M
@OVERFLOW2.1
// if y < 0, overflow risk confirmed
D;JLT
@CONTINUE1
0;JMP
(OVERFLOW1.1)
// x < 0 and y > 0
@SP
A = M - 1
A = A - 1
M = 0
@SP
A = M - 1
M = 1
@CONTINUE1
0;JMP
(OVERFLOW2.1)
// x > 0 and y < 0
@SP
A = M - 1
A = A - 1
M = 1
@SP
A = M - 1
M = 0
(CONTINUE1)

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
// performing equality
@SP
A = M - 1
D = M
@TRUE1
// if D = 0 than it means that x = y
D;JEQ
// else (false)
@SP
A = M - 1
M = 0
@END1
0;JMP
(TRUE1)
@SP
A = M - 1
M = -1
(END1)

// push
@17
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// push
@16
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// eq
@SP
A = M - 1
A = A - 1
D = M
// if x > 0, need to check if y < 0
@CHECK_NEG2
D;JGT
// else: x <= 0, so need to check if y > 0
@SP
A = M - 1
D = M
@OVERFLOW1.2
// if y > 0, overflow risk confirmed
D;JGT
@CONTINUE2
0;JMP
(CHECK_NEG2)
@SP
A = M - 1
D = M
@OVERFLOW2.2
// if y < 0, overflow risk confirmed
D;JLT
@CONTINUE2
0;JMP
(OVERFLOW1.2)
// x < 0 and y > 0
@SP
A = M - 1
A = A - 1
M = 0
@SP
A = M - 1
M = 1
@CONTINUE2
0;JMP
(OVERFLOW2.2)
// x > 0 and y < 0
@SP
A = M - 1
A = A - 1
M = 1
@SP
A = M - 1
M = 0
(CONTINUE2)

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
// performing equality
@SP
A = M - 1
D = M
@TRUE2
// if D = 0 than it means that x = y
D;JEQ
// else (false)
@SP
A = M - 1
M = 0
@END2
0;JMP
(TRUE2)
@SP
A = M - 1
M = -1
(END2)

// push
@16
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// push
@17
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// eq
@SP
A = M - 1
A = A - 1
D = M
// if x > 0, need to check if y < 0
@CHECK_NEG3
D;JGT
// else: x <= 0, so need to check if y > 0
@SP
A = M - 1
D = M
@OVERFLOW1.3
// if y > 0, overflow risk confirmed
D;JGT
@CONTINUE3
0;JMP
(CHECK_NEG3)
@SP
A = M - 1
D = M
@OVERFLOW2.3
// if y < 0, overflow risk confirmed
D;JLT
@CONTINUE3
0;JMP
(OVERFLOW1.3)
// x < 0 and y > 0
@SP
A = M - 1
A = A - 1
M = 0
@SP
A = M - 1
M = 1
@CONTINUE3
0;JMP
(OVERFLOW2.3)
// x > 0 and y < 0
@SP
A = M - 1
A = A - 1
M = 1
@SP
A = M - 1
M = 0
(CONTINUE3)

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
// performing equality
@SP
A = M - 1
D = M
@TRUE3
// if D = 0 than it means that x = y
D;JEQ
// else (false)
@SP
A = M - 1
M = 0
@END3
0;JMP
(TRUE3)
@SP
A = M - 1
M = -1
(END3)

// push
@892
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// push
@891
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// lt
@SP
A = M - 1
A = A - 1
D = M
// if x > 0, need to check if y < 0
@CHECK_NEG4
D;JGT
// else: x <= 0, so need to check if y > 0
@SP
A = M - 1
D = M
@OVERFLOW1.4
// if y > 0, overflow risk confirmed
D;JGT
@CONTINUE4
0;JMP
(CHECK_NEG4)
@SP
A = M - 1
D = M
@OVERFLOW2.4
// if y < 0, overflow risk confirmed
D;JLT
@CONTINUE4
0;JMP
(OVERFLOW1.4)
// x < 0 and y > 0
@SP
A = M - 1
A = A - 1
M = 0
@SP
A = M - 1
M = 1
@CONTINUE4
0;JMP
(OVERFLOW2.4)
// x > 0 and y < 0
@SP
A = M - 1
A = A - 1
M = 1
@SP
A = M - 1
M = 0
(CONTINUE4)

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
// performing equality
@SP
A = M - 1
D = M
@TRUE4
// if D = 0 than it means that x = y
D;JLT
// else (false)
@SP
A = M - 1
M = 0
@END4
0;JMP
(TRUE4)
@SP
A = M - 1
M = -1
(END4)

// push
@891
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// push
@892
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// lt
@SP
A = M - 1
A = A - 1
D = M
// if x > 0, need to check if y < 0
@CHECK_NEG5
D;JGT
// else: x <= 0, so need to check if y > 0
@SP
A = M - 1
D = M
@OVERFLOW1.5
// if y > 0, overflow risk confirmed
D;JGT
@CONTINUE5
0;JMP
(CHECK_NEG5)
@SP
A = M - 1
D = M
@OVERFLOW2.5
// if y < 0, overflow risk confirmed
D;JLT
@CONTINUE5
0;JMP
(OVERFLOW1.5)
// x < 0 and y > 0
@SP
A = M - 1
A = A - 1
M = 0
@SP
A = M - 1
M = 1
@CONTINUE5
0;JMP
(OVERFLOW2.5)
// x > 0 and y < 0
@SP
A = M - 1
A = A - 1
M = 1
@SP
A = M - 1
M = 0
(CONTINUE5)

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
// performing equality
@SP
A = M - 1
D = M
@TRUE5
// if D = 0 than it means that x = y
D;JLT
// else (false)
@SP
A = M - 1
M = 0
@END5
0;JMP
(TRUE5)
@SP
A = M - 1
M = -1
(END5)

// push
@891
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// push
@891
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// lt
@SP
A = M - 1
A = A - 1
D = M
// if x > 0, need to check if y < 0
@CHECK_NEG6
D;JGT
// else: x <= 0, so need to check if y > 0
@SP
A = M - 1
D = M
@OVERFLOW1.6
// if y > 0, overflow risk confirmed
D;JGT
@CONTINUE6
0;JMP
(CHECK_NEG6)
@SP
A = M - 1
D = M
@OVERFLOW2.6
// if y < 0, overflow risk confirmed
D;JLT
@CONTINUE6
0;JMP
(OVERFLOW1.6)
// x < 0 and y > 0
@SP
A = M - 1
A = A - 1
M = 0
@SP
A = M - 1
M = 1
@CONTINUE6
0;JMP
(OVERFLOW2.6)
// x > 0 and y < 0
@SP
A = M - 1
A = A - 1
M = 1
@SP
A = M - 1
M = 0
(CONTINUE6)

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
// performing equality
@SP
A = M - 1
D = M
@TRUE6
// if D = 0 than it means that x = y
D;JLT
// else (false)
@SP
A = M - 1
M = 0
@END6
0;JMP
(TRUE6)
@SP
A = M - 1
M = -1
(END6)

// push
@32767
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// push
@32766
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// gt
@SP
A = M - 1
A = A - 1
D = M
// if x > 0, need to check if y < 0
@CHECK_NEG7
D;JGT
// else: x <= 0, so need to check if y > 0
@SP
A = M - 1
D = M
@OVERFLOW1.7
// if y > 0, overflow risk confirmed
D;JGT
@CONTINUE7
0;JMP
(CHECK_NEG7)
@SP
A = M - 1
D = M
@OVERFLOW2.7
// if y < 0, overflow risk confirmed
D;JLT
@CONTINUE7
0;JMP
(OVERFLOW1.7)
// x < 0 and y > 0
@SP
A = M - 1
A = A - 1
M = 0
@SP
A = M - 1
M = 1
@CONTINUE7
0;JMP
(OVERFLOW2.7)
// x > 0 and y < 0
@SP
A = M - 1
A = A - 1
M = 1
@SP
A = M - 1
M = 0
(CONTINUE7)

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
// performing equality
@SP
A = M - 1
D = M
@TRUE7
// if D = 0 than it means that x = y
D;JGT
// else (false)
@SP
A = M - 1
M = 0
@END7
0;JMP
(TRUE7)
@SP
A = M - 1
M = -1
(END7)

// push
@32766
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// push
@32767
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// gt
@SP
A = M - 1
A = A - 1
D = M
// if x > 0, need to check if y < 0
@CHECK_NEG8
D;JGT
// else: x <= 0, so need to check if y > 0
@SP
A = M - 1
D = M
@OVERFLOW1.8
// if y > 0, overflow risk confirmed
D;JGT
@CONTINUE8
0;JMP
(CHECK_NEG8)
@SP
A = M - 1
D = M
@OVERFLOW2.8
// if y < 0, overflow risk confirmed
D;JLT
@CONTINUE8
0;JMP
(OVERFLOW1.8)
// x < 0 and y > 0
@SP
A = M - 1
A = A - 1
M = 0
@SP
A = M - 1
M = 1
@CONTINUE8
0;JMP
(OVERFLOW2.8)
// x > 0 and y < 0
@SP
A = M - 1
A = A - 1
M = 1
@SP
A = M - 1
M = 0
(CONTINUE8)

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
// performing equality
@SP
A = M - 1
D = M
@TRUE8
// if D = 0 than it means that x = y
D;JGT
// else (false)
@SP
A = M - 1
M = 0
@END8
0;JMP
(TRUE8)
@SP
A = M - 1
M = -1
(END8)

// push
@32766
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// push
@32766
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// gt
@SP
A = M - 1
A = A - 1
D = M
// if x > 0, need to check if y < 0
@CHECK_NEG9
D;JGT
// else: x <= 0, so need to check if y > 0
@SP
A = M - 1
D = M
@OVERFLOW1.9
// if y > 0, overflow risk confirmed
D;JGT
@CONTINUE9
0;JMP
(CHECK_NEG9)
@SP
A = M - 1
D = M
@OVERFLOW2.9
// if y < 0, overflow risk confirmed
D;JLT
@CONTINUE9
0;JMP
(OVERFLOW1.9)
// x < 0 and y > 0
@SP
A = M - 1
A = A - 1
M = 0
@SP
A = M - 1
M = 1
@CONTINUE9
0;JMP
(OVERFLOW2.9)
// x > 0 and y < 0
@SP
A = M - 1
A = A - 1
M = 1
@SP
A = M - 1
M = 0
(CONTINUE9)

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
// performing equality
@SP
A = M - 1
D = M
@TRUE9
// if D = 0 than it means that x = y
D;JGT
// else (false)
@SP
A = M - 1
M = 0
@END9
0;JMP
(TRUE9)
@SP
A = M - 1
M = -1
(END9)

// push
@57
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// push
@31
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// push
@53
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

// push
@112
D = A
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

// neg
@SP
A = M - 1
M = -M

// and
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
M = D & M
// (optional, only for cleanness) deleting SP's trash value (y)
A = A + 1
M = 0

// push
@82
D = A
// push in stack (D = element to push)
@SP
A = M
M = D
@SP
M = M + 1

// or
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
M = D | M
// (optional, only for cleanness) deleting SP's trash value (y)
A = A + 1
M = 0

// not
@SP
A = M - 1
M = !M
