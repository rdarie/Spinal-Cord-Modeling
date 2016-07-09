# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 19:14:49 2016

@author: Radu
"""

from pyparsing import Word, nums, OneOrMore, Keyword, Literal, ZeroOrMore, Optional, Group
import pdb
from string import lowercase

def print_for_loop(target_file, ntabs):
    def for_parseaction(origString, loc, tokens):
        for n in range(ntabs):
            target_file.write('\t')
        put_string = 'for ' + tokens[0] + ' in range(' + tokens[1] + ', ' + tokens[2] + '):\n\t'
        target_file.write(put_string)
    return for_parseaction

def update_current_section(target_file, ntabs):
    def update_cs_parseaction(origString, loc, tokens):
        for n in range(ntabs):
            target_file.write('\t')
        global current_section_name
        current_section_name = 'self.'
        if isinstance(tokens[0], str):
        # single section
            current_section_name += tokens[0] + '[0]'
        elif isinstance(tokens[0], type(tokens)):
            current_section_name += tokens[0][0] + '['
            for a in range(1,len(tokens[0])):
                current_section_name += tokens[0][a]
            current_section_name += ']'
        put_string = 'h.pt3dclear(sec = ' + current_section_name + ')\n'
        target_file.write(put_string)
    return update_cs_parseaction

def print_point_add(target_file, ntabs):
    def point_add_parseaction(origString, loc, tokens):
        for n in range(ntabs):
            target_file.write('\t')
        put_string = 'h.pt3dadd('
        for a in range(len(tokens)):
            if isinstance(tokens[a], str):
                put_string += tokens[a]
            elif isinstance(tokens[a], type(tokens)):
                for b in range(len(tokens[a])):
                    put_string+= tokens[a][b]
            put_string += ', '
        put_string += 'sec = ' + current_section_name + ')\n'
        target_file.write(put_string)
    return point_add_parseaction

def print_point_style(target_file, ntabs):
    def point_style_parseaction(origString, loc, tokens):
        for n in range(ntabs):
            target_file.write('\t')
        put_string = 'h.pt3dstyle('
        for a in range(len(tokens)):
            if isinstance(tokens[a], str):
                put_string += tokens[a]
            elif isinstance(tokens[a], type(tokens)):
                for b in range(len(tokens[a])):
                    put_string+= tokens[a][b]
            put_string += ', '
        put_string += 'sec = ' + current_section_name + ')\n'
        target_file.write(put_string)
    return point_style_parseaction

def print_create(target_file, ntabs):
    def create_parseaction(origString, loc, tokens):
        for a in range(len(tokens)):
            if isinstance(tokens[a], str):
                # single section
                put_string = 'self.' + tokens[a] + ' = [h.Section(name = \''+ tokens[a] +'\', cell = self)]\n'
            elif isinstance(tokens[a], type(tokens)):
                put_string = 'self.' + tokens[a][0] + ' = [h.Section(name = \'' + tokens[a][0] + '_%d\' % x, cell = self) for x in range(' + tokens[a][1]\
                + ')]\n'
            for n in range(ntabs):
                target_file.write('\t')
            target_file.write(put_string)
        target_file.write('\n')
    return create_parseaction

def connect_output_string(tokens):
    if isinstance(tokens[0][0], str):
        # tokens [0][0] is the name of the parent section
        parent = tokens[0][0] +'[0]'
    elif isinstance(tokens[0][0], type(tokens)):
        parent = tokens[0][0][0] + '['
        for a in range(1,len(tokens[0][0])):
            parent += tokens[0][0][a]
        parent += ']'
    # tokens [0][1] is the location in the parent where we connect to
    parent_loc = ''
    for a in range(len(tokens[0][1])):
        parent_loc += tokens[0][1][a]
    if isinstance(tokens[1][0], str):
        # tokens [0][0] is the name of the child section
        child = tokens[1][0] + '[0]'
    elif isinstance(tokens[1][0], type(tokens)):
        child = tokens[1][0][0] + '['
        for a in range(1,len(tokens[1][0])):
            child += tokens[1][0][a]
        child += ']'
    # tokens [1][1] is the location in the child where we connect to
    child_loc = ''
    for a in range(len(tokens[1][1])):
        child_loc += tokens[1][1][a]
    #pdb.set_trace()
    put_string = 'self.' + parent + '.connect(' + 'self.' + child + ', ' + child_loc + ', ' + parent_loc + ')\n'
    return put_string

def print_connect(target_file, ntabs):
    def connect_parseaction(origString, loc, tokens):
        for n in range(ntabs):
            target_file.write('\t')
        put_string = connect_output_string(tokens)
        target_file.write(put_string)
    return connect_parseaction

def print_geom_define(target_file, ntabs):
    def geom_define_parseaction(origString, loc, tokens):
        for n in range(ntabs):
            target_file.write('\t')
        target_file.write('geom_define\n')
        target_file.write(tokens[0])
    return geom_define_parseaction

# Resulting python file
def parse_morphology(filename, filename_toparse):
    global current_section_name
    current_section_name = ''
    converted_file = open(filename, 'w')

    put_string = 'from neuron import h\ndef shape_3D(self):\n'
    converted_file.write(put_string)
    ntabs = 1 # from here on, add a tab to all lines
    # define lists of characters for a..z and 1..9
    uppercase = lowercase.upper()
    lowercaseplus = lowercase+('_')
    lowercaseplus = lowercaseplus+(uppercase)
    nonzero = ''.join([str(i) for i in range(1, 10)])

    COMMA   = Literal(',')
    EQUALS  = Literal('=')
    MINUS   = Literal('-')
    PERIOD  = Literal('.')

    LCURL   = Literal('{')
    RCURL   = Literal('}')

    LBRACK  = Literal('(')
    RBRACK  = Literal(')')

    LSQUARE = Literal('[')
    RSQUARE = Literal(']')
    PTSCLEAR = Literal('{pt3dclear()').suppress()
    PTSCLEARNL = Literal('{\npt3dclear()\n').suppress()

    integer = Word(nums)
    single_section = Word(lowercaseplus, min = 2)
    single_section.setResultsName('SINGLE')

    integer_var = Word(lowercase, exact = 1)

    double = Group(Optional(MINUS) + integer + Optional(PERIOD + integer))

    operand = integer ^ integer_var
    operator = Word('+-*/', exact=1)

    unaryoperation = operand
    binaryoperation = operand + operator + operand
    operation = unaryoperation ^ binaryoperation

    array_section = Group(single_section + LSQUARE.suppress() + operation + RSQUARE.suppress())
    array_section.setResultsName('ARRAY')

    section = single_section ^ array_section

    section_location = Group(section + LBRACK.suppress() + double + RBRACK.suppress())

    create   = Keyword('create').suppress()  + section          + ZeroOrMore(COMMA.suppress() + section)
    create.setParseAction(print_create(converted_file, ntabs))

    connect  = Keyword('connect').suppress() + section_location + COMMA.suppress()  + section_location
    connect.setParseAction(print_connect(converted_file, ntabs))

    for_loop = Keyword('for').suppress()     + integer_var      + EQUALS.suppress()  + integer + COMMA.suppress() + integer
    # NOTE TO FUTURE SELF: for loops can only have one line of code in this implementation
    for_loop.setParseAction(print_for_loop(converted_file, ntabs))

    point_add = Literal('pt3dadd(').suppress() + double + COMMA.suppress() + double + COMMA.suppress() + double + COMMA.suppress() + double + RBRACK.suppress()
    point_add.setParseAction(print_point_add(converted_file, ntabs))

    point_style = Literal('pt3dstyle(').suppress() + double + COMMA.suppress() + double + COMMA.suppress()  + double + COMMA.suppress()  + double + RBRACK.suppress()
    point_style.setParseAction(print_point_style(converted_file, ntabs))

    geom_define_pre = section + (PTSCLEAR ^ PTSCLEARNL)
    geom_define_body = OneOrMore(point_add ^ point_style) + RCURL.suppress()
    geom_define_pre.setParseAction(update_current_section(converted_file, ntabs))

    geom_define = geom_define_pre + geom_define_body

    expression = (connect ^ for_loop ^ geom_define ^ create)
    codeblock = OneOrMore(expression)

    test_str = 'Ia_node[0] {\npt3dclear()\n pt3dadd( 47, 76, 92.5, 3.6) }'
    #file_to_parse = open('../../tempdata/Ia_geometry')
    file_to_parse = open(filename_toparse)
    tokens = codeblock.parseString(file_to_parse.read())
    #tokens = codeblock.parseString(test_str)
