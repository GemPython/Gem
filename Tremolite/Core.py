#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Tremolite.Core')
def gem():
    require_gem('Gem.Ascii')
    require_gem('Gem.Cache')
    require_gem('Gem.Codec')
    require_gem('Gem.DelayedFileOutput')
    require_gem('Gem.Exception')
    require_gem('Gem.Import')           #   For import_module
    require_gem('Gem.Map')
    require_gem('Gem.Path')
    require_gem('Gem.PortrayString')
    require_gem('Gem.System')


    from Gem import create_DelayedFileOutput, encode_ascii, first_map_item
    from Gem import iterate_items_sorted_by_key, iterate_values_sorted_by_key
    from Gem import lookup_ascii, produce_cache_and_insert_function, python_version, read_text_from_path, view_items


    share(
        #
        #   Imported functions
        #
        'create_DelayedFileOutput',             create_DelayedFileOutput,
        'encode_ascii',                         encode_ascii,
        'first_map_item',                       first_map_item,
        'iterate_items_sorted_by_key',          iterate_items_sorted_by_key,
        'iterate_values_sorted_by_key',         iterate_values_sorted_by_key,
        'lookup_ascii',                         lookup_ascii,
        'produce_cache_and_insert_function',    produce_cache_and_insert_function,
        'read_text_from_path',                  read_text_from_path,
        'view_items',                           view_items,


        #
        #   Values
        #
        'list_of_single_none',  [none],
        'python_version',       python_version,
    )
