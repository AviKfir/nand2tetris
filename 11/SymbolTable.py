"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

STATIC = "STATIC"
FIELD = "FIELD"
ARGUMENT = "ARG"
VARIABLE = "VAR"
CLASS_KINDS = [STATIC, FIELD]
SUBROUTINE_KINDS = [ARGUMENT, VARIABLE]

COUNT_INDEX = 2
KIND_INDEX = 1
TYPE_INDEX = 0

NOT_FOUND = "NONE"


class SymbolTable:
    """A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """

    def __init__(self) -> None:
        """Creates a new empty symbol table."""

        self.class_table = {}
        self.subroutine_table = {}
        self.static_count = 0
        self.var_count = 0
        self.arg_count = 0
        self.field_count = 0
        self.counters = {STATIC: self.static_count, FIELD: self.field_count,
                         VARIABLE: self.var_count, ARGUMENT: self.arg_count}

    def start_subroutine(self) -> None:
        """Starts a new subroutine scope (i.e., resets the subroutine's 
        symbol table).
        """
        # Your code goes here!
        self.subroutine_table.clear()
        self.arg_count = 0
        self.var_count = 0

    def define(self, name: str, type: str, kind: str) -> None:
        """Defines a new identifier of a given name, type and kind and assigns 
        it a running index. "STATIC" and "FIELD" identifiers have a class scope, 
        while "ARG" and "VAR" identifiers have a subroutine scope.

        Args:
            name (str): the name of the new identifier.
            type (str): the type of the new identifier.
            kind (str): the kind of the new identifier, can be:
            "STATIC", "FIELD", "ARG", "VAR".
        """

        if kind in CLASS_KINDS:
            self.class_table[name] = [type, kind]
            if kind == CLASS_KINDS[0]:  # Static
                self.class_table[name].append(self.static_count)
                self.static_count += 1
            elif kind == CLASS_KINDS[1]:  # Field
                self.class_table[name].append(self.field_count)
                self.field_count += 1
        elif kind in SUBROUTINE_KINDS:
            self.subroutine_table[name] = [type, kind]
            if kind == SUBROUTINE_KINDS[0]:  # Argument
                self.subroutine_table[name].append(self.arg_count)
                self.arg_count += 1
            elif kind == SUBROUTINE_KINDS[1]:  # Variable
                self.subroutine_table[name].append(self.var_count)
                self.var_count += 1

    def var_count_return(self, kind: str) -> int:
        """
        Args:
            kind (str): can be "STATIC", "FIELD", "ARG", "VAR".

        Returns:
            int: the number of variables of the given kind already defined in 
            the current scope.
        """
        # Your code goes here!
        if kind == STATIC:
            return self.static_count
        elif kind == FIELD:
            return self.field_count
        elif kind == ARGUMENT:
            return self.arg_count
        elif kind == VARIABLE:
            return self.var_count

        return 0

    def kind_of(self, name: str) -> str:
        """
        Args:
            name (str): name of an identifier.

        Returns:
            str: the kind of the named identifier in the current scope, or None
            if the identifier is unknown in the current scope.
        """
        # Your code goes here!
        if name in self.class_table:
            return self.class_table[name][KIND_INDEX]
        elif name in self.subroutine_table:
            return self.subroutine_table[name][KIND_INDEX]
        else:
            return NOT_FOUND

    def type_of(self, name: str) -> str:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        if name in self.class_table:
            return self.class_table[name][TYPE_INDEX]
        elif name in self.subroutine_table:
            return self.subroutine_table[name][TYPE_INDEX]

    def index_of(self, name: str) -> int:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """

        if name in self.class_table:
            return self.class_table[name][COUNT_INDEX]
        elif name in self.subroutine_table:
            return self.subroutine_table[name][COUNT_INDEX]
