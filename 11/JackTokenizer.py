"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

KEYWORDS = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int',
            'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let',
            'do', 'if', 'else', 'while', 'return']

SYMBOLS = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<',
           '>', '=', '~']

TOKEN_TYPES = ['KEYWORD', 'SYMBOL', 'IDENTIFIER', 'INT_CONST', 'STRING_CONST']

TOKEN_MAP = ['keyword', 'symbol', 'identifier', 'integerConstant', 'stringConstant']

SYMBOL_SWAP = {'<': '&lt;', '>': '&gt;', '"': '&quot;', '&': '&amp;'}

STRING_VAL_OPEN = '"'

INT_RANGE = range(0, 32767, 1)


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    """

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        # Your code goes here!
        # A good place to start is:
        # input_lines = input_stream.read().splitlines()

        input_lines = input_stream.read().splitlines()

        self.keywords_ = KEYWORDS
        self.symbols_ = SYMBOLS
        self.tokens_ = []
        self.print_output_ = ""
        self.output_ = []
        self.curr_word = []
        self.curr_token = ""
        self.total_tokens = 0
        for line in input_lines:
            line = line.strip()  # removing whitespaces from the left and right of the string
            line = line.replace("\n\r", "")
            line = line.replace("\t", "")
            if line == "":
                continue
            if line[0] == "/" or line[0] == '*':
                continue

            line = line.split("//")[0]  # taking only first part of line (before // comments)

            for token in line.split():
                self.tokens_.append(token)

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        if not self.tokens_ and not self.curr_word:
            return False
        return True

    def get_string_const(self) -> None:

        flag = 0
        while flag == 0:
            if not self.curr_word:
                self.curr_token += " "
                word = self.tokens_.pop(0)
                self.curr_word = list(word)  # placing all characters in array

            if self.curr_word[0] == '"':
                flag = 1

            self.curr_token += self.curr_word.pop(0)

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token. 
        This method should be called if has_more_tokens() is true. 
        Initially there is no current token.
        """
        # Your code goes here!
        self.curr_token = ""
        if not self.curr_word:
            word = self.tokens_.pop(0)
            self.curr_word = list(word)  # placing all characters in array

        while self.curr_word:  # while curr_word still has characters
            ch = self.curr_word[0]
            if ch not in self.symbols_ and ch != '"':  # if not a symbol, then part of a keyword, string constant, identifier, etc
                self.curr_word.pop(0)
                self.curr_token += ch
            elif ch != '"':
                if self.curr_token == "":  # if symbol comes after letters already added to curr_token, it is not added
                    self.curr_token = self.curr_word.pop(0)
                break
            else:
                self.curr_word.pop(0)
                self.curr_token += ch
                self.get_string_const()
                break

        self.output_.append(self.curr_token)

    """Checking if current token is INT_CONST"""

    def is_int_const(self) -> bool:
        try:
            int(self.curr_token)

        except ValueError:
            return False

        if int(self.curr_token) not in INT_RANGE:
            return False

        return True

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        # Your code goes here!
        if self.curr_token in self.keywords_:
            return "KEYWORD"
        elif self.curr_token in self.symbols_:
            return "SYMBOL"
        elif self.curr_token[0] == STRING_VAL_OPEN:
            return "STRING_CONST"
        elif self.is_int_const():
            return "INT_CONST"

        return "IDENTIFIER"

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", 
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO", 
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        # Your code goes here!
        return self.curr_token

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
        """
        # Your code goes here!
        output = self.curr_token
        if self.curr_token in SYMBOL_SWAP:
            output = SYMBOL_SWAP[self.curr_token]
        return output

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
        """
        # Your code goes here!
        return self.curr_token

    def int_val(self) -> int:
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
        """
        # Your code goes here!
        return int(self.curr_token)

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double 
            quotes. Should be called only when token_type() is "STRING_CONST".
        """
        # Your code goes here!

        return self.curr_token[1:-1]
