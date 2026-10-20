
# ECEG 431 - Project 6
# SymbolTable.py
#
# Stores symbols and their corresponding addresses.
# This includes predefined symbols, labels,
# and variables created by the assembly program.

class SymbolTable:

    def __init__(self):

        # Start with the predefined Hack symbols.
        self.table = {
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
            "SCREEN": 16384,
            "KBD": 24576
        }

        # Add registers R0 through R15.
        for i in range(16):
            self.table["R" + str(i)] = i

    def addEntry(self, symbol, address):
        # Add a new symbol and its address.
        self.table[symbol] = address

    def contains(self, symbol):
        # Check whether the symbol already exists.
        return symbol in self.table

    def getAddress(self, symbol):
        # Return the address stored for a symbol.
        return self.table[symbol]
