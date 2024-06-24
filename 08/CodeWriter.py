"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import typing

SP_INIT = '256'


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    _call_counter = 1
    _jump_counter = 1
    sys_init_written = False

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        self.output_stream = output_stream
        self.file_name = ""
        self.output = ""
        self.call_lst = []
        # self.file_name = str(os.path.basename(output_stream.name).partition(".")[0])

    def set_file_name(self, filename: str) -> None:
        """
        This function is used in Main.py
        Args:
            filename (str): The name of the VM file.
        """
        self.file_name = filename

    def write_arithmetic(self, command: str) -> None:
        """Writes the assembly code that is the translation of the given 
        arithmetic command.

        Args:
            command (str): an arithmetic command.

        first group: add, sub, add, or.
        second group: eq, gt, lt.
        third group: neg, not.
        """
        if command == 'add':
            self.first_group(command)
        elif command == 'sub':
            self.first_group(command)
        elif command == 'neg':
            self.third_group(command)
        elif command == 'eq':
            self.second_group(command)
        elif command == 'gt':
            self.second_group(command)
        elif command == 'lt':
            self.second_group(command)
        elif command == 'and':
            self.first_group(command)
        elif command == 'or':
            self.first_group(command)
        elif command == 'not':
            self.third_group(command)

    def first_group(self, command: str) -> None:
        self.output += '\n// {}\n'.format(command)
        if command == 'add':
            command = 'M + D'
        elif command == 'sub':
            command = 'M - D'
        elif command == 'and':
            command = 'D & M'
        elif command == 'or':
            command = 'D | M'
        self.store_x_address()
        self.output += '// performing addition\n'
        self.output += '@R13\n' \
                       'A = M\n' \
                       'D = M\n' \
                       'A = A - 1\n' \
                       'M = {}\n'.format(command)
        self.clean()

    def second_group(self, command: str) -> None:
        """ true = -1  ,  false = 0 """
        self.output += '\n// {}\n'.format(command)
        if command == 'eq':
            command = 'D;JEQ'
        elif command == 'gt':
            command = 'D;JGT'
        elif command == 'lt':
            command = 'D;JLT'
        self.check_overflow()
        self.first_group('sub')   # we use sub because if x = y than after subtraction we'll get x = 0.
        # if x < 0 than x < y (and opposite...)
        self.write_to_asm()
        self.output_stream.write("// performing equality\n@SP\nA = M - 1\nD = M\n"
                                 "@TRUE{0}\n// if D = 0 than it means that x = y\n{1}\n"
                                 "// else (false)\n@SP\nA = M - 1\nM = 0\n@END{0}\n0;JMP\n"
                                 "(TRUE{0})\n@SP\nA = M - 1\nM = -1\n(END{0})\n".format(str(CodeWriter._jump_counter),
                                                                                        command))
        CodeWriter._jump_counter += 1

    def third_group(self, command: str) -> None:
        self.output += '\n// {}\n'.format(command)
        if command == 'neg':
            command = '-M'
        elif command == 'not':
            command = '!M'
        self.output += '@SP\n' \
                       'A = M - 1\n' \
                       'M = {}\n'.format(command)

    def check_overflow(self) -> None:
        """
        # if x > 0 and y < 0 (or opposite): we can get an overflow during 'sub',
        # the result number can be outside of our memory limit.
        """
        self.write_to_asm()  # to write in our asm file what is already stored in self.output
        self.output_stream.write("@SP\nA = M - 1\nA = A - 1\nD = M\n"
                                 "// if x > 0, need to check if y < 0\n@CHECK_NEG{0}\nD;JGT\n"
                                 "// else: x <= 0, so need to check if y > 0\n"
                                 "@SP\nA = M - 1\nD = M\n@OVERFLOW1.{0}\n"
                                 "// if y > 0, overflow risk confirmed\n"
                                 "D;JGT\n@CONTINUE{0}\n0;JMP\n(CHECK_NEG{0})\n@SP\n"
                                 "A = M - 1\nD = M\n@OVERFLOW2.{0}\n"
                                 "// if y < 0, overflow risk confirmed\n"
                                 "D;JLT\n@CONTINUE{0}\n0;JMP\n(OVERFLOW1.{0})\n"
                                 "// x < 0 and y > 0\n@SP\nA = M - 1\nA = A - 1\n"
                                 "M = 0\n@SP\nA = M - 1\nM = 1\n@CONTINUE{0}\n0;JMP\n(OVERFLOW2.{0})\n"
                                 "// x > 0 and y < 0\n@SP\nA = M - 1\nA = A - 1\nM = 1\n@SP\n"
                                 "A = M - 1\nM = 0\n(CONTINUE{0})\n".format(str(CodeWriter._jump_counter)))

    def store_x_address(self) -> None:
        self.output += '// storing x in R13, updates SP\n'
        self.output += "@SP\n" \
                       "D = M - 1\n" \
                       "@R13\n" \
                       "M = D\n" \
                       "@SP\n" \
                       "M = M - 1\n"

    def clean(self) -> None:
        self.output += '// (optional, only for cleanness) deleting SP\'s trash value (y)\n' \
                       'A = A + 1\n' \
                       'M = 0\n'

    def shorten_seg_name(self, segment: str) -> str:
        """
        returns the seg name (LCL, ARG, THIS, THAT) as saved in the assembler's SymbolTable.
        temp: address starts at RAM[5].
        """
        if segment == 'local':
            segment = 'LCL'
        elif segment == 'argument':
            segment = 'ARG'
        elif segment == 'this':
            segment = 'THIS'
        elif segment == 'that':
            segment = 'THAT'
        elif segment == 'temp':
            segment = '5'
        return segment

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """
        Writes the assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        if command == 'C_PUSH':
            self.push_strategy(segment, index)
        elif command == 'C_POP':
            self.pop_strategy(segment, index)

    def push_strategy(self, segment: str, index: int) -> None:
        self.output += '\n// push\n'

        if segment == 'pointer':
            self.push_const_to_D('3')
            self.add_const_to_D(str(index))  # index should be 0 or 1 (THIS or THAT)
            self.output += 'A = D\n' \
                           'D = M\n'

        elif segment == 'static':
            self.output += '@{}.{}\n'.format(self.file_name, str(index))
            self.output += 'D = M\n'

        elif segment == 'constant':
            self.push_const_to_D(str(index))

        else:
            register = 'M'
            if segment == 'temp':
                register = 'A'  # we deal with 'temp' differently
            segment = self.shorten_seg_name(segment)
            self.output += '@{}\n'.format(segment)
            self.output += 'D = {}\n'.format(register)
            self.output += '@{}\n'.format(str(index))
            self.output += 'A = D + A\n' \
                           'D = M\n'

        self.push_D_in_stack()

    def pop_strategy(self, segment: str, index: int) -> None:
        """
        There's no constant segment in pop.
        we first save the address (where we'll put the topmost value in it) in D, then in R13.
        """
        self.output += '\n// pop\n'

        if segment == 'pointer':
            self.output += '@3\n' \
                           'D = A\n'
            # index = 0/1 (THIS or THAT). It's still possible for the index to be a different integer
            # (not only 0/1), because it is a weakly typed language (a.k.a that's the law boys).
            self.output += '@{}\n'.format(str(index))
            self.output += 'D = D + A\n'
            self.load_D_to_seg('R13')
            self.pop_from_stack_to_D()
            self.load_D_to_address_in_seg('R13')

        elif segment == 'static':
            self.pop_from_stack_to_D()
            self.load_D_to_seg('{}.{}'.format(self.file_name, str(index)))

        else:
            register = 'M'
            if segment == 'temp':
                register = 'A'  # we deal with 'temp' differently
            segment = self.shorten_seg_name(segment)
            self.output += '@{}\n'.format(segment)
            self.output += 'D = {}\n'.format(register)
            self.output += '@{}\n'.format(str(index))
            self.output += 'D = D + A\n'
            self.load_D_to_seg('R13')
            self.pop_from_stack_to_D()
            self.load_D_to_address_in_seg('R13')

    def load_from_seg_to_D(self, segment: str) -> None:
        self.output += '@{}\n'.format(segment)
        self.output += 'D = M\n'

    def load_D_to_seg(self, segment: str) -> None:
        self.output += '@{}\n'.format(segment)
        self.output += 'M = D\n'

    def push_const_to_D(self, constant: str) -> None:
        self.output += '@{}\n'.format(constant)
        self.output += 'D = A\n'

    def add_const_to_D(self, constant: str) -> None:
        self.output += '@{}\n'.format(constant)
        self.output += 'D = D + A\n'

    def load_D_to_address_in_seg(self, segment: str) -> None:
        self.output += '@{}\n'.format(segment)
        self.output += 'A = M\n' \
                       'M = D\n'

    def push_D_in_stack(self) -> None:
        self.output += '@SP\n' \
                       'A = M\n' \
                       'M = D\n' \
                       '@SP\n' \
                       'M = M + 1\n'

    def pop_from_stack_to_D(self) -> None:
        self.output += '@SP\n' \
                       'AM = M - 1\n' \
                       'D = M\n' \
                       '// (optional, only for cleanness) deleting SP\'s trash value (y)\n' \
                       'M = 0\n'

    def restore(self, constant: str) -> None:
        self.push_const_to_D(constant)
        self.output += '@R13\n' \
                       'A = M - D\n' \
                       'D = M\n'

    def write_label(self, label: str) -> None:
        self.output += '// Writing label\n' \
                       '({})\n'.format(label)

    def write_goto(self, label: str) -> None:
        self.output += '\n// Writing goto\n' \
                       '@{}\n'.format(label)
        self.output += '0; JMP\n'

    def write_if_goto(self, label: str) -> None:
        self.output += '\n//Writing if-goto\n' \
                       '@SP\n' \
                       'AM = M - 1\n' \
                       'D = M\n' \
                       '@{}\n'.format(label)
        self.output += 'D; JNE\n'

    def call_command(self, func_name: str, n_args: int) -> None:
        self.output += '\n// call command\n'
        return_label = 'RETURN_{}.{}'.format(func_name, CodeWriter._call_counter)
        CodeWriter._call_counter += 1
        self.call_lst.append(return_label)
        # push return-address
        self.output += '@{}\n'.format(return_label)
        self.output += 'D = A\n'
        self.push_D_in_stack()
        self.load_from_seg_to_D('LCL')
        self.push_D_in_stack()
        self.load_from_seg_to_D('ARG')
        self.push_D_in_stack()
        self.load_from_seg_to_D('THIS')
        self.push_D_in_stack()
        self.load_from_seg_to_D('THAT')
        self.push_D_in_stack()
        # ARG = SP - (n_args + 5)
        self.load_from_seg_to_D('SP')
        self.output += '@{}\n'.format(n_args)
        self.output += 'D = D - A\n' \
                       '@5\n' \
                       'D = D - A\n'
        self.load_D_to_seg('ARG')
        # LCL = SP
        self.output += '@SP\n' \
                       'D = M\n' \
                       '@LCL\n' \
                       'M = D\n'
        # goto function name (transfer control)
        self.write_goto(func_name)
        # dealing in case we have same labels for different calls (calling same function more than once).
        # The self.call_lst is for recursion cases. We take the last label from
        # self.call_lst to return in opposite order.
        curr_label = self.call_lst[-1]
        del self.call_lst[-1]
        self.write_label(curr_label)

    def function_command(self, func_name: str, k: int) -> None:
        self.output += '\n// function command\n'
        self.write_label(func_name)
        for i in range(k):
            self.output += 'D = 0\n'
            self.push_D_in_stack()

    def return_command(self) -> None:
        """
        endFrame = LCL (more exactly the value LCL holds)  -> saved in R13
        return_address = *(endFrame - 5)  -> saved in R14
        """
        self.output += '\n// return command\n'
        self.load_from_seg_to_D('LCL')  # Now D holds the value LCL holds. Next we'll save D in R13
        self.load_D_to_seg('R13')
        self.output += '@5\n' \
                       'A = D - A\n' \
                       'D = M\n'  # Now D holds the return address. Next we'll save D in R14
        self.load_D_to_seg('R14')
        self.pop_from_stack_to_D()  # *ARG = pop()
        self.load_D_to_address_in_seg('ARG')
        self.output += 'D = A + 1\n'  # SP = ARG + 1
        self.load_D_to_seg('SP')
        # THAT = *(endFrame - 1)
        self.restore('1')
        self.load_D_to_seg('THAT')
        # THIS = *(endFrame - 2)
        self.restore('2')
        self.load_D_to_seg('THIS')
        # ARG = *(endFrame - 3)
        self.restore('3')
        self.load_D_to_seg('ARG')
        # LCL = *(endFrame - 4)
        self.restore('4')
        self.load_D_to_seg('LCL')
        # goto return_address
        self.output += '@R14\n' \
                       'A = M\n' \
                       '0;JMP\n'

    def write_init(self) -> None:
        self.output += '\n// write_init function\n'
        self.push_const_to_D(SP_INIT)
        self.load_D_to_seg('SP')
        self.call_command('Sys.init', 0)

    def write_to_asm(self):
        self.output_stream.write(self.output)
        self.output = ""
