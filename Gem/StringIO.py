#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.StringIO')
def gem():
    require_gem('Gem.Import')


    if is_python_2:
        StringIO = import_module('cStringIO').StringIO
    else:
        StringIO = import_module('_io').StringIO


    @export
    def create_StringOutput():
        return StringIO()
