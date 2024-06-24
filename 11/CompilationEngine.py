"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter

STATIC = "STATIC"
FIELD = "FIELD"
ARGUMENT = "ARG"
VARIABLE = "VAR"

THIS = "this"
THAT = "that"

CLASS_KINDS = [STATIC, FIELD]
SUBROUTINE_KINDS = [ARGUMENT, VARIABLE]

TOKEN_MAP = {'KEYWORD': 'keyword', 'SYMBOL': 'symbol', 'IDENTIFIER': 'identifier'
    , 'INT_CONST': 'integerConstant', 'STRING_CONST': 'stringConstant'}

KEYWORD = "KEYWORD"
SYMBOL = "SYMBOL"
IDENTIFIER = "IDENTIFIER"
INTEGER = "INT_CONST"
STRING_CONST = "STRING_CONST"

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
OP_TO_VM = {"+": "ADD", "-": "SUB", "&": "AND", "=": "EQ", "<": "LT", ">": "GT", "|": "OR"}

UNARY_OP_LIST = ["~", "-"]
UNARY_OP_TO_VM = {"~": "NOT", "-": "NEG"}

OP_TO_FUNCTION = {"*": "Math.multiply", "/": "Math.divide"}

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

DEFINED = True
USED = False

DEFINE_OR_USE = {DEFINED: 'defined', USED: 'used'}

METHOD_LABEL = "method"
CONSTRUCTOR_LABEL = "constructor"

OOP_LABELS = [METHOD_LABEL, CONSTRUCTOR_LABEL]

COUNT_INDEX = 2
KIND_INDEX = 1
TYPE_INDEX = 0

TOKEN_INDEX = 0
TOKEN_TYPE_INDEX = 1

NOT_FOUND = "NONE"


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

        self.class_name = ""
        self.subroutines = []
        self.curr_subroutine = ""
        self.curr_subroutine_type = ""
        self.curr_expression = []
        self.curr_term = []

        self.if_label_counter = 1
        self.while_label_counter = 1

        self.expression_indicator = False

        self.symbol_table = SymbolTable()

        self.VM_writer = VMWriter(output_stream)

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
        # i = 0
        # while i < 3:
        #     self.tokenized.advance()
        #     self.produce_tokenized_line(self.tokenized.curr_token, TOKEN_MAP[self.tokenized.token_type()])
        #     i += 1

        self.output_x_tokens(2)  # class + className

        self.class_name = self.tokenized.curr_token

        self.output_x_tokens(1)  # '{'

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

            if self.expression_indicator:
                self.curr_term.append([self.tokenized.curr_token, self.tokenized.token_type()])

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # Your code goes here!
        self.initialize_class()

        while self.check_for_class_var_dec():
            self.compile_class_var_dec()

        while self.check_for_subroutine():
            self.symbol_table.start_subroutine()
            self.compile_subroutine()

        self.output_x_tokens(1)  # '}'
        self.produce_label(CLASS_LABEL, CLOSE)

    def add_variable_info(self, name: str, type: str, kind: str, def_or_use: bool):
        self.symbol_table.define(name, type, kind.upper())

        curr_count = self.symbol_table.index_of(name)
        self.final_output.append("<category> " + kind + ", <count> " + str(curr_count)
                                 + " <state> " + DEFINE_OR_USE[def_or_use] + "\n")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""

        self.produce_label(CLASS_VAR_DEC_LABEL, OPEN)
        self.output_x_tokens(3)  # static/field + type + varName

        var_kind = self.tokenized.output_[-3]  # static or field
        var_type = self.tokenized.output_[-2]  # int, str etc

        self.add_variable_info(self.tokenized.curr_token, var_type, var_kind, DEFINED)

        while self.look_ahead() != END_SENTENCE:
            self.output_x_tokens(2)  # ',' + varName
            self.add_variable_info(self.tokenized.curr_token, var_type, var_kind, DEFINED)

        self.output_x_tokens(1)  # ';'

        self.produce_label(CLASS_VAR_DEC_LABEL, CLOSE)

    def subroutine_dec_helper(self, name: str, subroutine_type: str, return_type: str) -> None:

        self.subroutines.append(name)
        self.final_output.append("<category> subroutine, <state> " + DEFINE_OR_USE[DEFINED] + "\n")

        self.curr_subroutine_type = subroutine_type
        if subroutine_type == METHOD_LABEL:
            self.symbol_table.define(THIS, self.class_name, ARGUMENT)

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function, or constructor."""
        # Your code goes here!
        self.produce_label(SUBROUTINE_DEC_LABEL, OPEN)

        self.output_x_tokens(3)  # 'constructor/function/method' + 'void/type' + name

        subroutine_type = self.tokenized.output_[-3]  # constructor/function/method
        return_type = self.tokenized.output_[-2]  # void/int/str etc...
        self.curr_subroutine = self.tokenized.curr_token
        self.subroutine_dec_helper(self.curr_subroutine, subroutine_type, return_type)

        self.output_x_tokens(1)  # '('
        self.compile_parameter_list()
        self.output_x_tokens(1)  # ')'
        self.compile_subroutine_body(subroutine_type)

        self.produce_label(SUBROUTINE_DEC_LABEL, CLOSE)

    def compile_parameter_var(self) -> None:
        var_name = self.tokenized.curr_token
        var_type = self.tokenized.output_[-2]
        self.add_variable_info(var_name, var_type, ARGUMENT, DEFINED)

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!

        self.produce_label(PARAM_LIST_LABEL, OPEN)
        if self.look_ahead() != ")":
            self.output_x_tokens(2)  # type + varName
            self.compile_parameter_var()

        while self.look_ahead() != ")":
            self.output_x_tokens(3)  # ',' + type + varName
            self.compile_parameter_var()

        self.produce_label(PARAM_LIST_LABEL, CLOSE)

    def check_for_var_dec(self) -> bool:
        if self.look_ahead() in VAR_DEC_LABEL:
            return True
        return False

    def write_subroutine_vm(self) -> None:

        name = self.class_name + "." + self.curr_subroutine
        local_var_count = self.symbol_table.var_count_return(VARIABLE)
        self.VM_writer.write_function(name, local_var_count)

    def compile_method_align(self) -> None:
        self.VM_writer.write_push(ARGUMENT, 0)
        self.VM_writer.write_pop("POINTER", 0)

    def compile_constructor(self) -> None:
        """Allocate memory block and aligning virtual memory segment 'this' with base address of allocated block"""
        n_fields = self.symbol_table.var_count_return(FIELD)
        self.VM_writer.write_push("CONST", n_fields)
        self.VM_writer.write_call("Memory.alloc", 1)
        self.VM_writer.write_pop("POINTER", 0)

    def compile_subroutine_body(self, subroutine_type) -> None:
        """Compiles a subroutine body consisting of {varDec* statements}"""
        self.produce_label(SUBROUTINE_BODY_LABEL, OPEN)
        self.output_x_tokens(1)  # '{'

        while self.check_for_var_dec():
            self.compile_var_dec()

        self.write_subroutine_vm()

        if subroutine_type == METHOD_LABEL:  # align virtual memory segment 'this' with the base address of the object
            self.compile_method_align()

        if subroutine_type == CONSTRUCTOR_LABEL:
            self.compile_constructor()

        self.compile_statements()

        self.output_x_tokens(1)  # '}'
        self.produce_label(SUBROUTINE_BODY_LABEL, CLOSE)

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.produce_label(VAR_DEC_LABEL, OPEN)
        self.output_x_tokens(3)  # 'var' + type + varName
        var_type = self.tokenized.output_[-2]
        self.add_variable_info(self.tokenized.curr_token, var_type, VARIABLE, DEFINED)
        while self.look_ahead() != END_SENTENCE:
            self.output_x_tokens(2)  # ',' + varName
            self.add_variable_info(self.tokenized.curr_token, var_type, VARIABLE, DEFINED)

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

    def is_call_method(self, name) -> bool:

        var_kind = self.symbol_table.kind_of(name)
        if self.symbol_table.kind_of(name) != NOT_FOUND:  # must be calling a method
            segment, index = self.generate_var_info(name)
            self.VM_writer.write_push(segment, index)
            return True

        return False

    def subroutine_call(self):
        self.output_x_tokens(1)  # [subroutineName | className | varName]
        name = self.tokenized.curr_token

        is_method = self.is_call_method(name)
        count = 0
        if is_method:
            count = 1  # add 1 to argument count
            name = self.symbol_table.type_of(name)

        if self.look_ahead() == ".":
            self.output_x_tokens(2)  # '.' + subroutineName
            name += "." + self.tokenized.curr_token
        else:  # need to add class name?
            if self.curr_subroutine_type in OOP_LABELS:
                count = 1
                self.VM_writer.write_push("POINTER", 0)

            name = self.class_name + "." + name

        self.output_x_tokens(1)  # '('
        count += self.compile_expression_list()
        self.output_x_tokens(1)  # ')'

        self.VM_writer.write_call(name, count)

    def compile_do(self) -> None:
        """Compiles a do statement."""

        self.produce_label(DO_LABEL, OPEN)
        self.output_x_tokens(1)  # 'do'
        self.subroutine_call()
        self.output_x_tokens(1)  # ';'

        self.VM_writer.write_pop("TEMP", 0)
        self.produce_label(DO_LABEL, CLOSE)

    def check_for_array_index(self) -> bool:
        if self.look_ahead() == "[":
            return True
        return False

    def generate_var_info(self, name):
        var_kind = self.symbol_table.kind_of(name)
        index = self.symbol_table.index_of(name)
        segment = ""
        if var_kind == FIELD:  # field variable, need to push this
            segment = "THIS"
        elif var_kind == VARIABLE:
            segment = "LOCAL"
        elif var_kind == ARGUMENT:
            segment = "ARG"
        elif var_kind == STATIC:
            segment = "STATIC"

        return segment, index

    def handle_array_LHS_let(self, var_name) -> None:
        var_segment, var_index = self.generate_var_info(var_name)
        self.VM_writer.write_push(var_segment, var_index)
        self.output_x_tokens(1)  # '['
        self.compile_expression()
        self.output_x_tokens(1)  # ']'

        self.VM_writer.write_arithmetic("ADD")  # arr + expression1

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.produce_label(LET_LABEL, OPEN)
        self.output_x_tokens(2)  # 'let' + varName
        var_name = self.tokenized.curr_token
        array_flag = False
        if self.check_for_array_index():  # handling arr[expression1] = expression2
            array_flag = True
            self.handle_array_LHS_let(var_name)

        self.output_x_tokens(1)  # '='
        self.compile_expression()
        self.output_x_tokens(1)  # ';'

        if array_flag:
            self.VM_writer.write_pop("TEMP", 0)  # save value of expression 2
            self.VM_writer.write_pop("POINTER", 1)  # RAM address of a[i]
            self.VM_writer.write_push("TEMP", 0)
            self.VM_writer.write_pop("THAT", 0)

        else:
            segment, index = self.generate_var_info(var_name)
            self.VM_writer.write_pop(segment, index)  # popping expression into variable

        self.produce_label(LET_LABEL, CLOSE)

    def compile_while(self) -> None:
        """Compiles a while statement."""

        self.produce_label(WHILE_LABEL, OPEN)

        label_num = self.while_label_counter
        while_label_start = "While_Label_Start_" + str(label_num)
        while_label_exit = "While_Label_Exit_" + str(label_num)
        self.while_label_counter += 1

        self.VM_writer.write_label(while_label_start)

        self.output_x_tokens(2)  # 'while' + '('
        self.compile_expression()

        self.VM_writer.write_arithmetic("NOT")
        self.VM_writer.write_if(while_label_exit)
        self.output_x_tokens(2)  # ')' + '{'
        self.compile_statements()
        self.output_x_tokens(1)  # '}'

        self.VM_writer.write_goto(while_label_start)
        self.VM_writer.write_label(while_label_exit)
        self.produce_label(WHILE_LABEL, CLOSE)

    def check_for_return_expression(self) -> bool:
        if self.look_ahead() != END_SENTENCE:
            return True
        return False

    def compile_return(self) -> None:
        """Compiles a return statement."""

        self.produce_label(RETURN_LABEL, OPEN)

        self.output_x_tokens(1)  # 'return'

        void_flag = True
        if self.check_for_return_expression():
            void_flag = False
            self.compile_expression()

        if void_flag:  # if function is a void method, need to return 0
            self.VM_writer.write_push("CONST", 0)

        self.VM_writer.write_return()  # return statement in VM

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

        self.VM_writer.write_arithmetic("NOT")
        self.output_x_tokens(2)  # ')' + '{'
        label_num = self.if_label_counter
        label_name = "Label_Else_" + str(label_num)
        self.VM_writer.write_if(label_name)
        self.if_label_counter += 1
        self.compile_statements()
        self.output_x_tokens(1)  # '}'

        label_skip_else = "Label_Skip_If_" + str(label_num)
        self.VM_writer.write_goto(label_skip_else)
        self.VM_writer.write_label(label_name)
        if self.check_for_else():
            self.compile_else()

        self.VM_writer.write_label(label_skip_else)
        self.produce_label(IF_LABEL, CLOSE)

    def check_for_op(self) -> bool:
        if self.look_ahead() in OP_LIST:
            return True
        return False

    def output_unary_op(self, unary_op_term):
        if unary_op_term in UNARY_OP_TO_VM:
            self.VM_writer.write_arithmetic(UNARY_OP_TO_VM[unary_op_term])

    def output_op(self, op_term) -> None:
        if op_term in OP_TO_VM:
            self.VM_writer.write_arithmetic(OP_TO_VM[op_term])  # translating op term to VM code

        elif op_term in OP_TO_FUNCTION:
            self.VM_writer.write_call(OP_TO_FUNCTION[op_term], 2)  # multiply or divide

    def exp_is_variable(self, name):

        segment, index = self.generate_var_info(name)
        self.VM_writer.write_push(segment, index)

    def exp_is_array(self, term) -> None:
        pass

    def handle_term_keyword(self, keyword) -> None:
        if keyword == KEYWORD_CONSTANTS[0]:  # true
            self.VM_writer.write_push("CONST", 1)
            self.VM_writer.write_arithmetic("NEG")
        elif keyword == KEYWORD_CONSTANTS[1]:  # false
            self.VM_writer.write_push("CONST", 0)
        elif keyword == KEYWORD_CONSTANTS[2]:  # null
            self.VM_writer.write_push("CONST", 0)
        elif keyword == KEYWORD_CONSTANTS[3]:  # this
            self.VM_writer.write_push("POINTER", 0)

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        self.produce_label(EXPRESSION_LABEL, OPEN)
        self.compile_term()
        while self.check_for_op():
            self.output_x_tokens(1)  # 'op'
            op_token = self.tokenized.curr_token
            self.compile_term()
            self.output_op(op_token)

        self.produce_label(EXPRESSION_LABEL, CLOSE)

    def handle_string_const(self, string_const):

        if string_const[0] == '"':
            string_const = string_const[1:-1]
        string_length = len(string_const)

        self.VM_writer.write_push("CONST", string_length)
        self.VM_writer.write_call("String.new", 1)
        for letter in string_const:
            self.VM_writer.write_push("CONST", ord(letter))
            self.VM_writer.write_call("String.appendChar", 2)

    def write_to_VM_identifier(self, single_token):

        token_type = self.tokenized.token_type()
        if token_type == INTEGER:  # push constant
            self.VM_writer.write_push("CONST", int(single_token))
        elif token_type == IDENTIFIER:  # must be variable
            self.exp_is_variable(single_token)
        elif token_type == KEYWORD:
            self.handle_term_keyword(single_token)
        elif token_type == STRING_CONST:
            self.handle_string_const(single_token)

    def handle_array_term(self) -> None:
        self.output_x_tokens(1)  # varName
        var_name = self.tokenized.curr_token
        var_segment, var_index = self.generate_var_info(var_name)
        self.VM_writer.write_push(var_segment, var_index)
        self.output_x_tokens(1)  # '['
        self.compile_expression()
        self.output_x_tokens(1)  # ']'

        self.VM_writer.write_arithmetic("ADD")

        self.VM_writer.write_pop("POINTER", 1)
        self.VM_writer.write_push("THAT", 0)

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

        self.curr_term = []
        if self.look_ahead() == "(":  # if starts with open bracket, must be '(expression)'
            self.output_x_tokens(1)  # '('
            self.compile_expression()
            self.output_x_tokens(1)  # ')'
        elif self.look_ahead() in UNARY_OP_LIST:  # (unaryOp term)
            self.output_x_tokens(1)  # 'unaryOp'
            unary_op = self.tokenized.curr_token
            self.compile_term()
            self.output_unary_op(unary_op)
        elif self.look_two_ahead() in ARRAY_INDICATOR:  # term is of the form varName[expression]
            self.handle_array_term()
        elif self.look_two_ahead() in SUBROUTINE_INDICATORS:
            self.subroutine_call()
        else:
            self.output_x_tokens(1)  # lone identifier
            single_token = self.tokenized.curr_token
            self.write_to_VM_identifier(single_token)

        self.produce_label(TERM_LABEL, CLOSE)

    def compile_expression_list(self) -> int:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        self.produce_label(EXPRESSION_LIST_LABEL, OPEN)

        count = 0
        if self.look_ahead() != ")":
            self.compile_expression()
            count += 1
            while self.look_ahead() != ")":
                self.output_x_tokens(1)  # ','
                self.compile_expression()
                count += 1

        self.produce_label(EXPRESSION_LIST_LABEL, CLOSE)

        return count
