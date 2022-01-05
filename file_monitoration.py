import os

from utils import convert_url, reading_json, retun_md


def plan_is_change(conf):
    now = os.path.getmtime(convert_url("./scan.xlsx"))
    
    in_base = reading_json(convert_url("./config/monitoration"))

    if in_base["scan"] == now:
        return False
    else:
        return True


def folder_is_change():

    in_base = reading_json(convert_url('./config/folders'))
    
    list_items = list()

    for ibase in in_base:
        for box in ibase["boxs"]:
            for key, value in box.items():
                if not retun_md(convert_url(f'./{ibase["index"]}/{key}')) == value:
                    list_items.append({
                        "index": ibase["index"],
                        "box": key
                    })
    
    if len(list_items):
        return True, list_items
    else:
        return False, list_items