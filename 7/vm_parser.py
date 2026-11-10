"""Parser for Nand2Tetris Project 7 VM instructions."""
from enum import Enum

class CommandType(Enum):
    C_ARITMETIC = 0
    C_PUSH = 1
    C_POP = 2
    C_LABEL = 3
    C_GOTO = 4
    C_IF = 5
    C_FUNCTION = 6
    C_RETURN = 7
    C_CALL = 8
    C_NONE = 9

arithmetic_all = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']
arithmetic_comp = ['eq', 'gt', 'lt']
arithmetic_unary = ['neg', 'not']
arithmetic_binary = ['add', 'sub', 'and', 'or']

class Parser:
    def __init__(self, inputfile):
        self._inputfile = inputfile
        self._lines = []
        self._preprocessFile()
        self._cur = -1
        self._ctype = CommandType.C_NONE
        self._carg1 = None
        self._carg2 = None

    def hasMoreLines(self):
        return self._cur + 1 < len(self._lines)

    def advance(self):
        if not self.hasMoreLines():
            raise StopIteration('No VM commands remaining')
        self._cur += 1
        self._interpretLine()

    def curLine(self):
        assert self._cur >= 0, 'No current VM command'
        return self._lines[self._cur]

    def commandType(self):
        return self._ctype

    def arg1(self):
        assert self._ctype != CommandType.C_RETURN
        return self._carg1

    def arg2(self):
        assert self._ctype in (CommandType.C_PUSH, CommandType.C_POP,
                               CommandType.C_FUNCTION, CommandType.C_CALL)
        return self._carg2

    def _interpretLine(self):
        tokens = self.curLine().split()
        operation = tokens[0]
        self._carg1 = None
        self._carg2 = None
        if operation in arithmetic_all:
            self._ctype = CommandType.C_ARITMETIC
            self._carg1 = operation
        elif operation in ('push', 'pop'):
            self._ctype = CommandType.C_PUSH if operation == 'push' else CommandType.C_POP
            self._carg1 = tokens[1]
            self._carg2 = int(tokens[2])
        else:
            raise ValueError(f'Unsupported Project 7 VM command: {self.curLine()}')

    def _preprocessFile(self):
        with open(self._inputfile, encoding='utf-8') as f:
            for line in f:
                line = line.split('//', 1)[0].strip()
                if line:
                    self._lines.append(line)
