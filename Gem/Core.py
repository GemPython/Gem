#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.Core')
def gem():
    PythonSystem = __import__('sys')
    is_python_2   = PythonSystem.version_info.major is 2
    PythonCore    = __import__('__builtin__'  if is_python_2 else   'builtins')


    #
    #   Python Functions
    #
    intern_string = (PythonCore   if is_python_2 else   PythonSystem).intern
    length        = PythonCore.len


    #
    #   Python Keywords
    #
    none = None


    #
    #   arrange
    #
    @export
    def arrange(format, *arguments):
        return format % arguments


    #
    #   line
    #
    flush_standard_output = PythonSystem.stdout.flush
    write_standard_output = PythonSystem.stdout.write


    @export
    def line(format = none, *arguments):
        if format is none:
            assert length(arguments) is 0

            write_standard_output('\n')
        else:
            write_standard_output((format % arguments   if arguments else   format) + '\n')

        flush_standard_output()


    export(
        #
        #   Functions
        #
        'intern_string',    intern_string,
        'introspection',    PythonCore.dir,
        'iterate',          PythonCore.iter,
        'length',           length,
        'property',         PythonCore.property,
        'type',             PythonCore.type,

        #
        #   Keywords
        #       implemented as keywords in Python 3.0 --so can't use something like PythonCore.None.
        #
        'false',    False,
        'none',     None,
        'true',     True,

        #
        #   Modules
        #
        'PythonCore',       PythonCore,
        'PythonSystem',     PythonSystem,

        #
        #   Types
        #
        'FrozenSet',        PythonCore.frozenset,
        'Module',           PythonCore.__class__,
        'Object',           PythonCore.object,
        'String',           PythonCore.str,

        #
        #   Values
        #
        'is_python_2',      is_python_2,
    )
