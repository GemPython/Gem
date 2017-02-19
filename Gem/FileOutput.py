#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.FileOutput')
def gem():
    require_gem('Gem.CatchException')
    require_gem('Gem.File')
    require_gem('Gem.Path')


    from Gem import open_file


    @export
    class FileOutput(Object):
        __slots__ = ((
            'path',                     #   String+
            'f',                        #   File
            '_write',                   #   Method
        ))


        def __init__(t, path):
            t.path   = path
            t._write = t.f  = none


        @privileged
        def __enter__(t):
            assert t.f is none

            t.f      = f       = open_file(t.path_new, 'w')
            t._write = f.write

            return t


        def __exit__(t, e_type, value, traceback):
            path = t.path
            f    = t.f

            path_new = t.path_new       #   Grab t.path_new & t.path_old before zaping t.path
            path_old = t.path_old

            t._write = t.f = t.path = none

            f.close()

            if e_type is none:
                with catch_FileNotFoundError():
                    path_remove(path_old)

                with catch_FileNotFoundError():
                    path_rename(path, path_old)

                path_rename(path_new, path)


        def line(t, format, *arguments):
            t._write((format % arguments) + '\n')


        @property
        def path_new(t):
            return arrange('%s.new', t.path)


        @property
        def path_old(t):
            return arrange('%s.old', t.path)
