"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    
    my_parser = Parser(input_file)
    my_code = Code()
    my_symbol_table = SymbolTable()  # initialization of all predefined symbols inside my_symbol_table

    # First Pass - adding label symbols
    curr_address = 0
    while my_parser.has_more_commands():
        if my_parser.command_type() == "L_COMMAND":
            curr_symbol = my_parser.symbol()
            my_symbol_table.add_entry(curr_symbol, curr_address)
        else:
            curr_address += 1
        my_parser.advance()

    # Second Pass - Parsing and translating
    my_parser.curr_command = 0  # because of previous loop we initialize it
    while my_parser.has_more_commands():
        # we skip L_COMMAND and do not include them inside the output file (.hack)
        if my_parser.command_type() == "A_COMMAND":
            # replacing an A instruction with its numeric meaning (exp: @LOOP -> @14)
            curr_symbol = my_parser.symbol()
            if not curr_symbol.isnumeric() and not my_symbol_table.contains(curr_symbol):
                my_symbol_table.add_entry(curr_symbol, my_symbol_table.free_address)
                my_symbol_table.free_address += 1
            if not curr_symbol.isnumeric():
                address = my_symbol_table.get_address(curr_symbol)
                my_parser.replace(curr_symbol, address)
                curr_symbol = address
            binary_address = my_code.translate_num_to_binary(int(curr_symbol))
            binary_address += "\n"
            output_file.write(binary_address)
        elif my_parser.command_type() == "C_COMMAND":
            # translation of a C instruction
            temp_str = "111"
            temp_str += my_code.comp(my_parser.comp())
            temp_str += my_code.dest(my_parser.dest())
            temp_str += my_code.jump(my_parser.jump())
            temp_str += "\n"
            output_file.write(temp_str)
        my_parser.advance()


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
