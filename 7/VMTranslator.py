"""Project 7 command-line VM translator."""
import sys
from pathlib import Path
from vm_codewriter import CodeWriter
from vm_parser import CommandType, Parser

def vm_translate(inputfile):
    """Translate one Project 7 VM file into a neighboring Hack assembly file."""
    inputfile = Path(inputfile)
    if inputfile.suffix.lower() != '.vm':
        raise ValueError('Please supply a .vm file')

    # Replace only the extension, so Program.vm becomes Program.asm in the same folder.
    outputfile = inputfile.with_suffix('.asm')
    parser = Parser(str(inputfile))
    coder = CodeWriter(str(outputfile))

    # The parser identifies each VM command; the code writer handles its assembly.
    while parser.hasMoreLines():
        parser.advance()
        # Keep the original command in the assembly as a comment for easier debugging.
        coder.writeComment(parser.curLine())
        kind = parser.commandType()
        if kind == CommandType.C_ARITMETIC:
            # Arithmetic commands need only their operation name (for example, "add").
            coder.writeArithmetic(parser.arg1())
        elif kind in (CommandType.C_PUSH, CommandType.C_POP):
            # Memory commands also need a segment (like "local") and an index.
            coder.writePushPop(kind, parser.arg1(), parser.arg2())
        else:
            raise ValueError(f'Unsupported command: {parser.curLine()}')

    # Finish the assembly with a halt loop, then tell the user where it was written.
    coder.close()
    print(f'Created {outputfile}')


if __name__ == '__main__':
    # This block runs only when the file is launched directly from the command line.
    if len(sys.argv) != 2:
        print('Usage: python VMTranslator.py path/to/Program.vm')
        sys.exit(1)
    vm_translate(sys.argv[1])

