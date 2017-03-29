#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.ExecuteFile')
def gem():
    require_gem('Gem.Path')


    from Gem import Module, path_basename, path_split_extension, read_text_from_path


    compile_python = PythonBuiltIn.compile
    execute_code   = PythonBuiltIn.eval


    @export
    def execute_python_from_file(path):
        path                  = intern_string(path)
        [basename, extension] = path_split_extension(path_basename(path))
        basename              = intern_string(basename)
        module                = Module(basename)

        execute_code(
            compile_python(read_text_from_path(path), path, 'exec'),
            module.__dict__,
        )

        return module
