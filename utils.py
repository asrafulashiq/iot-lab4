import os
import re
import numpy as np
from collections import defaultdict
import pickle


def find_all_level_essid(text):
    pattern = 'Signal level=([+-]?\d+) dBm.*\n.*ESSID:"(.*)"'
    reg = re.compile(pattern)
    _dict = {}
    matches = reg.findall(text)
    for match in matches:
        rsi, essid = float(match[0]), match[1]
        if essid == '':
            continue
        if _dict.get(essid, -float("inf")) < rsi:
            _dict[essid] = rsi
    return _dict


def get_dict_for_loc(fldr, is_write=True):
    dict_rsi = defaultdict(list)
    for fname in os.listdir(fldr):
        if not fname.endswith("txt"):
            continue
        fname = os.path.join(fldr, fname)
        with open(fname) as fp:
            text = fp.read()
            tmp_dict = find_all_level_essid(text)
            for key in tmp_dict:
                dict_rsi[key].append(tmp_dict[key])
            if is_write:
                fwrite = "combined/{}.pkl".format(fldr)
                with open(fwrite, "wb") as fw:
                    pickle.dump(dict_rsi, fw)
    m_dict = {}
    for k, v in dict_rsi.iteritems():
        m_dict[k] = np.max(v)
    return m_dict


if __name__ == "__main__":
    loc_names = ["G1", "R2", "Y1"]
    dict_of_loc_essid = {}
    keys = []
    for loc in loc_names:
        dict_of_loc_essid[loc] = \
            get_dict_for_loc(loc)
        keys.append(set(dict_of_loc_essid[loc].keys()))

    # get dict with common keys
    dict_of_loc_essid_common = {}
    common_keys = set.intersection(*keys)
    for loc in loc_names:
        dict_of_loc_essid_common[loc] = \
            {k: dict_of_loc_essid[loc][k] for k in common_keys}

    fwrite = "loc_vector_max.pkl".format(loc)
    with open(fwrite, "wb") as fw:
        pickle.dump(dict_of_loc_essid_common, fw)

