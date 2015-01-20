#!/usr/bin/env python3

from common import load_obj, edit_cls, expr, expr_type, expr_type_multi


def main():
    load_obj()

    edit = edit_cls('PKMain2')
    edit.find_method_def('onCreate')
    edit.find_line(r' invoke-super .*', 'down,in_method')
    edit.prepare_to_insert()
    edit.add_line(' sput-object p0, Lblind/pk/mod/Entry;->pk:Lcom/silvermoon/client/PKMain2;')
    edit.save()

    edit = edit_cls('GameController')
#    edit.mod_method_def('performAction', 'public')
    edit.prepare_after_prologue('selectMapElementsAction')
    edit.add_invoke_entry('autoPickAction', 'p0, p1', 'v2')
    edit.add_ret_if_result(True)
    edit.save()

if __name__ == '__main__':
    main()
