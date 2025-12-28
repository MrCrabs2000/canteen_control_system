from json import loads, dumps



def json_to_str(json_text):
    text, a, res = loads(json_text), 1, ''
    for key in text.keys():
        if a == len(text):
            res += text[key]
        else:
            res += text[key] + ' '
            a += 1
    return res


def str_to_json(text):
    text = text.strip().split()
    res = {}
    for i in range(len(text)):
        res[str(i)] = text[i]
    return dumps(res)