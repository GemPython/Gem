#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@export
def catch_ImportError():
    return CatchException(ImportError)
