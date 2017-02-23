if __name__ == '__main__':
    def execute(f):
        PythonSystem    = __import__('sys')
        is_python_2     = PythonSystem.version_info.major is 2
        PythonBuiltIn   = __import__('__builtin__'  if is_python_2 else   'builtins')
        PythonException = (__import__('exceptions')   if is_python_2 else  PythonBuiltIn)
        PythonTraceBack = __import__('traceback')


        SystemExit = PythonException.SystemExit


        try:
            assert f.__name__ == '__name__'

            del globals()['execute']    #   Delete ourselves

            f()                         #   Execute '__name__'

            return __name__             #   Return original '__name__' -- Thus leaving clean globals
        except:
            [e_type, e, traceback] = PythonSystem.exc_info()

            if e_type is SystemExit:    #   Builtin
                raise

            #
            #   Use 'traceback.tb_next' to remove ourselves from the stack trace
            #
            try:
                PythonTraceBack.print_exception(e_type, e, traceback.tb_next)
            finally:
                e_type = e = traceback = 0

            PythonSystem.exit(1)


    @execute
    def __name__():
        PythonPlatform  = __import__('platform')
        PythonSystem    = __import__('sys')
        is_python_2     = PythonSystem.version_info.major is 2
        is_python_3     = PythonSystem.version_info.major is 3
        PythonBuiltIn   = __import__('__builtin__'  if is_python_2 else   'builtins')
        PythonTraceBack = __import__('traceback')
        PythonTypes     = __import__('types')


        #
        #   Python keywords
        #       implemented as keywords in Python 3.0 --so can't use an expression like 'PythonBuiltIn.None'.
        #
        false = False
        none  = None


        #
        #   Python Functions
        #
        intern_string = (PythonBuiltIn   if is_python_2 else   PythonSystem).intern
        iterate       = PythonBuiltIn.iter
        length        = PythonBuiltIn.len
        portray       = PythonBuiltIn.repr
        type          = PythonBuiltIn.type


        #
        #   Python Types
        #
        FrozenSet = PythonBuiltIn.frozenset
        Method    = PythonTypes.MethodType
        NoneType  = none.__class__
        Object    = PythonBuiltIn.object
        Tuple     = PythonBuiltIn.tuple


        #
        #   Exceptions
        #
        PythonException = (__import__('exceptions')   if is_python_2 else  PythonBuiltIn)
        SystemExit      = PythonException.SystemExit



        #
        #   arrange
        #
        def arrange(format, *arguments):
            return format % arguments


        #
        #   line
        #
        flush_standard_output = PythonSystem.stdout.flush
        write_standard_output = PythonSystem.stdout.write
        position_cache        = [0]
        position              = Method(position_cache.__getitem__, 0)
        save_position         = Method(position_cache.__setitem__, 0)
        save_position_0       = Method(save_position, 0)


        def line(format = none, *arguments):
            if format is none:
                assert length(arguments) is 0

                write_standard_output('\n')
            else:
                if position() != 0:
                    write_standard_output(' ' + (format % arguments   if arguments else   format) + '\n')
                else:
                    write_standard_output((format % arguments   if arguments else   format) + '\n')

            flush_standard_output()
            save_position_0()



        def partial(format, *arguments):
            s = (format % arguments   if arguments else   format)

            write_standard_output(s)
            flush_standard_output()

            save_position(position() + length(s))


        #
        #   PrintHeader_and_PrintAndIgnoreExceptions
        #
        class PrintHeader_and_PrintAndIgnoreExceptions():
            __slots__ = ((
                'header',               #   String
            ))


            def __init__(t, header):
                t.header = header

            
            def __enter__(t):
                partial('%s ...', t.header)

                return t


            def __exit__(t, e_type, e_value, e_traceback):
                if (e_value is None) or (e_type is SystemExit):
                    return

                if position() != 0:
                    line()

                PythonTraceBack.print_exception(e_type, e_value, e_traceback.tb_next)

                #
                #   Swallow exception
                #
                return false


        def safe(header):
            return PrintHeader_and_PrintAndIgnoreExceptions(header)


        #
        #   python_version
        #
        def python_version():
            version_information = PythonSystem.version_info
            build_information   = PythonPlatform.python_build()

            assert (type(build_information) is Tuple) and (length(build_information) == 2)

            return arrange('%d%s%s%s (%s %s)',
                           version_information.major,
                           (
                               ''   if version_information.minor == version_information.micro == 0 else
                               arrange('.%d', version_information.micro)
                           ),
                           (
                               ''   if version_information.micro == 0 else
                               arrange('.%d', version_information.micro)
                           ),
                           (
                               ''   if version_information.serial == 0 else
                               arrange('.%d', version_information.serial)
                           ),
                           build_information[0],
                           build_information[1])



        with safe('Python version'):
            line(python_version())


        #
        #   Executable
        #
        lookup_PythonSystem = PythonSystem.__dict__.get

        with safe('Python executable'):
            executable = lookup_PythonSystem('executable')

            line('unknown'   if executable is none else   portray(executable))
