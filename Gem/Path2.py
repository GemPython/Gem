#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
#   NOTE:
#       Due to the fact that python 3.0 rejects 'raise' with three parameters, this code is in a seperate file
#
@gem('Gem.Path2')
def gem():
    require_gem('Gem.ErrorNumber')
    require_gem('Gem.Import')


    PythonOperatingSystem = import_module('os')
    PythonPath            = import_module('os.path')
    python__rename_path   = PythonOperatingSystem.rename
    python__remove_path   = PythonOperatingSystem.remove


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

        raise e_all


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
