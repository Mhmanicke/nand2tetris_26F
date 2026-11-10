// VM translation output: StackTest

// push constant 17

// C_PUSH constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 17

// C_PUSH constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// eq

// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.eq.0.TRUE
D;JEQ
@SP
A=M-1
M=0
@StackTest.eq.0.END
0;JMP
(StackTest.eq.0.TRUE)
@SP
A=M-1
M=-1
(StackTest.eq.0.END)

// push constant 17

// C_PUSH constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 16

// C_PUSH constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1

// eq

// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.eq.1.TRUE
D;JEQ
@SP
A=M-1
M=0
@StackTest.eq.1.END
0;JMP
(StackTest.eq.1.TRUE)
@SP
A=M-1
M=-1
(StackTest.eq.1.END)

// push constant 16

// C_PUSH constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 17

// C_PUSH constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// eq

// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.eq.2.TRUE
D;JEQ
@SP
A=M-1
M=0
@StackTest.eq.2.END
0;JMP
(StackTest.eq.2.TRUE)
@SP
A=M-1
M=-1
(StackTest.eq.2.END)

// push constant 892

// C_PUSH constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 891

// C_PUSH constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt

// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.lt.0.TRUE
D;JLT
@SP
A=M-1
M=0
@StackTest.lt.0.END
0;JMP
(StackTest.lt.0.TRUE)
@SP
A=M-1
M=-1
(StackTest.lt.0.END)

// push constant 891

// C_PUSH constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 892

// C_PUSH constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt

// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.lt.1.TRUE
D;JLT
@SP
A=M-1
M=0
@StackTest.lt.1.END
0;JMP
(StackTest.lt.1.TRUE)
@SP
A=M-1
M=-1
(StackTest.lt.1.END)

// push constant 891

// C_PUSH constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 891

// C_PUSH constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt

// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.lt.2.TRUE
D;JLT
@SP
A=M-1
M=0
@StackTest.lt.2.END
0;JMP
(StackTest.lt.2.TRUE)
@SP
A=M-1
M=-1
(StackTest.lt.2.END)

// push constant 32767

// C_PUSH constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 32766

// C_PUSH constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// gt

// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.gt.0.TRUE
D;JGT
@SP
A=M-1
M=0
@StackTest.gt.0.END
0;JMP
(StackTest.gt.0.TRUE)
@SP
A=M-1
M=-1
(StackTest.gt.0.END)

// push constant 32766

// C_PUSH constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 32767

// C_PUSH constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

// gt

// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.gt.1.TRUE
D;JGT
@SP
A=M-1
M=0
@StackTest.gt.1.END
0;JMP
(StackTest.gt.1.TRUE)
@SP
A=M-1
M=-1
(StackTest.gt.1.END)

// push constant 32766

// C_PUSH constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 32766

// C_PUSH constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// gt

// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.gt.2.TRUE
D;JGT
@SP
A=M-1
M=0
@StackTest.gt.2.END
0;JMP
(StackTest.gt.2.TRUE)
@SP
A=M-1
M=-1
(StackTest.gt.2.END)

// push constant 57

// C_PUSH constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 31

// C_PUSH constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 53

// C_PUSH constant 53
@53
D=A
@SP
A=M
M=D
@SP
M=M+1

// add

// add
@SP
AM=M-1
D=M
A=A-1
M=D+M

// push constant 112

// C_PUSH constant 112
@112
D=A
@SP
A=M
M=D
@SP
M=M+1

// sub

// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D

// neg

// neg
@SP
A=M-1
M=-M

// and

// and
@SP
AM=M-1
D=M
A=A-1
M=D&M

// push constant 82

// C_PUSH constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1

// or

// or
@SP
AM=M-1
D=M
A=A-1
M=D|M

// not

// not
@SP
A=M-1
M=!M
(END)
@END
0;JMP
