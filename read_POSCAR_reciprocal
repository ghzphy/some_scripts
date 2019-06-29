##读取 POSCAR 文件, 输出原胞基矢以及倒格矢基矢.2019年4月3日.
def Write(filepath):
    try:
        with open(filepath,'r',encoding = 'utf-8') as f:
            content = f.readlines()
    except:
        print('POSCAR不存在或文件名错误!')
    line1 = content[0].strip('\n')
    print('{0:-^73}'.format('该体系为:'+ line1)+'\n')
    line3 = content[2].split(' ')
    line4 = content[3].split(' ')
    line5 = content[4].split(' ')
    a1_line = []
    a2_line = []
    a3_line = []
    for i in line3:
        if i != '':
            a1_line.append(i)
    for i in line4:
        if i != '':
            a2_line.append(i)
    for i in line5:
        if i != '':
            a3_line.append(i)
    a11 = float(a1_line[0])
    a12 = float(a1_line[1])
    a13 = float(a1_line[2])

    a21 = float(a2_line[0])
    a22 = float(a2_line[1])
    a23 = float(a2_line[2])
    
    a31 = float(a3_line[0])
    a32 = float(a3_line[1])
    
    a33 = float(a3_line[2])

    print('{0:*^73}'.format(' 原胞基矢 a1,a2,a3 '))
    print('a1 = {:0<15}*i + {:0<15}*j + {:0<15}*k'.format(a11,a12,a13))
    print('a2 = {:0<15}*i + {:0<15}*j + {:0<15}*k'.format(a21,a22,a23))
    print('a3 = {:0<15}*i + {:0<15}*j + {:0<15}*k'.format(a31,a32,a33))

    b11 = a22*a33 - a32*a23
    b12 = -a21*a33 + a31*a23
    b13 = a21*a32 - a22*a31

    b21 = a32*a13 - a12*a33
    b22 = -a31*a13 + a11*a33
    b23 = a31*a12 - a11*a32

    b31 = a12*a23 - a22*a13
    b32 = -a11*a23 + a21*a13
    b33 = a11*a22 - a21*a12


    V = b31*a31 + b32*a32 + b33*a33
    print('原胞体积为:{0:.7f} A^3.'.format(V))
    pi = 3.14159265358979
    print('\n')
    print('{0:*^71}'.format(' 倒格矢 b1,b2,b3(没乘以2pi)'))
    print('b1 = {:0<20}*i + {:0<20}*j + {:0<20}*k'.format(b11/V,b12/V,b13/V))
    print('b2 = {:0<20}*i + {:0<20}*j + {:0<20}*k'.format(b21/V,b22/V,b23/V))
    print('b3 = {:0<20}*i + {:0<20}*j + {:0<20}*k'.format(b31/V,b32/V,b33/V))
    print('\n')
    print('{0:*^74}'.format(' 倒格矢 b1,b2,b3 '))
    print('b1 = {:0<20}*i + {:0<20}*j + {:0<20}*k'.format(b11*2*pi/V,b12*2*pi/V,b13*2*pi/V))
    print('b2 = {:0<20}*i + {:0<20}*j + {:0<20}*k'.format(b21*2*pi/V,b22*2*pi/V,b23*2*pi/V))
    print('b3 = {:0<20}*i + {:0<20}*j + {:0<20}*k'.format(b31*2*pi/V,b32*2*pi/V,b33*2*pi/V))
   
filepath = 'F:\\研究生\\vasp\\MiBiTe\\POSCAR'
Write(filepath)
