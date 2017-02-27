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
        #   Functions
        #
        'character',        PythonBuiltIn.chr,
        'globals',          PythonBuiltIn.globals,
        'introspection',    PythonBuiltIn.dir,
        'iterate',          PythonBuiltIn.iter,
        'iterate_range',    PythonBuiltIn.range,
        'ordinal',          PythonBuiltIn.ord,
        'portray',          PythonBuiltIn.repr,
        'property',         PythonBuiltIn.property,
        'sorted_list',      PythonBuiltIn.sorted,
        'type',             PythonBuiltIn.type,


        #
        #   Types
        #
        'Map',              PythonBuiltIn.dict,
        'FrozenSet',        PythonBuiltIn.frozenset,
        'Object',           PythonBuiltIn.object,
    )
