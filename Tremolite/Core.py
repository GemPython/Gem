#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Tremolite.Core')
def gem():
    require_gem('Gem.Codec')
    require_gem('Gem.Exception')
    require_gem('Gem.Import')           #   For import_module
    require_gem('Gem.Map')


    from Gem import encode_ascii, first_map_item, iterate_items_sorted_by_key, view_items


    share(
        #
        #   Imported functions
        #
        'encode_ascii',                 encode_ascii,
        'first_map_item',               first_map_item,
        'iterate_items_sorted_by_key',  iterate_items_sorted_by_key,
        'view_items',                   view_items,


        #
        #   Values
        #
        'list_of_single_none',  [none],
    )
