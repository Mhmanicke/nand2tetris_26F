"""Parser for Nand2Tetris Project 7 VM instructions."""
from enum import Enum

class CommandType(Enum):
    # Project 7 uses arithmetic, push, and pop. The remaining types are for later projects.
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
        # Store only real commands; the position starts before the first command.
        self._preprocessFile()
        self._cur = -1
        self._ctype = CommandType.C_NONE
        self._carg1 = None
        self._carg2 = None

    def hasMoreLines(self):
        """Return whether there is another cleaned command to parse."""
        return self._cur + 1 < len(self._lines)

    def advance(self):
        """Move to the next command and update its type and arguments."""
        if not self.hasMoreLines():
            raise StopIteration('No VM commands remaining')
        self._cur += 1
        self._interpretLine()

    def curLine(self):
        """Return the current command's cleaned text."""
        assert self._cur >= 0, 'No current VM command'
        return self._lines[self._cur]

    def commandType(self):
        """Return the current command category, such as C_PUSH or C_ARITMETIC."""
        return self._ctype

    def arg1(self):
        """Return the operation name or first argument of the current command."""
        assert self._ctype != CommandType.C_RETURN
        return self._carg1

    def arg2(self):
        """Return the numeric index used by push, pop, function, or call commands."""
        assert self._ctype in (CommandType.C_PUSH, CommandType.C_POP,
                               CommandType.C_FUNCTION, CommandType.C_CALL)
        return self._carg2

    def _interpretLine(self):
        tokens = self.curLine().split()
        operation = tokens[0]
        # Reset arguments so values from the previous command cannot carry over.
        self._carg1 = None
        self._carg2 = None

        # Arithmetic commands use their operation as arg1; push/pop use segment and index.
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
        """Remove comments and blank lines before the parser walks the file."""
        with open(self._inputfile, encoding='utf-8') as f:
            for line in f:
                # Split also removes inline comments, e.g. "add // sum the top two".
                line = line.split('//', 1)[0].strip()
                if line:
                    self._lines.append(line)

