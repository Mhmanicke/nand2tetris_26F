
# ECEG 431 - Project 6
# Code.py
#
# Converts Hack assembly mnemonics into binary.
# Each dictionary connects an assembly command
# with its corresponding binary representation.

class Code:

    def __init__(self):

        # Destination bits (3 bits).
        # These determine where the ALU result goes.
        self.dest_table = {
            "":    "000",
            "M":   "001",
            "D":   "010",
            "MD":  "011",
            "DM":  "011",
            "A":   "100",
            "AM":  "101",
            "MA":  "101",
            "AD":  "110",
            "DA":  "110",
            "AMD": "111",
            "ADM": "111",
            "MAD": "111",
            "MDA": "111",
            "DAM": "111",
            "DMA": "111"
        }

        # Computation bits (7 bits).
        # The first bit selects A or M.
        # The remaining six bits control the ALU.
        self.comp_table = {
            "0":   "0101010",
            "1":   "0111111",
            "-1":  "0111010",
            "D":   "0001100",
            "A":   "0110000",
            "!D":  "0001101",
            "!A":  "0110001",
            "-D":  "0001111",
            "-A":  "0110011",
            "D+1": "0011111",
            "A+1": "0110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "D+A": "0000010",
            "D-A": "0010011",
            "A-D": "0000111",
            "D&A": "0000000",
            "D|A": "0010101",

            "M":   "1110000",
            "!M":  "1110001",
            "-M":  "1110011",
            "M+1": "1110111",
            "M-1": "1110010",
            "D+M": "1000010",
            "D-M": "1010011",
            "M-D": "1000111",
            "D&M": "1000000",
            "D|M": "1010101"
        }

        # Jump bits (3 bits).
        # These determine when the computer jumps.
        self.jump_table = {
            "":    "000",
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111"
        }

    def dest(self, mnemonic):
        # Return the 3-bit destination code.
        return self.dest_table[mnemonic]

    def comp(self, mnemonic):
        # Return the 7-bit computation code.
        return self.comp_table[mnemonic]

    def jump(self, mnemonic):
        # Return the 3-bit jump code.
        return self.jump_table[mnemonic]
