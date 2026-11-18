"""Generate Hack assembly for Nand2Tetris Project 7."""
import os
from vm_parser import CommandType, arithmetic_all

standard_pushd = '@SP\nA=M\nM=D\n@SP\nM=M+1\n'


class CodeWriter:
    def __init__(self, outfile=None):
        self._outfile = outfile or './Garbage.asm'
        # Each comparison gets unique labels so repeated commands do not collide.
        self.comp_counts = {'lt': 0, 'eq': 0, 'gt': 0}
        self.static_count = 0
        # Use the output's base name for comments, static symbols, and comparison labels.
        self.static_name = self.extract_static_name(self._outfile)
        # Start a fresh output file and identify the translated VM file in its header.
        with open(self._outfile, 'w', encoding='utf-8') as f:
            f.write(f'// VM translation output: {self.static_name}\n')

    def _write(self, assembly):
        # Append each generated assembly fragment to the output file.
        with open(self._outfile, 'a', encoding='utf-8') as f:
            f.write(assembly)

    def gettwo(self):
        # For a binary operation, remove y into D and leave x at the top for the result.
        return '@SP\nAM=M-1\nD=M\nA=A-1\n'

    def getone(self):
        # Unary operations change the top value in place, so SP does not move.
        return '@SP\nA=M-1\n'

    def writeArithmetic(self, command):
        assert command in arithmetic_all
        self.writeComment(command)
        binary = {'add': 'M=D+M', 'sub': 'M=M-D',
                  'and': 'M=D&M', 'or': 'M=D|M'}
        unary = {'neg': 'M=-M', 'not': 'M=!M'}
        if command in binary:
            # D holds y and M holds x; replace x with the operation result.
            self._write(self.gettwo() + binary[command] + '\n')
        elif command in unary:
            self._write(self.getone() + unary[command] + '\n')
        else:
            # VM true is -1, VM false is 0.
            # Subtract the stack values, then use a signed jump to choose true or false.
            number = self.comp_counts[command]
            self.comp_counts[command] += 1
            true_label = f'{self.static_name}.{command}.{number}.TRUE'
            end_label = f'{self.static_name}.{command}.{number}.END'
            jump = {'eq': 'JEQ', 'gt': 'JGT', 'lt': 'JLT'}[command]
            asm = (self.gettwo() + 'D=M-D\n'
                   + f'@{true_label}\nD;{jump}\n'
                   + '@SP\nA=M-1\nM=0\n'
                   + f'@{end_label}\n0;JMP\n'
                   + f'({true_label})\n@SP\nA=M-1\nM=-1\n'
                   + f'({end_label})\n')
            self._write(asm)

    def writePushPop(self, command, segment, index):
        assert command in (CommandType.C_PUSH, CommandType.C_POP)
        self.writeComment(f'{command.name} {segment} {index}')
        if segment == 'static':
            # Static values have their own symbols rather than a fixed RAM base.
            self.staticPushPop(command, index)
            return
        if segment == 'constant':
            if command != CommandType.C_PUSH:
                raise ValueError('Cannot pop to constant')
            # The constant is an immediate value, not a writable memory location.
            self._write(f'@{index}\nD=A\n' + standard_pushd)
            return
        bases = {'local': 'LCL', 'argument': 'ARG',
                 'this': 'THIS', 'that': 'THAT'}
        if segment in bases:
            base = bases[segment]
            if command == CommandType.C_PUSH:
                # Read RAM[base + index], then push that value onto the stack.
                self._write(f'@{base}\nD=M\n@{index}\nA=D+A\nD=M\n'
                            + standard_pushd)
            else:
                # Save base + index before popping, since the pop changes the stack pointer.
                self._write(f'@{base}\nD=M\n@{index}\nD=D+A\n'
                            '@R13\nM=D\n@SP\nAM=M-1\nD=M\n'
                            '@R13\nA=M\nM=D\n')
            return
        if segment == 'temp':
            if not 0 <= index <= 7:
                raise ValueError('temp index must be 0..7')
            # The temp segment maps directly to RAM addresses 5 through 12.
            address = 5 + index
        elif segment == 'pointer':
            if index not in (0, 1):
                raise ValueError('pointer index must be 0 or 1')
            address = 3 + index  # RAM[3] = THIS; RAM[4] = THAT
        else:
            raise ValueError(f'Unknown VM segment: {segment}')
        if command == CommandType.C_PUSH:
            # These segments already map to one RAM address; read or write it directly.
            self._write(f'@{address}\nD=M\n' + standard_pushd)
        else:
            self._write(f'@SP\nAM=M-1\nD=M\n@{address}\nM=D\n')

    def staticPushPop(self, command, index):
        # Prefix the index with the file name to avoid collisions between VM files.
        varname = f'{self.static_name}.{index}'
        if command == CommandType.C_PUSH:
            self._write(f'@{varname}\nD=M\n' + standard_pushd)
        else:
            self._write(f'@SP\nAM=M-1\nD=M\n@{varname}\nM=D\n')

    def extract_static_name(self, filename):
        """Use the output file's base name as the VM file's static-symbol prefix."""
        return os.path.splitext(os.path.basename(filename))[0]

    def close(self):
        # Keep the CPU in a loop after the translated program finishes.
        self._write('(END)\n@END\n0;JMP\n')

    def writeComment(self, comment):
        self._write(f'\n// {comment}\n')

