#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.Exception')
def gem():
    PythonException = (__import__('exceptions')   if is_python_2 else  PythonBuiltIn)
    RuntimeError    = PythonException.RuntimeError


    @export
    def raise_runtime_error(format, *arguments):
        error_message = (format   % arguments   if arguments else   format)

        raise RuntimeError(error_message)


    export(
        'FileNotFoundError',  (PythonBuiltIn.OSError   if is_python_2 else    PythonBuiltIn.FileNotFoundError),
        'ImportError',        PythonException.ImportError,
    )
