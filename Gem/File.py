#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.File')
def gem():
    require_gem('Gem.CatchException')


    PythonOperatingSystem = __import__('os')
    remove_file           = PythonOperatingSystem.remove
    rename_file           = PythonOperatingSystem.rename


    open_file = PythonCore.open


    @export
    @privileged_2
    def read_text_file(path):
        with open_file(path) as f:
            return f.read()


    @export
    def remove_file__ignore_file_not_found(path):
        with catch_FileNotFoundError():
            remove_file(path)


    @export
    def rename_file__ignore_file_not_found(from_path, to_path):
        with catch_FileNotFoundError():
            rename_file(from_path, to_path)


    export(
        'remove_file',  PythonOperatingSystem.remove,
        'rename_file',  PythonOperatingSystem.rename,
    )

    restricted(
        'open_file',    PythonCore.open,
    )
