#!/usr/bin/env python

# Note: This script runs w1fit3kAl1 from within a cloned git repo.
# The script `bin/wifite` is designed to be run after installing (from /usr/sbin), not from the cwd.
import os
os.system('perl airmon/airmon.pl')
from wifite import __main__
__main__.entry_point()
os.system('bash airmon/reload_net.sh')
