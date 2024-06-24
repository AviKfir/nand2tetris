"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from Parser import Parser
from CodeWriter import CodeWriter


def translate_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Translates a single file.

    Args:
        input_file (typing.TextIO): the file to translate.
        output_file (typing.TextIO): writes all output to this file.
    """

    my_parser = Parser(input_file)
    my_CodeWriter = CodeWriter(output_file)
    input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
    my_CodeWriter.set_file_name(input_filename)

    if not CodeWriter.sys_init_written:  # the bootstrap code will be added only during first file translation.
        my_CodeWriter.write_init()  # Initializes SP, calls Sys.init (bootstrap code)
        CodeWriter.sys_init_written = True

    while my_parser.has_more_commands():
        command_type = my_parser.command_type()
        if command_type == "C_ARITHMETIC":
            my_CodeWriter.write_arithmetic(my_parser.arg1())
        elif command_type in "C_PUSH C_POP":
            my_CodeWriter.write_push_pop(command_type, my_parser.arg1(), my_parser.arg2())
        elif command_type == "C_LABEL":
            my_CodeWriter.write_label(my_parser.arg1())
        elif command_type == "C_GOTO":
            my_CodeWriter.write_goto(my_parser.arg1())
        elif command_type == "C_IF":
            my_CodeWriter.write_if_goto(my_parser.arg1())
        elif command_type == "C_FUNCTION":
            my_CodeWriter.function_command(my_parser.arg1(), my_parser.arg2())
        elif command_type == "C_RETURN":
            my_CodeWriter.return_command()
        elif command_type == "C_CALL":
            my_CodeWriter.call_command(my_parser.arg1(), my_parser.arg2())

        my_parser.advance()

    my_CodeWriter.write_to_asm()


if "__main__" == __name__:
    # Parses the input path and calls translate_file on each input file
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: VMtranslator <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_translate = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
        output_path = os.path.join(argument_path, os.path.basename(
            argument_path))
    else:
        files_to_translate = [argument_path]
        output_path, extension = os.path.splitext(argument_path)
    output_path += ".asm"
    with open(output_path, 'w') as output_file:
        for input_path in files_to_translate:
            filename, extension = os.path.splitext(input_path)
            if extension.lower() != ".vm":
                continue
            with open(input_path, 'r') as input_file:
                translate_file(input_file, output_file)
