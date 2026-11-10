"""Generate Hack assembly for Nand2Tetris Project 7."""
import os
from vm_parser import CommandType, arithmetic_all

standard_pushd = '@SP\nA=M\nM=D\n@SP\nM=M+1\n'

class CodeWriter:
    def __init__(self, outfile=None):
        self._outfile = outfile or './Garbage.asm'
        self.comp_counts = {'lt': 0, 'eq': 0, 'gt': 0}
        self.static_count = 0
        self.static_name = self.extract_static_name(self._outfile)
        with open(self._outfile, 'w', encoding='utf-8') as f:
            f.write(f'// VM translation output: {self.static_name}\n')

    def _write(self, assembly):
        with open(self._outfile, 'a', encoding='utf-8') as f:
            f.write(assembly)

    def gettwo(self):
        # Pop y into D, leaving A pointing at x (which will hold result).
        return '@SP\nAM=M-1\nD=M\nA=A-1\n'

    def getone(self):
        # Point A at the top stack element without removing it.
        return '@SP\nA=M-1\n'

    def writeArithmetic(self, command):
        assert command in arithmetic_all
        self.writeComment(command)
        binary = {'add': 'M=D+M', 'sub': 'M=M-D',
                  'and': 'M=D&M', 'or': 'M=D|M'}
        unary = {'neg': 'M=-M', 'not': 'M=!M'}
        if command in binary:
            self._write(self.gettwo() + binary[command] + '\n')
        elif command in unary:
            self._write(self.getone() + unary[command] + '\n')
        else:
            # VM true is -1, VM false is 0.
            # Use a unique pair of labels for every comparison.
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
            self.staticPushPop(command, index)
            return
        if segment == 'constant':
            if command != CommandType.C_PUSH:
                raise ValueError('Cannot pop to constant')
            self._write(f'@{index}\nD=A\n' + standard_pushd)
            return
        bases = {'local': 'LCL', 'argument': 'ARG',
                 'this': 'THIS', 'that': 'THAT'}
        if segment in bases:
            base = bases[segment]
            if command == CommandType.C_PUSH:
                # A = RAM[base] + index; D = RAM[A].
                self._write(f'@{base}\nD=M\n@{index}\nA=D+A\nD=M\n'
                            + standard_pushd)
            else:
                # Save destination address in R13 before popping.
                self._write(f'@{base}\nD=M\n@{index}\nD=D+A\n'
                            '@R13\nM=D\n@SP\nAM=M-1\nD=M\n'
                            '@R13\nA=M\nM=D\n')
            return
        if segment == 'temp':
            if not 0 <= index <= 7:
                raise ValueError('temp index must be 0..7')
            address = 5 + index
        elif segment == 'pointer':
            if index not in (0, 1):
                raise ValueError('pointer index must be 0 or 1')
            address = 3 + index  # RAM[3] = THIS; RAM[4] = THAT
        else:
            raise ValueError(f'Unknown VM segment: {segment}')
        if command == CommandType.C_PUSH:
            self._write(f'@{address}\nD=M\n' + standard_pushd)
        else:
            self._write(f'@SP\nAM=M-1\nD=M\n@{address}\nM=D\n')

    def staticPushPop(self, command, index):
        varname = f'{self.static_name}.{index}'
        if command == CommandType.C_PUSH:
            self._write(f'@{varname}\nD=M\n' + standard_pushd)
        else:
            self._write(f'@SP\nAM=M-1\nD=M\n@{varname}\nM=D\n')

    def extract_static_name(self, filename):
        return os.path.splitext(os.path.basename(filename))[0]

    def close(self):
        self._write('(END)\n@END\n0;JMP\n')

    def writeComment(self, comment):
        self._write(f'\n// {comment}\n')
