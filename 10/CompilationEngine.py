"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

from JackTokenizer import JackTokenizer

TOKEN_MAP = {'KEYWORD': 'keyword', 'SYMBOL': 'symbol', 'IDENTIFIER': 'identifier'
    , 'INT_CONST': 'integerConstant', 'STRING_CONST': 'stringConstant'}

CLASS_LABEL = "class"

CLASS_VAR_DEC_LABEL = "classVarDec"
CLASS_VAR_DEC_START = ["static", "field"]

SUBROUTINE_DEC_START = ["constructor", "function", "method"]
SUBROUTINE_DEC_LABEL = "subroutineDec"

SUBROUTINE_BODY_LABEL = "subroutineBody"
VAR_DEC_LABEL = "varDec"
VAR_DEC_START = ["var"]
PARAM_LIST_LABEL = "parameterList"

STATEMENTS_LABEL = "statements"
STATEMENTS = ["let", "if", "while", "do", "return"]

OP_LIST = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
UNARY_OP_LIST = ["~", "-"]

KEYWORD_CONSTANTS = ["true", "false", "null", "this"]

LET_LABEL = "letStatement"
IF_LABEL = "ifStatement"
WHILE_LABEL = "whileStatement"
DO_LABEL = "doStatement"
RETURN_LABEL = "returnStatement"

EXPRESSION_LABEL = "expression"
EXPRESSION_LIST_LABEL = "expressionList"
TERM_LABEL = "term"

END_SENTENCE = ";"
ARRAY_INDICATOR = "["
STRING_VAL_OPEN = '"'
SUBROUTINE_INDICATORS = ["(", "."]

SYMBOL_SWAP = {'<': '&lt;', '>': '&gt;', '"': '&quot;', '&': '&amp;'}

OPEN = True
CLOSE = False


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: typing.TextIO, output_stream: typing.TextIO) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!

        self.tokenized = JackTokenizer(input_stream)

        self.tab = ""
        self.final_output = []
        self.output_stream = output_stream

    def increase_tab(self) -> None:
        self.tab += "  "

    def decrease_tab(self) -> None:
        self.tab = self.tab[:-2]

    def produce_label(self, label: str, state: bool) -> None:
        if state == OPEN:
            self.final_output.append(self.tab + "<" + label + ">\n")
            self.increase_tab()
        else:
            self.produce_close_label(label)

    def produce_close_label(self, label: str) -> None:
        length = len(self.final_output)
        if self.final_output[length - 1].strip()[0:3] == "<":  # if a declaration is empty
            self.final_output.pop()  # remove original open label
            self.decrease_tab()
            self.final_output.append(self.tab + "<" + label + "> " + "</" + label + ">\n")

        else:  # there is a "full" list or declaration
            self.decrease_tab()
            self.final_output.append(self.tab + "</" + label + ">\n")

    def token_check(self, token, label):
        token_out = token
        if label == TOKEN_MAP["STRING_CONST"]:
            if token[0] == STRING_VAL_OPEN:
                token_out = token_out[1:]
            if token[-1] == STRING_VAL_OPEN:
                token_out = token_out[:-1]

        elif label == TOKEN_MAP["SYMBOL"]:
            if token in SYMBOL_SWAP:
                token_out = SYMBOL_SWAP[token]

        return token_out

    def produce_tokenized_line(self, token, label) -> None:

        token = self.token_check(token, label)
        self.final_output.append(self.tab + "<" + label + "> " + token + " </" + label + ">\n")

    def initialize_class(self) -> None:
        self.produce_label(CLASS_LABEL, OPEN)
        i = 0
        while i < 3:
            self.tokenized.advance()
            self.produce_tokenized_line(self.tokenized.curr_token, TOKEN_MAP[self.tokenized.token_type()])
            i += 1

    """ checking if variable decelerations exist"""

    def check_for_class_var_dec(self) -> bool:
        if self.look_ahead() in CLASS_VAR_DEC_START:
            return True
        return False

    def check_for_subroutine(self) -> bool:
        if self.look_ahead() in SUBROUTINE_DEC_START:
            return True
        return False

    def pop_back_to_tokens(self):
        token = self.tokenized.curr_token
        self.tokenized.curr_word = list(token) + self.tokenized.curr_word  # popping token back in
        return token

    def look_ahead(self):
        if self.tokenized.has_more_tokens():
            self.tokenized.advance()
            token = self.pop_back_to_tokens()
            return token

        return ""

    def look_two_ahead(self):
        self.tokenized.advance()
        token_1 = self.tokenized.curr_token
        self.tokenized.advance()
        token_2 = self.tokenized.curr_token

        self.tokenized.curr_word = list(token_1) + list(token_2) + self.tokenized.curr_word  # popping tokens back in

        return token_2

    """Output a specified number of tokens to final output"""

    def output_x_tokens(self, num_x: int):

        counter = 0
        while counter < num_x:
            self.tokenized.advance()
            self.produce_tokenized_line(self.tokenized.curr_token, TOKEN_MAP[self.tokenized.token_type()])
            counter += 1

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # Your code goes here!
        self.initialize_class()

        while self.check_for_class_var_dec():
            self.compile_class_var_dec()

        while self.check_for_subroutine():
            self.compile_subroutine()

        self.output_x_tokens(1)  # '}'
        self.produce_label(CLASS_LABEL, CLOSE)
        for line in self.final_output:
            self.output_stream.write(line)
            print(line)

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""

        self.produce_label(CLASS_VAR_DEC_LABEL, OPEN)
        self.output_x_tokens(3)  # static/field + type + varName

        while self.look_ahead() != END_SENTENCE:
            self.output_x_tokens(2)  # ',' + varName

        self.output_x_tokens(1)  # ';'

        self.produce_label(CLASS_VAR_DEC_LABEL, CLOSE)

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function, or constructor."""
        # Your code goes here!
        self.produce_label(SUBROUTINE_DEC_LABEL, OPEN)

        self.output_x_tokens(4)  # 'constructor/function/method' + 'void/type' + name + '('
        self.compile_parameter_list()
        self.output_x_tokens(1)  # ')'
        self.compile_subroutine_body()

        self.produce_label(SUBROUTINE_DEC_LABEL, CLOSE)

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!

        self.produce_label(PARAM_LIST_LABEL, OPEN)
        if self.look_ahead() != ")":
            self.output_x_tokens(2)  # type + varName

        while self.look_ahead() != ")":
            self.output_x_tokens(3)  # ',' + type + varName

        self.produce_label(PARAM_LIST_LABEL, CLOSE)

    def check_for_var_dec(self) -> bool:
        if self.look_ahead() in VAR_DEC_LABEL:
            return True
        return False

    def compile_subroutine_body(self) -> None:
        """Compiles a subroutine body consisting of {varDec* statements}"""
        self.produce_label(SUBROUTINE_BODY_LABEL, OPEN)
        self.output_x_tokens(1)  # '{'
        while self.check_for_var_dec():
            self.compile_var_dec()

        self.compile_statements()

        self.output_x_tokens(1)  # '}'
        self.produce_label(SUBROUTINE_BODY_LABEL, CLOSE)

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.produce_label(VAR_DEC_LABEL, OPEN)
        self.output_x_tokens(3)  # 'var' + type + varName
        while self.look_ahead() != END_SENTENCE:
            self.output_x_tokens(2)  # ',' + varName

        self.output_x_tokens(1)  # ';'
        self.produce_label(VAR_DEC_LABEL, CLOSE)

    def check_for_statements(self) -> bool:

        if self.look_ahead() in STATEMENTS:
            return True
        return False

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """

        self.produce_label(STATEMENTS_LABEL, OPEN)

        while self.check_for_statements():
            if self.look_ahead() == "let":
                self.compile_let()
            elif self.look_ahead() == "if":
                self.compile_if()
            elif self.look_ahead() == "while":
                self.compile_while()
            elif self.look_ahead() == "do":
                self.compile_do()
            elif self.look_ahead() == "return":
                self.compile_return()

        self.produce_label(STATEMENTS_LABEL, CLOSE)

    def subroutine_call(self) -> None:
        self.output_x_tokens(1)  # [subroutineName | className | varName]
        if self.look_ahead() == ".":
            self.output_x_tokens(2)  # '.' + subroutineName

        self.output_x_tokens(1)  # '('
        self.compile_expression_list()
        self.output_x_tokens(1)  # ')'

    def compile_do(self) -> None:
        """Compiles a do statement."""

        self.produce_label(DO_LABEL, OPEN)
        self.output_x_tokens(1)  # 'do'
        self.subroutine_call()
        self.output_x_tokens(1)  # ';'
        self.produce_label(DO_LABEL, CLOSE)

    def check_for_array_index(self) -> bool:
        if self.look_ahead() == "[":
            return True
        return False

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.produce_label(LET_LABEL, OPEN)
        self.output_x_tokens(2)  # 'let' + varName
        if self.check_for_array_index():
            self.output_x_tokens(1)  # '['
            self.compile_expression()
            self.output_x_tokens(1)  # ']'

        self.output_x_tokens(1)  # '='
        self.compile_expression()
        self.output_x_tokens(1)  # ';'

        self.produce_label(LET_LABEL, CLOSE)

    def compile_while(self) -> None:
        """Compiles a while statement."""

        self.produce_label(WHILE_LABEL, OPEN)

        self.output_x_tokens(2)  # 'while' + '('
        self.compile_expression()
        self.output_x_tokens(2)  # ')' + '{'
        self.compile_statements()
        self.output_x_tokens(1)  # '}'

        self.produce_label(WHILE_LABEL, CLOSE)

    def check_for_return_expression(self) -> bool:
        if self.look_ahead() != END_SENTENCE:
            return True
        return False

    def compile_return(self) -> None:
        """Compiles a return statement."""

        self.produce_label(RETURN_LABEL, OPEN)

        self.output_x_tokens(1)  # 'return'

        if self.check_for_return_expression():
            self.compile_expression()

        self.output_x_tokens(1)  # ';'

        self.produce_label(RETURN_LABEL, CLOSE)

    def check_for_else(self) -> bool:
        if self.look_ahead() == "else":
            return True
        return False

    def compile_else(self) -> None:

        self.output_x_tokens(2)  # 'else' + '#'
        self.compile_statements()
        self.output_x_tokens(1)  # '}'

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""

        self.produce_label(IF_LABEL, OPEN)
        self.output_x_tokens(2)  # 'if' + '('
        self.compile_expression()
        self.output_x_tokens(2)  # ')' + '{'
        self.compile_statements()
        self.output_x_tokens(1)  # '}'

        if self.check_for_else():
            self.compile_else()

        self.produce_label(IF_LABEL, CLOSE)

    def check_for_op(self) -> bool:
        if self.look_ahead() in OP_LIST:
            return True
        return False

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        self.produce_label(EXPRESSION_LABEL, OPEN)
        self.compile_term()
        while self.check_for_op():
            self.output_x_tokens(1)  # 'op'
            self.compile_term()

        self.produce_label(EXPRESSION_LABEL, CLOSE)

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        # Your code goes here!

        self.produce_label(TERM_LABEL, OPEN)
        if self.look_ahead() == "(":  # if starts with open bracket, must be '(expression)'
            self.output_x_tokens(1)  # '('
            self.compile_expression()
            self.output_x_tokens(1)  # ')'
        elif self.look_ahead() in UNARY_OP_LIST:  # (unaryOp term)
            self.output_x_tokens(1)  # 'unaryOp'
            self.compile_term()

        elif self.look_two_ahead() in ARRAY_INDICATOR:
            self.output_x_tokens(2)  # varName + '['
            self.compile_expression()
            self.output_x_tokens(1)  # ']'
        elif self.look_two_ahead() in SUBROUTINE_INDICATORS:
            self.subroutine_call()
        else:
            self.output_x_tokens(1)  # lone identifier

        self.produce_label(TERM_LABEL, CLOSE)

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        self.produce_label(EXPRESSION_LIST_LABEL, OPEN)

        if self.look_ahead() != ")":
            self.compile_expression()
            while self.look_ahead() != ")":
                self.output_x_tokens(1)  # ','
                self.compile_expression()

        self.produce_label(EXPRESSION_LIST_LABEL, CLOSE)
