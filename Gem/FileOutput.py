#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.FileOutput')
def gem():
    require_gem('Gem.Path')


    from Gem.Privileged import open_path


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

            t.f      = f       = open_path(t.path_new, 'w')
            t._write = f.write

            return t


        def __exit__(t, e_type, value, traceback):
            f        = t.f
            t._write = t.f = none

            f.close()

            path = t.path

            path_new = t.path_new       #   Grab t.path_new & t.path_old before zapping t.path
            path_old = t.path_old

            t.path = none

            if e_type is none:
                remove_path__ignore_file_not_found(path_old)
                rename_path__ignore_file_not_found(path, path_old)
                rename_path(path_new, path)


        def line(t, format = none, *arguments):
            if format is none:
                assert length(arguments) is 0

                t._write('\n')
                return

            t._write((format % arguments   if arguments else   format) + '\n')


        @property
        def path_new(t):
            return arrange('%s.new', t.path)


        @property
        def path_old(t):
            return arrange('%s.old', t.path)
