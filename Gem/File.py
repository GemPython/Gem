#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.File')
def gem():
    export(
        'open_file',    PythonCore.open,
    )
