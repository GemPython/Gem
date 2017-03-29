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
    open_path             = PythonBuiltIn.open

    if is_python_2:
        require_gem('Gem.Path2')

        from Gem import rename_path, remove_path
    else:
        rename_path = PythonOperatingSystem.rename
        remove_path = PythonOperatingSystem.remove


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


    if is_python_3:
        export(
            'remove_path',  remove_path,
            'rename_path',  rename_path,
        )


    @export
    def remove_path__ignore_file_not_found(path):
        with catch_FileNotFoundError() as e:
            remove_path(path)

        return e.caught is none


    @export
    def rename_path__ignore_file_not_found(from_path, to_path):
        with catch_FileNotFoundError() as e:
            rename_path(from_path, to_path)

        return e.caught is none


    export(
        'path_basename',            PythonPath.basename,
        'path_join',                PythonPath.join,
        'path_split_extension',     PythonPath.splitext,
    )

    restricted(
        'open_path',    PythonBuiltIn.open,
    )
