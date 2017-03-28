#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.Map')
def gem():
    #
    #   view_items
    #       Access the .viewitems method of a Map.
    #
    #       (Deals with the annoyance of .viewitems method named .viewitems in python 2.0, but .items in
    #       python 3.0)
    #
    view_items = (Map.viewitems   if is_python_2 else  Map.items)


    if is_python_2:
        @export
        def first_map_item(mapping):
            return iterate(view_items(mapping)).next()
    else:
        @export
        def first_map_item(mapping):
            return iterate(view_items(mapping)).__next__()


    @export
    def iterate_items_sorted_by_key(mapping):
        value = mapping.__getitem__

        for k in sorted_list(mapping):
            yield (( k, value(k) ))


    @export
    def values_tuple_sorted_by_key(mapping):
        value = mapping.__getitem__

        return Tuple(value(k)   for k in sorted_list(mapping))


    export(
        'view_items',   view_items,
    )
