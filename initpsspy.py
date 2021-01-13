# add PSS/E path to python
import pssepath
pssepath.add_pssepath()

# import all psspy functions
from psspy import *

# redirect PSS/E alerts/messages to python command line
import redirect
redirect.psse2py()

# declare 'with mute:' block to silent PSS/E alerts
import os
from contextlib2 import redirect_stdout
mute = redirect_stdout(open(os.devnull, 'w'))

# initialize PSS/E
with mute:
    psseinit()

def read_raw_file(raw_file_name, numnam=0):
    with mute:
        _, major, _, _, _, _ = psseversion()
        versions = [str(n) for n in range(major, 14, -1)]
        for ver in versions:
            readrawversion(numnam=numnam, vernum=ver, ifile=raw_file_name)
            ierr = check_powerflow_data(0, 1, 0)
            if ierr == 0:
                return 0
    return -1
