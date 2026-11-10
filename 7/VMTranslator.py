"""Project 7 command-line VM translator."""
import sys
from pathlib import Path
from vm_codewriter import CodeWriter
from vm_parser import CommandType, Parser

def vm_translate(inputfile):
    inputfile = Path(inputfile)
    if inputfile.suffix.lower() != '.vm':
        raise ValueError('Please supply a .vm file')
    outputfile = inputfile.with_suffix('.asm')
    parser = Parser(str(inputfile))
    coder = CodeWriter(str(outputfile))
    while parser.hasMoreLines():
        parser.advance()
        coder.writeComment(parser.curLine())
        kind = parser.commandType()
        if kind == CommandType.C_ARITMETIC:
            coder.writeArithmetic(parser.arg1())
        elif kind in (CommandType.C_PUSH, CommandType.C_POP):
            coder.writePushPop(kind, parser.arg1(), parser.arg2())
        else:
            raise ValueError(f'Unsupported command: {parser.curLine()}')
    coder.close()
    print(f'Created {outputfile}')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python VMTranslator.py path/to/Program.vm')
        sys.exit(1)
    vm_translate(sys.argv[1])
