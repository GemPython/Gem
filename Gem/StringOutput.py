#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.StringOutput')
def gem():
    require_gem('Gem.SimpleStringIO')


    class Indent(Object):
        __slots__ = ((
            'f',                        #   StringOutput
            'old_prefix',               #   String
            'ending',                   #   None | String
            'prefix',                   #   String
        ))


        def __init__(t, f, ending, prefix):
            t.f          = f
            t.old_prefix = f.prefix
            t.ending     = ending
            t.prefix     = prefix


        def __enter__(t):
            t.f.prefix += t.prefix

            return t


        def __exit__(t, e_type, e, e_traceback):
            t.f.prefix = t.old_prefix

            if e is none:
                if t.ending is not none:
                    t.f.line(t.ending)


    class StringOutput(Object):
        __slots__ = ((
            'f',                        #   StringIO
            'prefix',                   #   String
            '_blank',                   #   Integer
            '_write',                   #   Method
        ))


        def __init__(t, f):
            t.f      = f
            t.prefix = ''
            t._blank = -1
            t._write = f.write


        def blank(t):
            if t._blank is 0:
                t._blank = 1


        def blank2(t):
            if 0 <= t._blank < 2:
                t._blank = 2


        def close(t):
            f        = t.f
            t._write = t.f = none

            if f is not none:
                f.close()


        def indent(t, header, ending = none, prefix = 4):
            t.line(header)

            return Indent(t, ending, prefix * ' ')

            
        def finish(t):
            r = t.f.getvalue()

            t.close()

            return r


        def line(t, format = none, *arguments):
            if format is none:
                assert length(arguments) is 0

                t._write('\n')

                if t._blank > 0:
                    t._blank -= 1

                return

            if t._blank > 0:
                t._write('\n' * t._blank + t.prefix + (format % arguments   if arguments else   format) + '\n')
                t._blank = 0
                return

            t._write(t.prefix + (format % arguments   if arguments else   format) + '\n')
            t._blank = 0


    @export
    def create_StringOutput():
        return StringOutput(create_SimpleStringOutput())
