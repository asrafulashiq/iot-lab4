import numpy as np
import os
import time
import pickle
from utils import find_all_level_essid


def get_vector(dictionary, keys):
    vec = np.zeros(len(keys))
    for i, key in enumerate(keys):
        vec[i] = dictionary[key]
    return vec

WIFI_SCAN_CMD = "sudo iwlist wlan0 scan | " +\
    "grep -E ESSID\|Signal\ level"
loc_names = ["G1", "R2", "Y1"]

pickle_file = "./loc_vector_mean.pkl"
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
    pos_vector = get_vector(tmp_dict, common_keys)

    min_dis, min_loc = (float("inf"), None)
    for loc in loc_names:
        _vec = get_vector(dict_of_loc_essid[loc], common_keys)
        _dis = np.linalg.norm(_vec - pos_vector)
        if _dis < min_dis:
            min_dis = _dis
            min_loc = loc
    print "Current Location : ", min_loc

    time.sleep(0.1)
    counter += 1
