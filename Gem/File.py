#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.File')
def gem():
    PythonOperatingSystem = __import__('os')


    open_file = PythonCore.open


    @export
    @privileged_2
    def read_text_file(path):
        with open_file(path) as f:
            return f.read()


    export(
        'remove_file',  PythonOperatingSystem.remove,
        'rename_file',  PythonOperatingSystem.rename,
    )

    restricted(
        'open_file',    PythonCore.open,
    )

