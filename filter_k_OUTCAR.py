########## 从OUTCAR 提取分数坐标k点 ############
def kxkykz():
    with open('OUTCAR','r') as outcar:
        outcar_content = outcar.readlines()
    with open('kpoints','w') as kpoints:
        flag = 'N'
        for line in outcar_content:
            if 'k-points in reciprocal lattice and weights:' in line:
                flag = 'Y'
                continue
            if 'position of ions in fractional coordinates' in line:
                flag = 'N'
                break
            if flag == 'Y':
                kpoints.write(line.replace('    0.006','     0'))
kxkykz()
