"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

CONSTANT = "CONST"
ARGUMENT = "ARG"
LOCAL = "LOCAL"
STATIC = "STATIC"
THIS = "THIS"
THAT = "THAT"
POINTER = "POINTER"
TEMP = "TEMP"

SEGMENTS = {CONSTANT: 'constant', ARGUMENT: 'argument', LOCAL: 'local', STATIC: 'static'
    , THIS: 'this', THAT: 'that', POINTER: 'pointer', TEMP: 'temp'}

ADD = "ADD"
SUBTRACT = "SUB"
NEGATE = "NEG"
EQUAL = "EQ"
GREATER_THAN = "GT"
LESS_THAN = "LT"
AND = "AND"
OR = "OR"
NOT = "NOT"

ARITHMETIC_COMMANDS = {ADD: 'add', SUBTRACT: 'sub', NEGATE: 'neg', EQUAL: 'eq', GREATER_THAN: 'gt'
    , LESS_THAN: 'lt', AND: 'and', OR: 'or', NOT: 'not'}

WRITE_PUSH = "push"
WRITE_POP = "pop"
WRITE_LABEL = "label"
GOTO_LABEL = "goto"
IF_GOTO_LABEL = "if-goto"
WRITE_CALL = "call"
WRITE_FUNCTION = "function"
WRITE_RETURN = "return"


class VMWriter:
    """
    Writes VM commands into a file. Encapsulates the VM command syntax.
    """

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Creates a new file and prepares it for writing VM commands."""
        # Your code goes here!
        self.output_stream = output_stream

        self.final_output = []

    def write_line(self, command, args=None):
        line = str(command)
        if args:
            for arg in args:
                line += " " + arg

        line += "\n"
        self.final_output.append(line)
        self.output_stream.write(line)

    def write_push(self, segment: str, index: int) -> None:
        """Writes a VM push command.

        Args:
            segment (str): the segment to push to, can be "CONST", "ARG", 
            "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP"
            index (int): the index to push to.
        """
        # Your code goes here!
        self.write_line(WRITE_PUSH, [SEGMENTS[segment], str(index)])

    def write_pop(self, segment: str, index: int) -> None:
        """Writes a VM pop command.

        Args:
            segment (str): the segment to pop from, can be "CONST", "ARG", 
            "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP".
            index (int): the index to pop from.
        """
        # Your code goes here!

        self.write_line(WRITE_POP, [SEGMENTS[segment], str(index)])

    def write_arithmetic(self, command: str) -> None:
        """Writes a VM arithmetic command.

        Args:
            command (str): the command to write, can be "ADD", "SUB", "NEG", 
            "EQ", "GT", "LT", "AND", "OR", "NOT".
        """

        self.write_line(ARITHMETIC_COMMANDS[command])

    def write_label(self, label: str) -> None:
        """Writes a VM label command.

        Args:
            label (str): the label to write.
        """
        # Your code goes here!
        self.write_line(WRITE_LABEL, [label])

    def write_goto(self, label: str) -> None:
        """Writes a VM goto command.

        Args:
            label (str): the label to go to.
        """
        # Your code goes here!
        self.write_line(GOTO_LABEL, [label])

    def write_if(self, label: str) -> None:
        """Writes a VM if-goto command.

        Args:
            label (str): the label to go to.
        """

        self.write_line(IF_GOTO_LABEL, [label])

    def write_call(self, name: str, n_args: int) -> None:
        """Writes a VM call command.

        Args:
            name (str): the name of the function to call.
            n_args (int): the number of arguments the function receives.
        """
        # Your code goes here!
        self.write_line(WRITE_CALL, [name, str(n_args)])

    def write_function(self, name: str, n_locals: int) -> None:
        """Writes a VM function command.

        Args:
            name (str): the name of the function.
            n_locals (int): the number of local variables the function uses.
        """
        # Your code goes here!
        self.write_line(WRITE_FUNCTION, [name, str(n_locals)])

    def write_return(self) -> None:
        """Writes a VM return command."""
        # Your code goes here!
        self.write_line(WRITE_RETURN)

    def close(self) -> None:
        """Closes the output file."""
        # Your code goes here!
        self.output_stream.close()
