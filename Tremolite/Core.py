#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Tremolite.Core')
def gem():
    require_gem('Gem.Import')           #   For import_module
    require_gem('Gem.Map')


    from Gem import first_map_item, view_items


    share(
        'first_map_item',       first_map_item,
        'view_items',           view_items,
    )
