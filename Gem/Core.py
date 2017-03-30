#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.Core')
def gem():
    @export
    def execute(f):
        f()

        return execute


    #
    #   intern_arrange
    #
    @built_in
    def intern_arrange(format, *arguments):
        return intern_string(format % arguments)


    #
    #   line
    #
    flush_standard_output = PythonSystem.stdout.flush
    write_standard_output = PythonSystem.stdout.write


    @built_in
    def line(format = none, *arguments):
        if format is none:
            assert length(arguments) is 0

            write_standard_output('\n')
        else:
            write_standard_output((format % arguments   if arguments else   format) + '\n')

        flush_standard_output()


    #
    #   privileged_2
    #
    if is_python_2:
        export(
            'privileged_2',     rename_function('privileged_2', privileged)
        )
    else:
        @export
        def privileged_2(f):
            return f


    built_in(
        #
        #   Types
        #
        'Boolean',          PythonBuiltIn.bool,
        'Bytes',            PythonBuiltIn.bytes,
        'Integer',          PythonBuiltIn.int,
        'FrozenSet',        PythonBuiltIn.frozenset,
        'List',             PythonBuiltIn.list,
        'Long',             (PythonBuiltIn.long    if is_python_2 else   PythonBuiltIn.int),
        'Map',              PythonBuiltIn.dict,
        'Object',           PythonBuiltIn.object,
        'Tuple',            PythonBuiltIn.tuple,


        #
        #   Functions
        #
        'character',        PythonBuiltIn.chr,
        'enumerate',        PythonBuiltIn.enumerate,
        'globals',          PythonBuiltIn.globals,
        'introspection',    PythonBuiltIn.dir,
        'iterate',          PythonBuiltIn.iter,
        'iterate_range',    PythonBuiltIn.range,
        'maximum',          PythonBuiltIn.max,
        'ordinal',          PythonBuiltIn.ord,
        'portray',          PythonBuiltIn.repr,
        'property',         PythonBuiltIn.property,
        'sorted_list',      PythonBuiltIn.sorted,
        'static_method',    PythonBuiltIn.staticmethod,
        'type',             PythonBuiltIn.type,

        #
        #   Values
        #
        '__debug__',        PythonBuiltIn.__debug__,
    )


    if __debug__:
        built_in(PythonException.AssertionError)
