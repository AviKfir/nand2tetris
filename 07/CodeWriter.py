"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import os


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        self.output_stream = output_stream
        self.output = ""
        self.counter = 1
        self.file_name = str(os.path.basename(output_stream.name).partition(".")[0])

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

        self.output_stream.write(self.output)
        self.output = ""

    def first_group(self, command: str) -> None:
        """ first group: add, sub, add, or. """
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
        """
        second group: eq, gt, lt.
        true = -1
        false = 0
        """
        self.output += '\n// {}\n'.format(command)
        if command == 'eq':
            command = 'D;JEQ'
        elif command == 'gt':
            command = 'D;JGT'
        elif command == 'lt':
            command = 'D;JLT'
        # if x > 0 and y < 0 (or opposite): we can get an overflow during 'sub',
        # the result number can be outside of our memory limit.
        self.check_overflow()
        self.first_group('sub')
        # we use sub because if x = y than after subtraction we'll get x = 0.
        # if x < 0 than x < y (and opposite...)
        self.output += '// performing equality\n'
        self.output += '@SP\n' \
                       'A = M - 1\n' \
                       'D = M\n' \
                       '@TRUE{}\n'.format(str(self.counter))
        self.output += '// if D = 0 than it means that x = y\n' \
                       '{}\n'.format(command)
        self.output += '// else (false)\n' \
                       '@SP\n' \
                       'A = M - 1\n' \
                       'M = 0\n' \
                       '@END{}\n'.format(str(self.counter))
        self.output += '0;JMP\n' \
                       '(TRUE{})\n'.format(str(self.counter))
        self.output += '@SP\n' \
                       'A = M - 1\n' \
                       'M = -1\n'
        self.output += '(END{})\n'.format(str(self.counter))
        self.counter += 1

    def third_group(self, command: str) -> None:
        """ third group: neg, not."""
        self.output += '\n// {}\n'.format(command)
        if command == 'neg':
            command = '-M'
        elif command == 'not':
            command = '!M'
        self.output += '@SP\n' \
                       'A = M - 1\n' \
                       'M = {}\n'.format(command)

    def check_overflow(self):
        self.output += '@SP\n' \
                       'A = M - 1\n' \
                       'A = A - 1\n' \
                       'D = M\n' \
                       '// if x > 0, need to check if y < 0\n' \
                       '@CHECK_NEG{}\n'.format(str(self.counter))
        self.output += 'D;JGT\n' \
                       '// else: x <= 0, so need to check if y > 0\n' \
                       '@SP\n' \
                       'A = M - 1\n' \
                       'D = M\n' \
                       '@OVERFLOW1.{}\n'.format(str(self.counter))
        self.output += '// if y > 0, overflow risk confirmed\n' \
                       'D;JGT\n' \
                       '@CONTINUE{}\n'.format(str(self.counter))
        self.output += '0;JMP\n' \
                       '(CHECK_NEG{})\n'.format(str(self.counter))
        self.output += '@SP\n' \
                       'A = M - 1\n' \
                       'D = M\n' \
                       '@OVERFLOW2.{}\n'.format(str(self.counter))
        self.output += '// if y < 0, overflow risk confirmed\n' \
                       'D;JLT\n' \
                       '@CONTINUE{}\n'.format(str(self.counter))
        self.output += '0;JMP\n' \
                       '(OVERFLOW1.{})\n'.format(str(self.counter))
        self.output += '// x < 0 and y > 0\n' \
                       '@SP\n' \
                       'A = M - 1\n' \
                       'A = A - 1\n' \
                       'M = 0\n' \
                       '@SP\n' \
                       'A = M - 1\n' \
                       'M = 1\n' \
                       '@CONTINUE{}\n'.format(str(self.counter))
        self.output += '0;JMP\n' \
                       '(OVERFLOW2.{})\n'.format(str(self.counter))
        self.output += '// x > 0 and y < 0\n' \
                       '@SP\n' \
                       'A = M - 1\n' \
                       'A = A - 1\n' \
                       'M = 1\n' \
                       '@SP\n' \
                       'A = M - 1\n' \
                       'M = 0\n' \
                       '(CONTINUE{})\n'.format(str(self.counter))

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

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes the assembly code that is the translation of the given
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
        self.output_stream.write(self.output)
        self.output = ""

    def push_strategy(self, segment: str, index: int) -> None:
        self.output += '\n// push\n'
        if segment == 'pointer':
            self.output += '@3\n' \
                           'D = A\n'
            self.output += '@{}\n'.format(str(index))  # index = 0 or 1 (THIS or THAT)
            self.output += 'D = D + A\n' \
                           'A = D\n' \
                           'D = M\n'
        elif segment == 'static':
            self.output += '@{}.{}\n'.format(self.file_name, str(index))
            self.output += 'D = M\n'
        elif segment != 'constant':
            self.address_in_D(segment, index)
            # now the corresponding address of the element is saved in D.
            self.output += 'A = D\n' \
                           'D = M\n'
        else:  # segment = 'constant'
            self.output += '@{}\n'.format(str(index))
            self.output += 'D = A\n'

        # D is the element to push in stack
        self.push_in_stack()

    def pop_strategy(self, segment: str, index: int) -> None:
        """ There's no constant segment in pop
        we first save the address (where we'll put the topmost value in it) in D, then in R13.
        """
        self.output += '\n// pop\n'

        if segment == 'pointer':
            self.output += '@3\n' \
                           'D = A\n'
            self.output += '@{}\n'.format(str(index))  # index = 0 or 1 (THIS or THAT)
            self.output += 'D = D + A\n'

        elif segment == 'static':
            self.output += '@{}.{}\n'.format(self.file_name, str(index))
            self.output += 'D = A\n'

        else:  # address where we will insert the popped element.
            self.address_in_D(segment, index)

        # saving the address in R13 because we will use D and therefor loose its value.
        self.output += '@13\n' \
                       'M = D\n'

        # Saving the popped element in D.
        self.pop_from_stack()
        self.output += '@13\n' \
                       'A = M\n' \
                       'M = D\n'

    def push_in_stack(self) -> None:
        self.output += '// push in stack (D = element to push)\n' \
                       '@SP\n' \
                       'A = M\n' \
                       'M = D\n' \
                       '@SP\n' \
                       'M = M + 1\n'

    def pop_from_stack(self) -> None:
        """ Saving the popped element in D. """
        self.output += '// pop from stack (saving in D) \n' \
                       '@SP\n' \
                       'AM = M - 1\n' \
                       'D = M\n' \
                       '// (optional, only for cleanness) deleting SP\'s trash value (y)\n' \
                       'M = 0\n'

    def address_in_D(self, segment: str, index: int) -> None:
        """
        Saving the address of element in D.
        ----------------------------------
        LCL, ARG, THIS, THAT: are already in the symbol table.
        --
        static:
        starts at RAM[16]
        we do not deal with static in this function.
        --
        constant: (only with push)
        We deal with the case differently. D holds the constant number.
        (we won't save the elem in address D. Because here D is already the elem we searched for.)
        --
        pointer:
        address starts at RAM[3]. (index = 0/1. Thus, pointer + i = THIS / THAT.)
        --
        temp:
        address starts at RAM[5].
        """
        deal_temp_segment = 'M'
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
            deal_temp_segment = 'A'
        self.output += '@{}\n'.format(segment)
        self.output += 'D = {}\n'.format(deal_temp_segment)
        self.output += '@{}\n'.format(str(index))
        self.output += 'D = D + A\n'
