import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/yasin/turtlesim_ws/src/install/turtlesim_py_pkg'
