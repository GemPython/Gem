#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Sapphire.Parse')
def gem():
    require_gem('Sapphire.Match')


    class Token(Object):
        __slots__ = ((
            's',
        ))


        def __init__(t, s):
            t.s = s


        def __repr__(t):
            return arrange('<%s %s>', t.__class__.__name__, portray_string(t.s))


    class Comment(Token):
        __slots__ = (())


    class IndentedComment(Token):
        __slots__ = ((
            'indented',                     #   String
        ))


        def __init__(t, indented, s):
            t.indented = indented
            t.s        = s


        def __repr__(t):
            if t.s is '':
                return arrange('<+# %r #>', t.indented)

            return arrange('<+# %r # %s>', t.indented, portray_string(t.s))


    class DefineHeader(Token):
        __slots__ = ((
            'indented',                     #   String
            'keyword_define',               #   String
            'name',                         #   String
            'left_parenthesis',             #   String
            'argument_1',                   #   String
            'right_parenthesis__colon',     #   String
        ))


        def __init__(t, indented, keyword_define, name, left_parenthesis, argument_1, right_parenthesis__colon):
            t.indented                 = indented
            t.keyword_define           = keyword_define
            t.name                     = name
            t.left_parenthesis         = left_parenthesis
            t.argument_1               = argument_1
            t.right_parenthesis__colon = right_parenthesis__colon


        def  __repr__(t):
            return arrange('<DefineHeader %r %s %s %s %s %s>',
                           t.indented,
                           portray_string(t.keyword_define),
                           t.name,
                           portray_string(t.left_parenthesis),
                           t.argument_1,
                           portray_string(t.right_parenthesis__colon))


    class EmptyComment(Token):
        __slots__ = (())


        @static_method
        def __repr__():
            return '<EmptyComment>'


    empty_comment = EmptyComment('')


    class EmptyLine(Token):
        __slots__ = (())


        def __repr__(t):
            if t.s is '':
                return '<EmptyLine>'

            return arrange('<EmptyLine %r>', t.s)


    empty_line = EmptyLine('')


    class UnknownLine(Token):
        pass


    @share
    def parse_python_from_path(path):
        data        = read_text_from_path('../Sapphire/Main.py')
        many        = []
        append_line = many.append

        for s in data.splitlines():
            m = line_match(s)

            if m is not none:
                [indented, comment] = m.group('ow1', 'comment')

                if comment is not none:
                    if indented is '':
                        if comment is '':
                            append_line(empty_comment)
                            continue

                        append_line(Comment(comment))
                        continue

                    append_line(IndentedComment(indented, comment))
                    continue

                keyword_define= m.group('keyword_define')

                if keyword_define is not none:
                    [
                        name_1, left_parenthesis, name_2, right_parenthesis__colon,
                    ] = m.group('name_1', 'left_parenthesis', 'name_2', 'right_parenthesis__colon')

                    append_line(
                        DefineHeader(
                            indented,
                            keyword_define,
                            name_1,
                            left_parenthesis,
                            name_2,
                            right_parenthesis__colon,
                        ),
                    )

                    continue


                if indented is '':
                    append_line(empty_line)
                    continue

                append_line(EmptyLine(indented))
                continue

            append_line(UnknownLine(s))

        for v in many:
            line('%r', v)
