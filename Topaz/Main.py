#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
def boot(module_name):
    def execute(f):
        return f()

    return execute


@boot('Boot')
def boot():
    from sys     import path    as module_path
    from os.path import abspath as path_absolute, join as path_join

    module_path.insert(1, path_absolute(path_join(module_path[0], '..')))


    import Gem


@gem('Topaz.Main')
def gem():
    require_gem('Gem.RawString')


    from Gem import portray_raw_string, raise_value_error


    @share
    def main():
        for [s, expected] in [
                [   r'',                            "r''"                               ],

                #
                #       0 = no ' or " seen
                #
                [   r'test',                        "r'test'"                           ],  #   0,0,0


                #
                #       1 = saw a '
                #       11 = last saw '
                #       12 = last saw ''
                #
                [   r"can't",                       '''r"can't"'''                      ],  #   1,0,-1
                [   r"'",                           '''r"'"'''                          ],  #   1,11,-1
                [   r"quoted: ''",                  '''r"quoted: ''"'''                 ],  #   1,12,-2

                #
                #       2 = saw a "
                #       9  = last saw "
                #       10 = last saw ""
                #
                [   r'She said "hello"',            """r'She said "hello"'"""           ],  #   2,9,2
                [   r'"',                           """r'"'"""                          ],  #   2,9,1
                [   r'double quoted: ""',           """r'double quoted: ""'"""          ],  #   2,10,2

                #<special-cases>
                #
                #   Begin with " & has ''' internally
                #
                [   '''"triple" is: ''\'.''',       portray('''"triple" is: ''\'.''')   ],  #   5,0,-1
                #
                #   End with " & has ''' internally
                #
                [   '''three: "''\'."''',           portray('''three: "''\'."''')       ],  #   5,9,-1
                #
                #   Begin with ' & has """ internally
                #
                [   """'triple' is: ""\".""",       portray("""'triple' is: ""\".""")   ],  #   7,0,1
                #
                #   End with ' & has """ internally
                #
                [   """3: '""\".'""",               portray("""3: '""\".'""")           ],  #   7,11,1
                #</special-cases>

                #
                #       3  = saw a ' & a "
                #       9  = last saw "
                #       10 = last saw ""
                #       11 = last saw '
                #
                [   r'''the quotes: ' & "''',       """r'''the quotes: ' & "'''"""      ],  #   3,9,0
                [   r'''singles "'" & "''"''',      """r'''singles "'" & "''"'''"""     ],  #   3,9,1
                [   r'''more quotes: '' & ""''',    """r'''more quotes: '' & ""'''"""   ],  #   3,10,0
                [   r"""other way: " & '""",        '''r"""other way: " & '"""'''       ],  #   3,11,1
                [   r"""prefer ", "", ', or ''""",  '''r"""prefer ", "", ', or ''"""''' ],  #   3,12,0
                [   r"""single: ', '' .vs. "?""",   '''r"""single: ', '' .vs. "?"""'''  ],  #   3,0,-2
        ]:
            actual = portray_raw_string(s)

            if actual != expected:
                raise_value_error('portray_raw_string(%r): %r (expected: %r)', s, actual, expected)
