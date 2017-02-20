#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.Path')
def gem():
    PythonPath = __import__('os.path').path


    export(
        'path_basename',            PythonPath.basename,
        'path_join',                PythonPath.join,
        'path_split_extension',     PythonPath.splitext,
    )
