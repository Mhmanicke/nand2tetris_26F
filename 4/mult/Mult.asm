// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.
//// Replace this comment with your code.

//Program flow:
//answer = 0
//counter = R1
//while counter > 0:
//    answer = answer + R0
//    counter = counter - 1
//
//R2 = answer


// Start the answer at 0
    @R2
    M=0
// Copy R1 into a counter.
// We use a separate counter because we are not
// allowed to change the original value in R1.
    @R0
    D=M
    @counter
    M=D
// Start of multiplication loop
(LOOP)
    // Check if counter has reached 0
    // If it has, multiplication is finished.
    @counter
    D=M
    @END
    D;JEQ
    // Add R0 to the current answer in R2
    @R1
    D=M
    @R2
    M=D+M
    // Decrease counter by 1
    @counter
    M=M-1
    // Repeat the loop
    @LOOP
    0;JMP
// When multiplication is finished,
// stay here forever.
(END)
    @END
    0;JMP