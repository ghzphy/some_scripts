############################################### 需要EIGENVAL, OUTCAR,以及上一步scf的OUTCAR#################################
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

def kxkykz():
    global E_fermi
    with open('OUTCAR','r') as outcar:
        outcar_content = outcar.readlines()
    kx = []; ky = []; kz = []
    flag = 'N'
    for line in outcar_content:
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
    kx,ky,kz = kx[:],ky[:],kz[:]
    return kx,ky,kz


def Read_scf_Fermi():
    with open('../OUTCAR','r') as outcar:
        outcar_content = outcar.readlines()
    for line in outcar_content:
        if 'E-fermi' in line:
            fermi =[]
            for i in line.strip('\n').split(' '):
                if i != '':
                    fermi.append(i)
            E_fermi = float(fermi[2])
            break
    return E_fermi

def Read_nonscf_Fermi():
    with open('OUTCAR','r') as outcar:
        outcar_content = outcar.readlines()
    for line in outcar_content:
        if 'E-fermi' in line:
            fermi =[]
            for i in line.strip('\n').split(' '):
                if i != '':
                    fermi.append(i)
            E_fermi = float(fermi[2])
            break
    return E_fermi

def ReadKPOINTS():
    with open('KPOINTS','r') as kpoints:
        kpoints_content = kpoints.readlines()
    each = float(kpoints_content[1].strip('\n').strip(' '))
    label = []
    for line in kpoints_content[4:]:
        linelist = []
        if line != '\n':
            for i in line.strip('\n').split(' '):
                if i != '':
                    linelist.append(i)
            try:
                label.append(linelist[-1])
            except:
                print('KPOINTS文件里的空行存在空格,请最好删除里面的空格!')
            
    label_new = []
    label_new.append(label[0])
    for i in range(len(label)-1):
        if i%2 == 1:
            if label[i] == label[i+1]:
                label_new.append(label[i])
            else:
                label_new.append(label[i]+ '|' +label[i+1])
    label_new.append(label[-1])
#    print(label_new)
    return each,label_new

def kd():
    #each,label_new = ReadKPOINTS()
    kx,ky,kz= kxkykz()
    k = []
    k.append(0)
    kd = 0  #kd:k-distance
    for i in range(len(kx)):
        flag = 'T'
        if i <= (len(kx)-2):
            kd = kd + ((kx[i+1]-kx[i])**2 + (ky[i+1]-ky[i])**2 + (kz[i+1]-kz[i])**2)**0.5
            if (i+1)%each == 0:
                if ((kx[i+1]-kx[i])**2 + (ky[i+1]-ky[i])**2 + (kz[i+1]-kz[i])**2)**0.5 != 0:
                    flag = 'F'
            if flag == 'T':
                k.append(kd)
            else:
                k.append(kd -((kx[i+1]-kx[i])**2 + (ky[i+1]-ky[i])**2 + (kz[i+1]-kz[i])**2)**0.5)
                kd = kd -((kx[i+1]-kx[i])**2 + (ky[i+1]-ky[i])**2 + (kz[i+1]-kz[i])**2)**0.5
    return k

def Readeigval():
    with open('EIGENVAL','r') as eig:
        eig_content = eig.readlines()
    info = []
    for i in eig_content[5].strip('\n').split(' '):
        if i != '':
            info.append(i)
    global system
    global totalband
    system = eig_content[4].strip('\n').strip(' ')
    totalband = int(info[2])
    return eig_content,info
    
def SelectBand(band):
    eig_content,info =Readeigval()
    ek = []
    for i in range(6,len(eig_content)):
        if (i-7)%(int(info[2])+2) == band:
            e = []
            for each in eig_content[i].strip('\n').split(' '):
                if each != '':
                    e.append(float(each))
            ek.append(e[1])
    return ek

def Plot(E_fermi):
    ek = SelectBand(band)[:]#######
    ek = np.array(ek)
    #plt.plot(k,ek-E_fermi,linewidth = 1,color= 'k')
    plt.plot(k,ek-E_fermi,color= 'k')

def main():
    eig_content,info = Readeigval()

    global each
    global label_new
    each,label_new= ReadKPOINTS()
    print('该体系({0:})有{1:}个价电子,{2:}个k点,{3:}条能带.'.format(eig_content[4].strip('\n').strip(' '),info[0],info[1],info[2]))

    global k
    k = kd()
    fig,ax= plt.subplots()

    response = input('是否手动设置费米能级,y or n ?')
    if  response == 'y':
        E_fermi = eval(input('请输入费米能级:'))
    elif response == 'n':
        response1 = input('采用scf(1)或者nonscf(2)时的费米能级,1 or 2?')
        if response1 == '1':
            E_fermi = Read_scf_Fermi()
        else:
            E_fermi = Read_nonscf_Fermi()
    global band
    for band in range(1,totalband+1):
        SelectBand(band)
        Plot(E_fermi)
        
    ax.set_ylabel('Energy (eV)')
    ax.set_xlim(k[0],k[-1])

    plot_range = eval(input('请输入能带画图范围,例如:-2,2: '))
    ax.set_ylim(plot_range[0],plot_range[1])
    ax.set_title(system)
    
    ticks = [0]
    for i in range(len(k)):
        if (i+1)%each == 0:
            ax.axvline(k[i],linewidth = 0.5,color = 'k')
            ticks.append(k[i])
    ax.axhline(0,linewidth = 0.3,color = 'k')

    ax.set_xticks(ticks)
    k_label = label_new
    #k_label= [r'B',r'$\Gamma$',r'Y',r'H',r'A',r'M',r'B',r'Z',r'$\Gamma$',r'X']
    ax.set_xticklabels(k_label)
    ax.tick_params(direction='in')
    
    fig.savefig('{}_band'.format(system) + '.png')
    plt.show()
main()
