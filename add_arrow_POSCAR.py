#对POSCAR的某一列都加上某个值
with open('POSCAR_WTe_010_10','r') as f1:
    content = f1.readlines()

with open('POSCAR_WTe_new_010','w') as f2:
    for line in content[0:8]:
        f2.write(line)
    x=[]
    y=[]
    z=[]
    for line in content[8:]:
        ls = []
        for i in line.strip('\n').split(' '):
            if i != '':
                ls.append(i)
        x.append(float(ls[0]))
        y.append(float(ls[1]))

        z.append(float(ls[2]))
    new_y = []
    for i in y:
        new_y.append(i+7)
    for i in range(len(x)):
        f2.write('{0:>21}{1:>21}{2:>21}'.format(x[i],new_y[i],z[i])+'\n')
