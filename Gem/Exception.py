#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.Exception')
def gem():
    PythonException = (__import__('exceptions')   if is_python_2 else  PythonBuiltIn)
    RuntimeError    = PythonException.RuntimeError
    ValueError      = PythonException.ValueError


    #
    #   GENERIC NOTE:
    #       Lines with 'raise' will appear in stack traces, so make them look prettier by using
    #       a precalculated variable like 'runtime_error' (to make the line shorter & more readable)
    #       instead of doing the calculation on the line with 'raise'.
    #

    #
    #   raise_runtime_error
    #
    @export
    def raise_runtime_error(format, *arguments):
        runtime_error = (format   % arguments   if arguments else   format)

        raise RuntimeError(runtime_error)


    #
    #   raise_value_error
    #
    @export
    def raise_value_error(format, *arguments):
        value_error = format % arguments

        #
        #   Since the next line will appear in stack traces, make it look prettier by using 'value_error'
        #   (to make the line shorter & more readable)
        #
        raise ValueError(value_error)


    export(
        'FileNotFoundError',  (PythonBuiltIn.OSError   if is_python_2 else    PythonBuiltIn.FileNotFoundError),
        'ImportError',        PythonException.ImportError,
    )
