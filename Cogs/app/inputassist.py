import pykakasi
from neologdn import normalize
from difflib import SequenceMatcher as sm
from romkan import to_roma


def hyokiyure(sinput: str, slist: list) -> list:
    kakasi = pykakasi.kakasi()
    kakasi.setMode(fr="J", to="H")
    conv = kakasi.getConverter()
    anslist = [
        [],
        [],
        [],
        [],
        [],
    ]
    converted_slist = [to_roma(normalize(conv.do(s))) for s in slist]
    sinput = to_roma(normalize(conv.do(sinput)))
    for s in converted_slist:
        rate = sm(None, sinput, s).ratio()
        if rate >= 0.6:
            anslist[10 - int(rate * 10)].append(s)
    return anslist
