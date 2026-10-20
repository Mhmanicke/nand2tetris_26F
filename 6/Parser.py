
# ECEG 431 - Project 6
# Parser.py
#
# This class reads a Hack assembly file and separates
# each instruction into its individual components.

class Parser:

    def __init__(self, filename):
        # Open the assembly file and read every line.
        with open(filename, "r") as file:
            lines = file.readlines()

        # Store only actual instructions.
        self.instructions = []

        for line in lines:
            # Remove comments beginning with //.
            line = line.split("//")[0]

            # Remove spaces, tabs, and newline characters.
            line = "".join(line.split())

            # Ignore empty lines.
            if line:
                self.instructions.append(line)

        # Keep track of the current instruction.
        self.current_index = -1
        self.current_instruction = None

    def hasMoreLines(self):
        # Return True if another instruction exists.
        return self.current_index + 1 < len(self.instructions)

    def advance(self):
        # Move to the next instruction.
        if self.hasMoreLines():
            self.current_index += 1
            self.current_instruction = self.instructions[self.current_index]

    def instructionType(self):
        # A-instructions begin with @.
        if self.current_instruction.startswith("@"):
            return "A_INSTRUCTION"

        # Labels are written inside parentheses.
        elif self.current_instruction.startswith("("):
            return "L_INSTRUCTION"

        # Everything else is a C-instruction.
        else:
            return "C_INSTRUCTION"

    def symbol(self):
        # Return the symbol or number from an
        # A-instruction or label.

        if self.instructionType() == "A_INSTRUCTION":
            return self.current_instruction[1:]

        elif self.instructionType() == "L_INSTRUCTION":
            return self.current_instruction[1:-1]

    def dest(self):
        # Destination is before the = sign.
        # Example: D=M gives destination D.

        if "=" in self.current_instruction:
            return self.current_instruction.split("=")[0]

        # No destination was specified.
        return ""

    def comp(self):
        # Computation is between = and ;.
        # Example: D=M+1 gives M+1.

        instruction = self.current_instruction

        if "=" in instruction:
            instruction = instruction.split("=")[1]

        if ";" in instruction:
            instruction = instruction.split(";")[0]

        return instruction

    def jump(self):
        # Jump instruction comes after ;.
        # Example: D;JGT gives JGT.

        if ";" in self.current_instruction:
            return self.current_instruction.split(";")[1]

        # No jump was specified.
        return ""
