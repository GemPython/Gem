#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.Path')
def gem():
    require_gem('Gem.CatchException')
    require_gem('Gem.ErrorNumber')
    require_gem('Gem.Import')


    PythonOperatingSystem = import_module('os')
    PythonPath            = import_module('os.path')
    python__rename_path   = PythonOperatingSystem.rename
    python__remove_path   = PythonOperatingSystem.remove
    open_path             = PythonBuiltIn.open


    @export
    @privileged_2
    def read_text_from_path(path):
        with open_path(path, 'r') as f:
            return f.read()


    @export
    @privileged_2
    def write_binary_to_path(path, data):
        with open_path(path, 'wb') as f:
            return f.write(data)


    if is_python_2:
        def adjust_OSError_exception():
            [e_type, e, e_traceback] = e_all = exception_information()

            assert e_type is OSError

            arguments = e.args

            if (type(arguments) is Tuple) and (length(arguments) is 2):
                error_number = arguments[0]

                if error_number is ERROR_NO_ACCESS:
                    return ((PermissionError, arguments, e_traceback))

                if error_number is ERROR_NO_ENTRY:
                    return ((FileNotFoundError, arguments, e_traceback))

            line('e_all: %r', e_all)
            raise e_all


    if is_python_2:
        @export
        def remove_path(path):
            try:
                python__remove_path(path)
            except OSError as e:
                #
                #   NOTE:
                #       To avoid adding an extra frame in the traceback, the 'raise' must be issued in this function,
                #       instead of inside adjust_OSError_exception()
                #
                [e_type, e, e_traceback] = adjust_OSError_exception()

                raise e_type, e, e_traceback
    else:
        remove_path = python__remove_path

        export(
            'remove_path',  remove_path,
        )


    if is_python_2:
        @export
        def rename_path(from_path, to_path):
            try:
                python__rename_path(from_path, to_path)
            except OSError as e:
                #
                #   NOTE:
                #       To avoid adding an extra frame in the traceback, the 'raise' must be issued in this function,
                #       instead of inside adjust_OSError_exception()
                #
                [e_type, e, e_traceback] = adjust_OSError_exception()

                raise e_type, e, e_traceback
    else:
        rename_path = python__rename_path

        export(
            'rename_path',  rename_path,
        )


    @export
    def remove_path__ignore_file_not_found(path):
        with catch_FileNotFoundError():
            remove_path(path)


    @export
    def rename_path__ignore_file_not_found(from_path, to_path):
        with catch_FileNotFoundError():
            rename_path(from_path, to_path)


    export(
        'path_basename',            PythonPath.basename,
        'path_join',                PythonPath.join,
        'path_split_extension',     PythonPath.splitext,
    )

    restricted(
        'open_path',    PythonBuiltIn.open,
    )
