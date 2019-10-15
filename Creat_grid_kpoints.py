#####k点撒点####
import numpy as np

s = 0.03
N = 25
a = np.linspace(-s,s,N)
b = []
for i in list(a):
    b.append('{0: >7}  {1:}'.format(str(-s),float(i))+'   0.0000' + '\n')
    b.append('{0: >7}  {1:}'.format(str(s),float(i)) + '   0.0000'+'\n\n')
with open('KPOINTS','w') as f2:
    f2.write('k-points along high symmetry lines\n')
    f2.write('{}'.format(N) + '\n')
    f2.write('Line-mode\nC\n')
    for i in b:
        f2.write(i)
