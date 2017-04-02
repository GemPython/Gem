#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Sapphire.ParseExpression')
def gem():
    show = true


    def parse_arguments__atom__left_parenthesis(s, m, atom):
        arguments = parse_arguments__left_parenthesis(s, m.end(), LeftParenthesis(m.group('operator__ow')))

        if arguments is none:
            return none

        line('parse_arguments__atom__left_parenthesis: incomplete #3')
        return none


    find__parse_arguments__atom__operator = {
                                                '(' : parse_arguments__atom__left_parenthesis,
                                            }.__getitem__



    def parse_arguments__left_parenthesis(s, index, left_parenthesis_0):
        m = first_argument_match(s, index)

        if m is none:
            return none

        [name, number, operator] = m.group('name', 'number', 'operator')

        if name is not none:
            assert number is none

            argument_0 = Symbol(name)
        else:
            assert number is not none

            argument_0 = Number(number)

        if operator is ',':
            comma_0 = OperatorComma(operator)
        else:
            find_parse_arguments__atom__operator(operator)(s, m, argument_0)
            line('parse_arguments__left_parenthesis: incomplete #2')
            return none

        line('parse_arguments__left_parenthesis: incomplete #3: %r, %r', argument_0, comma_0)
        return none


    @share
    def parse_expression__symbol(m0, s, name):
        if show:
            line(portray_raw_string(s[m0.end():]))

        m = postfix_match(s, m0.end())

        if m is none:
            return UnknownLine(s)

        [dot, name, left_parenthesis] = m.group('dot', 'name', 'left_parenthesis')

        arguments = parse_arguments__left_parenthesis(s, m.end(), left_parenthesis)

        if arguments is none:
            return UnknownLine(s)

        line('parse_expression__symbol: incomplete: %r %r %r %r', dot, name, left_parenthesis, arguments)
        return UnknownLine(s)
