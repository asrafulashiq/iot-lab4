import numpy as np
import os
import time
import pickle
from utils import find_all_level_essid

WIFI_SCAN_CMD = "sudo iwlist wlan0 scan | " +\
    "grep -E ESSID\|Signal\ level"
loc_names = ["G1", "R2", "Y1"]

pickle_file = "./loc_vector.pkl"
with open(pickle_file, "rb") as fp:
    dict_of_loc_essid = pickle.load(fp)

keys = set(dict_of_loc_essid[loc_names[0]].keys())

counter = 1
while True:
    print counter
    scan_rst = os.popen(WIFI_SCAN_CMD).read()
    tmp_dict = find_all_level_essid(scan_rst)
    tmp_keys = set(tmp_dict.keys())
    common_keys = tmp_keys.intersection(keys)
    time.sleep(0.1)
    counter += 1
