import sys
import os
import spider_mkii

os.environ['PYUSB_DEBUG'] = 'critical'

# TODO Get these from a configuration file
amp = spider_mkii.SpiderMKii(0x0E41, 0x5056)

# Get preset 0
data = amp.getSelection(0)

# read forever
while True:
    success, data = amp.read()
    if success:
        # special case where we need more data
        if data[0] == 52 and data[1] == 240:
            while len(data) < 20:
                _, more = amp.read()
                data.extend(more)
            
        amp.handleIncomingData(data)