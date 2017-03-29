#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.Codec')
def gem():
    require_gem('Gem.Import')


    PythonCodec         = import_module('codecs')
    python_encode_ascii = PythonCodec.getencoder('ascii')


    @export
    def encode_ascii(s):
        return python_encode_ascii(s)[0]
