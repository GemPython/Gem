@export
def catch_ImportError():
    return CatchException(ImportError)
