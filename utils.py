import json, sys

def get_private_res(*args, **kwargs):
    """
    Gets value from private_resources.json when arbitrary set of args are given
    i.e. get_private_res("people", "places", "things") would return 
    """
    with open("private_resources.json", 'r') as jdb:
        # json_db = jdb.read()
        json_db = json.load(jdb)
    # breakpoint()
    try:
        init_item = json_db[(args)[0]]
        remain_args = (args)[1:]
        desired_item = None
        for arg in remain_args:
            desired_item = init_item[arg]
            init_item = desired_item
    except IndexError:
        desired_item = init_item
        pass
    except KeyError:
        print("Item not in private resources file.")
        sys.exit(1)
    if desired_item == None:
        desired_item = init_item
    return desired_item