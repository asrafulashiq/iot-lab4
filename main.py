import numpy as np
import os
import time
import pickle
import re
# from utils import find_all_level_essid


def find_all_level_essid(text):
    pattern = 'Quality=(\d+)/70[\W]+Signal level=([+-]?\d+) dBm.*\n.*ESSID:"(.*)"'
    reg = re.compile(pattern)
    _dict = {}
    matches = reg.findall(text)
    for match in matches:
        quality, rsi, essid = float(match[0])/70, float(match[1]), match[2]
        if essid == '':
            continue
        if _dict.get(essid, [-float("inf"), -1])[0] < rsi:
            _dict[essid] = (rsi, quality)
    return _dict


def get_vector(dictionary, keys):
    vec = np.zeros(len(keys))
    for i, key in enumerate(keys):
        vec[i] = dictionary[key]
    return vec


def get_vector_and_quality(dictionary, keys):
    vec = np.zeros(len(keys))
    qual_ = np.zeros(len(keys))
    for i, key in enumerate(keys):
        vec[i] = dictionary[key][0]
        qual_[i] = dictionary[key][1]
    return vec, qual_


WIFI_SCAN_CMD = "sudo iwlist wlan0 scan | " +\
    "grep -E ESSID\|Signal\ level"
loc_names = ["G1", "R2", "Y1"]

pickle_file = "./loc_vector.pkl"
with open(pickle_file, "rb") as fp:
    dict_of_loc_essid = pickle.load(fp)
loc_keys = set(dict_of_loc_essid[loc_names[0]].keys())

counter = 1
while True:
    print counter
    scan_rst = os.popen(WIFI_SCAN_CMD).read()
    tmp_dict = find_all_level_essid(scan_rst)
    tmp_keys = set(tmp_dict.keys())
    common_keys = sorted(list(tmp_keys.intersection(loc_keys)))
    pos_vector, qual = get_vector_and_quality(tmp_dict, common_keys)

    min_dis, min_loc = (float("inf"), None)
    for loc in loc_names:
        _vec = get_vector(dict_of_loc_essid[loc], common_keys)
        _dis = np.linalg.norm(np.sqrt(qual) * (_vec - pos_vector))
        if _dis < min_dis:
            min_dis = _dis
            min_loc = loc
    print "Current Location : ", min_loc

    time.sleep(0.1)
    counter += 1
