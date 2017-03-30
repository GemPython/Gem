#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.DelayedFileOutput')
def gem():
    require_gem('Gem.Path')
    require_gem('Gem.StringOutput')


    from Gem import create_StringOutput


    class DelayedFileOutput(Object):
        __slots__ = ((
            'path',                     #   String+
            'data',                     #   None | String
            'f',                        #   File
            'blank',                    #   Method
            'blank2',                   #   Method
            'blank_suppress',           #   Method
            'indent',                   #   Method
            'line',                     #   Method
        ))


        def __init__(t, path):
            t.path = path
            t.line = t.indent = t.blank2 = t.blank = t.f = t.data = none


        @privileged
        def __enter__(t):
            assert t.f is none

            t.f              = f       = create_StringOutput()
            t.blank2         = f.blank2
            t.blank          = f.blank
            t.blank_suppress = f.blank_suppress
            t.indent         = f.indent
            t.line           = f.line

            return t


        def __exit__(t, e_type, e, traceback):
            if e is not none:
                t.close()
                return

            data = (t.data) or (f.finish())

            path     = t.path
            path_new = t.path_new       #   Grab t.path_new & t.path_old before zapping t.path
            path_old = t.path_old

            t.path = none

            write_binary_to_path(path_new, data)
            remove_path__ignore_file_not_found(path_old)
            rename_path__ignore_file_not_found(path, path_old)
            rename_path(path_new, path)


        def close(t):
            f      = t.f
            t.line = t.indent = t.blank_suppress = t.blank2 = t.blank = t.f = t.data = none

            if f is not none:
                f.close()


        def finish(t):
            assert t.data is none

            f      = t.f
            t.line = t.indent = t.blank2 = t.blank = t.f = none

            data = t.data = f.finish()

            return data


        @property
        def path_new(t):
            return arrange('%s.new', t.path)


        @property
        def path_old(t):
            return arrange('%s.old', t.path)

        @property
        def prefix_total(t):
            return length(t.f.prefix)


    export(
        'create_DelayedFileOutput',     DelayedFileOutput,
    )
