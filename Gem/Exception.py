#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.Exception')
def gem():
    require_gem('Gem.Import')


    PythonException = (import_module('exceptions')   if is_python_2 else  PythonBuiltIn)
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
    @built_in
    def raise_runtime_error(format, *arguments):
        runtime_error = (format   % arguments   if arguments else   format)

        raise RuntimeError(runtime_error)


    #
    #   raise_value_error
    #
    @built_in
    def raise_value_error(format, *arguments):
        value_error = format % arguments

        #
        #   Since the next line will appear in stack traces, make it look prettier by using 'value_error'
        #   (to make the line shorter & more readable)
        #
        raise ValueError(value_error)


    if is_python_2:
        EnvironmentError = PythonException.EnvironmentError


        class FileNotFoundError(EnvironmentError):
            pass


        class PermissionError(EnvironmentError):
            pass
    else:
        FileNotFoundError = PythonBuiltIn.FileNotFoundError
        PermissionError   = PythonBuiltIn.PermissionError


    export(
        #
        #   Exception Types
        #
        'FileNotFoundError',  FileNotFoundError,
        'ImportError',        PythonException.ImportError,
        'OSError',            PythonException.OSError,
        'PermissionError',    PermissionError,

        #
        #   Functions
        #
        'exception_information',    PythonSystem.exc_info,
    )
