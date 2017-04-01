#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Sapphire.Parse')
def gem():
    @share
    def parse_python_from_path(path):
        data = read_text_from_path('../Sapphire/Main.py')

        for s in data.splitlines():
            line(s)
