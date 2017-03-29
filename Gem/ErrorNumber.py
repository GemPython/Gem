#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.ErrorNumber')
def gem():
    require_gem('Gem.Import')


    PythonErrorNumber = import_module('errno')


    export(
        'ERROR_NO_ACCESS',  PythonErrorNumber.EACCES,
        'ERROR_NO_ENTRY',   PythonErrorNumber.ENOENT,
    )
