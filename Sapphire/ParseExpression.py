#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Sapphire.ParseExpression')
def gem():
    show = true


    tuple_of_2_nones = ((none, none))
    tuple_of_3_nones = ((none, none, none))


    def parse_arguments__atom__left_parenthesis(s, m, atom):
        [left, index] = parse_arguments__left_parenthesis(s, m.end(), OperatorLeftParenthesis(m.group('operator__ow')))

        if left is none:
            return tuple_of_3_nones

        m = argument_postfix_match(s, index)

        if m is none:
            line('parse_arguments__atom__left_parenthesis: incomplete #1A: %r %r', left, s[index:])
            return tuple_of_3_nones

        operator = m.group('operator')

        if operator is ')':
            return (( left, OperatorRightParenthesis(m.group('operator__ow')), m.end() ))

        if operator is ',':
            return (( left, OperatorComma(m.group('operator__ow')), m.end() ))

        line('parse_arguments__atom__left_parenthesis: incomplete #2: %r %r', left, operator)
        return tuple_of_3_nones


    def parse_arguments__atom__left_square_bracket(s, m, array):
        left_square_bracket = OperatorLeftSquareBracket(m.group('operator__ow'))
        m                   = index_1_match(s, m.end())

        if m is none:
            line('parse_arguments__atom__left_square_bracket: incomplete #3: %r %r', s[index:], left_square_bracket)
            return tuple_of_3_nones

        [name, number, operator] = m.group('name', 'number', 'operator')

        if name is not none:
            assert number is none

            index_1 = Symbol(name)
        else:
            assert number is not none

            index_1 = Number(number)

        if operator is ']':
            left = ExpressionIndex_1(array, left_square_bracket, index_1, OperatorRightSquareBracket(m.group('operator__ow')))
        else:
            line('parse_arguments__atom__left_square_bracket: incomplete #4: %r %r', index_1, operator)
            return tuple_of_3_nones

        m = argument_postfix_match(s, m.end())

        if m is none:
            line('parse_arguments__atom__left_square_bracket: incomplete #5A: %r %r', left, s[m.end():])
            return tuple_of_3_nones

        operator = m.group('operator')

        if operator is ')':
            line('parse_arguments__atom__left_square_bracket: incomplete #5B: %r %r', left, operator)
            return tuple_of_3_nones

        if operator is ',':
            return (( left, OperatorComma(m.group('operator__ow')), m.end() ))

        line('parse_arguments__atom__left_square_bracket: incomplete #6: %r %r', left, operator)
        return tuple_of_3_nones


    find__parse_arguments__atom__operator = {
                                                '(' : parse_arguments__atom__left_parenthesis,
                                                '[' : parse_arguments__atom__left_square_bracket,
                                            }.__getitem__



    def parse_arguments__left_parenthesis(s, index, left_parenthesis_0):
        m = argument_1_match(s, index)

        if m is none:
            line('parse_arguments__left_parenthesis: incomplete #7: %s', portray_string(s[index:]))
            return tuple_of_2_nones

        [name, number, operator] = m.group('name', 'number', 'operator')

        if name is not none:
            assert number is none

            argument_0 = Symbol(name)
        else:
            assert number is not none

            argument_0 = Number(number)

        if operator is ',':
            operator_0 = OperatorComma(operator)
            index_0    = m.end()
        else:
            [argument_0, operator_0, index_0] = find__parse_arguments__atom__operator(operator)(s, m, argument_0)

            if argument_0 is none:
                return tuple_of_2_nones

            #   (
            if operator_0.is_right_parenthesis:
                return ((
                           Arguments_1(left_parenthesis_0, argument_0, operator),
                           index_0,
                       ))

            if not operator_0.is_comma:
                line('parse_arguments__left_parenthesis: incomplete #8: %r %r', argument_0, operator_0)
                return tuple_of_2_nones

        m = argument_2_match(s, index_0)

        if m is none:
            line('parse_arguments__left_parenthesis: incomplete #9: %r %r %r', argument_0, operator_0, s[index_0:])
            return tuple_of_2_nones

        [name, number, single_quote, operator] = m.group('name', 'number', 'single_quote', 'operator')

        if name is not none:
            assert number is single_quote is none

            argument_1 = Symbol(name)
        elif number is not none:
            assert single_quote is none

            argument_1 = Number(number)
        else:
            assert single_quote is not none

            argument_1 = SingleQuote(single_quote)

        if operator is ')':
            return ((
                       Arguments_2(left_parenthesis_0, argument_0, operator_0, argument_1, OperatorRightParenthesis(operator)),
                       m.end(),
                   ))

        if operator is ',':
            comma_1 = OperatorComma(operator)
        else:
            [argument_1, operator_1, index_1] = find__parse_arguments__atom__operator(operator)(s, m, argument_1)

            if argument_1 is none:
                return tuple_of_2_nones

            line('parse_arguments__left_parenthesis: incomplete #10: %r %r %r %r %r %r',
                 left_parenthesis_0, argument_0, operator_0, argument_1, operator_1, s[index:])

            return tuple_of_2_nones

        line('parse_arguments__left_parenthesis: incomplete #11: %r, %r', argument_1, operator)
        return tuple_of_2_nones


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
