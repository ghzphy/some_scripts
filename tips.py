import os
ispin = os.popen('grep ISPIN OUTCAR').read().split()[2]

### other case
import subprocess
A = subprocess.getoutput('grep band PROCAR')
