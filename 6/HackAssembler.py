
# ECEG 431 - Project 6
# HackAssembler.py
#
# Main assembler program.
# Takes a Hack .asm file and translates it
# into a .hack file containing 16-bit binary.
#
# Uses Parser, Code, and SymbolTable classes.

import sys
from pathlib import Path

from Parser import Parser
from Code import Code
from SymbolTable import SymbolTable


def assemble(filename):

    # Create our helper objects.
    parser = Parser(filename)
    coder = Code()
    symbols = SymbolTable()

    # ---------------------------------------
    # FIRST PASS: Find all labels
    # ---------------------------------------

    # ROM address keeps track of the instruction
    # number in the final machine code.
    rom_address = 0

    while parser.hasMoreLines():
        parser.advance()

        instruction_type = parser.instructionType()

        if instruction_type == "L_INSTRUCTION":
            # Labels do not create machine code.
            # Store the address of the next
            # actual instruction.
            label = parser.symbol()
            symbols.addEntry(label, rom_address)

        else:
            # Only A- and C-instructions count
            # toward the ROM address.
            rom_address += 1

    # ---------------------------------------
    # SECOND PASS: Translate instructions
    # ---------------------------------------

    # Create a new Parser so we start at
    # the beginning of the assembly file.
    parser = Parser(filename)

    # New variables begin at RAM address 16.
    ram_address = 16

    # Store the completed binary instructions.
    binary_instructions = []

    while parser.hasMoreLines():
        parser.advance()

        instruction_type = parser.instructionType()

        # -----------------------------------
        # Handle A-instructions
        # -----------------------------------

        if instruction_type == "A_INSTRUCTION":

            # Get everything after the @ symbol.
            symbol = parser.symbol()

            if symbol.isdigit():
                # Example: @5
                # Convert the number directly.
                address = int(symbol)

            else:
                # Example: @LOOP or @counter

                if not symbols.contains(symbol):
                    # If this is a new variable,
                    # give it the next free RAM address.
                    symbols.addEntry(symbol, ram_address)
                    ram_address += 1

                # Find the address of the symbol.
                address = symbols.getAddress(symbol)

            # Convert the address into 16-bit binary.
            # A-instructions always start with 0.
            binary = format(address, "016b")

            binary_instructions.append(binary)

        # -----------------------------------
        # Handle C-instructions
        # -----------------------------------

        elif instruction_type == "C_INSTRUCTION":

            # Separate the three components.
            dest = parser.dest()
            comp = parser.comp()
            jump = parser.jump()

            # Convert each component into binary.
            comp_bits = coder.comp(comp)
            dest_bits = coder.dest(dest)
            jump_bits = coder.jump(jump)

            # C-instructions begin with 111.
            # Format: 111 + comp + dest + jump
            binary = (
                "111"
                + comp_bits
                + dest_bits
                + jump_bits
            )

            binary_instructions.append(binary)

        # Labels are ignored in the second pass
        # because they do not produce binary code.

    # ---------------------------------------
    # CREATE THE OUTPUT FILE
    # ---------------------------------------

    # Replace .asm with .hack.
    # Keep the output in the same folder.
    output_filename = Path(filename).with_suffix(".hack")

    # Write each 16-bit instruction on a new line.
    # Existing .hack files are overwritten.
    with open(output_filename, "w") as file:
        file.write("\n".join(binary_instructions))

    print("Assembly completed successfully!")
    print("Output file:", output_filename)


# -------------------------------------------
# RUN THE ASSEMBLER
# -------------------------------------------

if __name__ == "__main__":

    # Check that the user provided a filename.
    if len(sys.argv) != 2:
        print("Usage: python HackAssembler.py Prog.asm")

    else:
        # Assemble the provided assembly file.
        assemble(sys.argv[1])
