// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.

// Fill.asm
// Continuously checks the keyboard.
//
// If ANY key is pressed:
//      Make the screen black.
//
// If NO key is pressed:
//      Make the screen white.

// START
// Reset our screen pointer to the beginning
// of screen memory.
(START)
    // Store the beginning of screen memory
    // inside our variable called address.
    @SCREEN
    D=A
    @address
    M=D

// CHECK KEYBOARD
(CHECKKEY)
    // Read the keyboard.
    // KBD = 0 means no key is being pressed.
    // KBD != 0 means some key is being pressed.
    @KBD
    D=M
    // If D equals 0, go make the screen white.
    @WHITE
    D;JEQ
    // Otherwise, a key is being pressed,
    // so go make the screen black.
    @BLACK
    0;JMP

// BLACK
// Makes one word of the screen black.
(BLACK)
    // Go to the current screen address.
    @address
    A=M
    // -1 = 1111111111111111 in binary.
    // Therefore all 16 pixels controlled by
    // this memory word become black.
    M=-1
    // Move our pointer to the next screen word.
    @address
    M=M+1
    // Check whether we have reached KBD.
    // KBD comes directly after screen memory,
    // so reaching KBD means the entire screen
    // has been filled.
    @KBD
    D=A
    @address
    D=M-D
    // If address == KBD, we are finished
    // filling the screen.
    @START
    D;JEQ
    // Otherwise continue making screen words black.
    @BLACK
    0;JMP

// WHITE
// Makes one word of the screen white.
(WHITE)
    // Go to the current screen address.
    @address
    A=M
    // 0 means all 16 bits are 0,
    // which makes these pixels white.
    M=0
    // Move to the next screen word.
    @address
    M=M+1
    // Check if we have reached the end
    // of screen memory.
    @KBD
    D=A
    @address
    D=M-D
    // If address == KBD, the whole screen
    // has been cleared.
    @START
    D;JEQ
    // Otherwise continue clearing the screen.
    @WHITE
    0;JMP