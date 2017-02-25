#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.CatchException')
def gem():
    require_gem('Gem.Exception')


    class CatchException(Object):
        __slots__ = ((
            'exception_type',           #   Type
            'caught',                   #   None | FileNotFoundError
        ))


        def __init__(t, exception_type):
            t.exception_type = exception_type
            t.caught         = none


        def __bool__(t):
            return t.caught is not none


        def __enter__(t):
            return t


        def __exit__(t, e_type, value, traceback):
            if e_type is t.exception_type:
                t.caught = value
                return true


        def __repr__(t):
            return arrange('<CatchException %r %r>', t.exception_type, t.caught)


        if is_python_2:

            __nonzero__ = __bool__


    @export
    def catch_FileNotFoundError():
        return CatchException(FileNotFoundError)
