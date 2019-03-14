import os
import time

WIFI_SCAN_CMD = "sudo iwlist wlan0 scan | " +\
        "grep -E ESSID\|Signal\ level"
location = "R2"
os.mkdir(location)
counter = 1
max_count = 70
while True:
    print counter
    scan_rst = os.popen(WIFI_SCAN_CMD).read()
    fname = os.path.join(location, "{}.txt".format(counter))
    with open(fname, "w") as fp:
        fp.write(scan_rst)
    time.sleep(0.5)
    counter += 1
    if counter >= max_count:
        break
