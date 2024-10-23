from consts import ALLOWED_TYPE_OPTIONS


def convert_list_to_dict(lst):
    res_dict = {}
    for i in range(0, len(lst), 2):
        res_dict[lst[i]] = lst[i + 1]
    return res_dict

def get_jadn_type_opts(jadn_type_name: str) -> tuple:
    # LEFTOFF HERE
    zzz = ALLOWED_TYPE_OPTIONS.get(jadn_type_name)
    return zzz