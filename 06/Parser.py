"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """Encapsulates access to the input code. Reads and assembly language 
    command, parses it, and provides convenient access to the commands 
    components (fields and symbols). In addition, removes all white space and 
    comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """

        input_lines = input_file.read().splitlines()

        self.list_of_commands = []
        for line in input_lines:
            line = line.replace(" ", "")
            if line == "":
                continue
            if line[0] == "/":
                continue
            else:
                for i in range(len(line)):
                    if line[i] == "/":
                        line = line[:i]
                        break
            self.list_of_commands.append(line)

        self.num_of_commands = len(self.list_of_commands)
        self.curr_command = 0

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        if (self.curr_command + 1) > self.num_of_commands:
            return False
        return True

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        self.curr_command += 1

    def replace(self, old: str, new: int) -> None:
        self.list_of_commands[self.curr_command] = \
            self.list_of_commands[self.curr_command].replace(old, str(new))

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        if self.list_of_commands[self.curr_command][0] == "@":
            return "A_COMMAND"
        elif self.list_of_commands[self.curr_command][0] == "(":
            return "L_COMMAND"
        return "C_COMMAND"

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        if self.command_type() == "A_COMMAND":
            return self.list_of_commands[self.curr_command][1:]
        return self.list_of_commands[self.curr_command][1:-1]

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        my_command = self.list_of_commands[self.curr_command]
        if "=" in my_command:
            index = my_command.find("=")
            return my_command[:index]
        return "null"

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # exp:   D=D+1;JLE (comp=D+1),   D=M (comp=M),   0;JMP (comp=0)

        my_command = self.list_of_commands[self.curr_command]
        if "=" in my_command and ";" in my_command:
            a = my_command.find("=")
            b = my_command.find(";")
            return my_command[a + 1:b]
        elif "=" in my_command:
            a = my_command.find("=")
            return my_command[a + 1:]
        else:  # only ";" in my_command
            b = my_command.find(";")
            return my_command[:b]

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        my_command = self.list_of_commands[self.curr_command]
        if ";" in my_command:
            index = my_command.find(";")
            return my_command[index+1:]
        return "null"
