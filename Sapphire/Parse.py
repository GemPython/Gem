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



    class EmptyLine(Token):
        __slots__ = ((
            'portray',                  #   String
        ))


        def __init__(t, portray, s):
            t.portray = portray
            t.s       = s


        def __repr__(t):
            return arrange('<%s>', t.portray)


    empty_line    = EmptyLine('EmptyLine', '')
    empty_comment = EmptyLine('EmptyComment', '#')


    class UnknownLine(Token):
        pass


    @share
    def parse_python_from_path(path):
        data        = read_text_from_path('../Sapphire/Main.py')
        many        = []
        append_line = many.append

        for s in data.splitlines():
            m = comment_match(s)

            if m is not none:
                comment = m.group('comment')

                if comment is not none:
                    if comment == '':
                        append_line(empty_comment)
                        continue


                    append_line(Comment(comment))
                    continue

                append_line(empty_line)
                continue

            append_line(UnknownLine(s))

        for v in many:
            line('%r', v)
