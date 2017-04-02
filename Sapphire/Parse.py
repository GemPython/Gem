#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Sapphire.Parse')
def gem():
    require_gem('Sapphire.Match')
    require_gem('Sapphire.Statement')
    require_gem('Sapphire.Token')


    class FunctionCall_0(Object):
        __slot__ = ((
            'left',                         #   Expression
            'pair_of_parenthesis',          #   String
        ))


        def __init__(t, left, pair_of_parenthesis):
            t.left                = left
            t.pair_of_parenthesis = pair_of_parenthesis


        def __repr__(t):
            return arrange('<FunctionCall0 %r %r>', t.left, t.pair_of_parenthesis)


    class ReturnExpression(Token):
        __slots__ = ((
            'keyword_return',               #   String
            'expression',                   #   String
        ))


        def __init__(t, keyword_return, expression):
            t.keyword_return = keyword_return
            t.expression     = expression


        def  __repr__(t):
            return arrange('<Return %r %s>', t.keyword_return, t.expression)


    def parse_define_header(m0, s):
        #line(portray_raw_string(s[m0.end():]))

        m = define_1_match(s[m0.end():])

        if m is none:
            return UnknownLine(s)

        [
            name_1, left_parenthesis, name_2, right_parenthesis__colon,
        ] = m.group('name_1', 'left_parenthesis', 'name_2', 'right_parenthesis__colon')

        return DefineHeader(
                   m0.group('keyword__ow'),
                   name_1,
                   ParameterColon_1(left_parenthesis, name_2, right_parenthesis__colon),
               )


    def parse_return(m0, s):
        #line(portray_raw_string(s[m0.end():]))

        m = expression_match(s[m0.end():])

        if m is none:
            return UnknownLine(s)

        [name_1, pair_of_parenthesis] = m.group('name_1', 'pair_of_parenthesis')

        expression = Symbol(name_1)

        if pair_of_parenthesis is not none:
            expression = FunctionCall_0(expression, pair_of_parenthesis)

        return ReturnExpression(m0.group('keyword__ow'), expression)


    keyword_define.parse_line = parse_define_header
    keyword_return.parse_line = parse_return


    @share
    def parse_python_from_path(path):
        data        = read_text_from_path('../Sapphire/Main.py')
        many        = []
        append_line = many.append

        for s in data.splitlines(true):
            m = line_match(s)

            if m is none:
                append_line(UnknownLine(s))
                continue

            [
                    indented, keyword, comment, newline_2,
            ] = m.group('indented', 'keyword', 'comment', 'newline_2')

            if keyword is not none:
                assert comment is newline_2 is none

                append_line(lookup_symbol(keyword).parse_line(m, s))
                continue

            assert newline_2 is not none

            if comment is not none:
                if indented is '':
                    if comment is '':
                        append_line(empty_comment)
                        continue

                    append_line(Comment(comment))
                    continue

                append_line(IndentedComment(indented, comment))
                continue

            if indented is '':
                append_line(empty_line)
                continue

            append_line(EmptyLine(indented))
            continue

        for v in many:
            line('%r', v)
