import matplotlib
import numpy as np
import matplotlib.pyplot as plt

def Read_OUTCAR(N):
    with open('OUTCAR','r') as outcar:
        outcar_content = outcar.readlines()
    kx = []; ky = []; kz = []
    flag = 'N'
    for line in outcar_content[257:]:
        if 'k-points in units of 2pi/SCALE and weight:' in line:
            flag = 'Y'
            continue
        if 'k-points in reciprocal lattice and weights:' in line:
            flag = 'N'
        if flag == 'Y':
            if line == ' \n':
                continue
            ls = []
            for i in line.strip('\n').strip(' ').split(' '):
                if i != '':
                    ls.append(i)
            kx.append(float(ls[0]))
            ky.append(float(ls[1]))
            kz.append(float(ls[2]))
        if 'E-fermi' in line:
            fermi =[]
            for i in line.strip('\n').split(' '):
                if i != '':
                    fermi.append(i)
            E_fermi = float(fermi[2])
            break
    kx = kx[N:]; ky = ky[N:]; kz = kz[N:]
    k = []
    label_number = [0]
    k.append(0)
    kd = 0  #kd:k-distance
    for i in range(len(kx)-1):
            kd = kd + ((kx[i+1]-kx[i])**2 + (ky[i+1]-ky[i])**2 + (kz[i+1]-kz[i])**2)**0.5
            k.append(2*pi*kd)
            if (kx[i+1]-kx[i])**2 + (ky[i+1]-ky[i])**2 + (kz[i+1]-kz[i])**2 == 0 :
                label_number.append(i)
    return k,label_number,E_fermi


def Read_KPOINTS():
    with open('KPOINTS','r') as kpoints:
        kpoints_content = kpoints.readlines()
    label = []
    if ('line' or 'Line' or 'LINE') in kpoints_content[2]:
        label_raw = []
        line_number = 4
        for line in kpoints_content[4:]:
            line_number += 1
            if line != '\n':
                ls = []
                for i in line.strip('\n').split(' '):
                    if i != '':
                        ls.append(i)
                label_raw.append(ls[-1])
                
        label = []
        label.append(label_raw[0])
        for i in range(len(label_raw)-1):
            if i%2 == 1:
                if label_raw[i] == label_raw[i+1]:
                    label.append(label_raw[i])
                else:
                    label.append(label_raw[i]+ '|' +label_raw[i+1])
        label.append(label_raw[-1])
    return label


def Read_EIGENVAL():
    with open('EIGENVAL','r') as eig:
        eig_content = eig.readlines()
    info = []
    for i in eig_content[5].strip('\n').split(' '):
        if i != '':
            info.append(i)
    global system
    system = eig_content[4].strip('\n').strip(' ')
    totalband = int(info[2])
    totalkpoints = int(info[1])

    ek = [[0.0 for i in range(totalkpoints)] for j in range(totalband)]
    ek = np.array(ek)

    i = 0
    j = 0 
    for line in range(6,len(eig_content)):
        if (line - 5)%(totalband+2) == 1 or (line - 5)%(totalband+2) == 2:
            continue
        e = []
        for each in eig_content[line].strip('\n').split(' '):
            if each != '':
                e.append(float(each))
        ek[i][j] = e[1]
        i += 1
        if (line -5)%(totalband+2) == 0:
            j += 1
            i = 0
    return totalband,totalkpoints,ek


def Write_dat(N,totalkpoints,totalband,k,ek,E_fermi,label,label_number):
    with open('band.dat','w') as f1:
        for band in range(totalband):
            for i in range(totalkpoints-N):
                f1.write('{:>15.7f}{:>15.7f}\n'.format(k[i],ek[band][i+N]-E_fermi))
            f1.write('\n')
    with open('band.gnu','w') as f2:
        f2.write('set terminal  postscript enhanced color font ",30"\n')
        f2.write("set output 'band.eps'\n")
        f2.write('set style data linespoints\n')
        f2.write('unset ztics\n')
        f2.write('unset key\n')
        f2.write('set pointsize 0.8\n')
        f2.write('set view 0,0\n')
        f2.write('set xtics font ",24"\n')
        f2.write('set ytics font ",24"\n')
        f2.write('set ylabel font ",24"\n')
        f2.write('set ylabel "Energy (eV)"\n')
        f2.write('set ylabel offset 1.5,0\n')
        f2.write('set xrange [{}:{:.6f} ]\n'.format(k[0],k[-1]))
        f2.write('set ylabel "Energy (eV)"\n')
        ymin = min(ek[0])-E_fermi
        ymax = max(ek[-1])-E_fermi
        f2.write('set yrange [{:>6}:{:>6}]\n'.format(ymin,ymax))
        f2.write('set xtics (')
        for i in label_number:
            f2.write('"X "  {:.6f},'.format(k[i]))
        f2.write('"X "  {:.6f})\n'.format(k[-1]))
        for i in label_number[1:]:
            f2.write('set arrow from    {0:.6f},  {1:} to    {0:.6f},   {2:} nohead\n'.format(k[i],ymin,ymax))
        f2.write("plot 'band.dat' u 1:2  w lp lw 2 pt 7  ps 0.2 lc rgb 'black', 0 w l lw 2")

        
def Plot(N,totalkpoints,totalband,k,ek,E_fermi,label,label_number):
    fig, ax = plt.subplots()
    for band in range(totalband):
        ax.plot(k,ek[band][N:]-E_fermi,color= 'k')
    ax.set_xlim(k[0],k[-1])
    plot_range = eval(input('请输入能带画图范围,例如:-2,2:'))
    ax.set_ylim(plot_range[0],plot_range[1])
    for i in label_number:
        ax.axvline(k[i],linewidth = 0.5,color = 'k')
    ax.axhline(0,linewidth = 0.3,color = 'k')
    label_number.append(totalkpoints-1-N)
    ticks = [k[i] for i in label_number]
    ax.set_xticks(ticks)
    ax.set_xticklabels(label)
    ax.tick_params(direction='in')
    fig.savefig('{}_band'.format(system) + '.png')
    plt.show()

                
def main():
    global pi
    pi = 3.1415926535897932
    response0 = input('是否扣掉能带路径前段,y or n ?')
    if response0 == 'y':
        N = eval(input('扣掉能带路径前段k点数N = '))
    else:
        N = 0
    k,label_number,E_fermi = Read_OUTCAR(N)
    label = Read_KPOINTS()
    totalband,totalkpoints,ek = Read_EIGENVAL()
    print('该体系({0:})能带计算有{1:}个k点,{2:}条能带.'.format(system,totalkpoints,totalband))

    response1 = input('是否手动设置费米能级,y or n?')
    if response1 == 'y':
        E_fermi = eval(input('请输入费米能级:'))
        
    Write_dat(N,totalkpoints,totalband,k,ek,E_fermi,label,label_number)
    response2 = input('能否在图形界面显示能带图形,y or n ?')
    if  response2 == 'y':
        Plot(N,totalkpoints,totalband,k,ek,E_fermi,label,label_number)
    else:
        print('无法直接绘制能带!!!\n请采用gnuplot命令操作生成的gnu文件绘制能带!!!')
main()
