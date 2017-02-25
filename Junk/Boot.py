#
#   Copyright (c) 2017 Amit Green
#
if 0:
    import Gem, sys as PythonSystem


    none                  = Gem.BuiltIn.none
    flush_standard_output = PythonSystem.stdout.flush
    write_standard_output = PythonSystem.stdout.write


    def line(format = none, *arguments):
        if format is none:
            assert length(arguments) is 0

            write_standard_output('\n')
        else:
            write_standard_output((format % arguments   if arguments else   format) + '\n')

        flush_standard_output()



    Gem_keys     = sorted(Gem.__dict__.keys())
    BuiltIn_keys = sorted(Gem.BuiltIn.__dict__.keys())

    line('Gem:                   %s',        Gem_keys)
    line('BuiltIn:               %s',    BuiltIn_keys)

    line('Shared: [- exported]:  %s',
          sorted(k   for k in Gem.Shared.__dict__.keys()   if k not in Gem_keys))

    line('Privileged:            %s', sorted(Gem.Shared.Privileged.__dict__.keys()))
