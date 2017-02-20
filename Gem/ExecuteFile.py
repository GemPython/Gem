#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.ExecuteFile')
def gem():
    require_gem('Gem.File')
    require_gem('Gem.Path')


    from Gem import Module, open_file, path_basename, path_split_extension


    if is_python_2:
        execute_file = PythonCore.execfile


        @export
        def execute_python_from_file(path):
            path                  = intern_string(path)
            [basename, extension] = path_split_extension(path_basename(path))
            basename              = intern_string(basename)
            module                = Module(basename)

            execute_file(path, module.__dict__)

            return module


    else:
        compile_python = PythonCore.compile
        execute_python = PythonCore.eval


        @export
        @privileged
        def execute_python_from_file(path):
            path                  = intern_string(path)
            [basename, extension] = path_split_extension(path_basename(path))
            basename              = intern_string(basename)
            module                = Module(basename)

            with open_file(path) as f:
                code = compile_python(f.read(), path, 'exec')
                execute_python(code, module.__dict__)

            return module
