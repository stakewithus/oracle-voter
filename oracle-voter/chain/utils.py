from collections import OrderedDict


def LexiSortDict(payload):
    d = OrderedDict()
    # Sort The Keys
    sorted_keys = sorted(payload.keys())
    for k in sorted_keys:
        # Check the Value is Not a Dict
        v = None
        if isinstance(payload[k], dict):
            v = LexiSortDict(payload[k])
        elif isinstance(payload[k], list):
            v = list()
            for subv in payload[k]:
                if isinstance(subv, dict):
                    vs = LexiSortDict(subv)
                    v.append(vs)
                else:
                    v.append(subv)
        else:
            v = payload[k]
        d[k] = v
    return d
