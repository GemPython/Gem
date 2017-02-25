#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.FileStatus')
def gem():
    PythonOperatingSystem         = __import__('os')
    PythonFileStatus              = __import__('stat')
    PythonFileStatus__inode_flags = PythonFileStatus.S_IMODE
    PythonFileStatus__file_type   = PythonFileStatus.S_IFMT
    python_file_status            = PythonOperatingSystem.stat


    class FileType(Object):
        __slots__ = ((
            'name',                     #   String+
            'is_block_device',          #   Boolean
            'is_character_device',      #   Boolean
            'is_directory',             #   Boolean
            'is_fifo',                  #   Boolean
            'is_regular_file',          #   Boolean
            'is_socket',                #   Boolean
            'is_symbolic_link',         #   Boolean
            'nonexistent',              #   Boolean
        ))


        def __init__(
                t, name,

                is_block_device     = false,
                is_character_device = false,
                is_directory        = false,
                is_fifo             = false,
                is_regular_file     = false,
                is_socket           = false,
                is_symbolic_link    = false,
                nonexistent         = false,
        ):
            assert name.__class__ is String

            assert (
                     (
                           is_block_device + is_character_device + is_directory + is_fifo + is_regular_file
                         + is_socket + is_symbolic_link + nonexistent
                     )
                  == 1
            )

            t.name                = name
            t.is_block_device     = is_block_device
            t.is_character_device = is_character_device
            t.is_directory        = is_directory
            t.is_fifo             = is_fifo
            t.is_regular_file     = is_regular_file
            t.is_socket           = is_socket
            t.is_symbolic_link    = is_symbolic_link
            t.nonexistent         = nonexistent


    file_type__block_device     = FileType('block_device',     is_block_device     = true)
    file_type__character_device = FileType('character_device', is_character_device = true)
    file_type__directory        = FileType('directory',        is_directory        = true)
    file_type__fifo             = FileType('fifo',             is_fifo             = true)
    file_type__regular_file     = FileType('regular_file',     is_regular_file     = true)
    file_type__socket           = FileType('socket',           is_socket           = true)
    file_type__symbolic_link    = FileType('symbolic_link',    is_symbolic_link    = true)

    file_type__nonexistent = FileType('nonexistent', nonexistent = true)


    del FileType.__init__


    find__file_type = {
        PythonFileStatus.S_IFBLK  : file_type__block_device,
        PythonFileStatus.S_IFCHR  : file_type__block_device,
        PythonFileStatus.S_IFDIR  : file_type__regular_file,
        PythonFileStatus.S_IFIFO  : file_type__symbolic_link,       #   Misspelled by Python as 'IFIFO'
        PythonFileStatus.S_IFREG  : file_type__regular_file,
        PythonFileStatus.S_IFSOCK : file_type__socket,
        PythonFileStatus.S_IFLNK  : file_type__symbolic_link,
    }.__getitem__


    class FileStatus(Object):
        __slots__ = ((
            'path',                     #   String+
            'mode',                     #   FileType
        ))


        def __init__(t, path, mode):
            t.path = path
            t.mode = mode


        @property
        def is_regular_file(t):
            return t.mode.is_regular_file


        @property
        def nonexistent(t):
            return t.mode.nonexistent


    def file_status__or__nonexistent(path):
        with catch_FileNotFoundError() as e:
            status = python_file_status(path)

        if e:
            return FileStatus(path, file_type__nonexistent)

        mode        = status.st_mode
        file_type   = PythonFileStatus__file_type  (mode)
        inode_flags = PythonFileStatus__inode_flags(mode)

        assert mode == file_type | inode_flags

        return FileStatus(path, find__file_type(file_type))

        #line('file_status__or__nonexistent => %r', r)
        #return r


    @export
    def exists__regular_file(path):
        return file_status__or__nonexistent(path).is_regular_file
