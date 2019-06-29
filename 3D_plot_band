############################################# 绘制三维能带 ##########################################################
########################################### 只需要读取EIGENVAL,OUTCAR 文件###########################################
#######################################  kx,ky 点数目一定得是 n^2 个 ################################################

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

def kxkykz():
    with open('OUTCAR','r') as outcar:
        outcar_content = outcar.readlines()
    kx = []; ky = []; kz = []
    flag = 'N'
    for line in outcar_content:
        if 'k-points in units of 2pi/SCALE and weight:' in line:
            flag = 'Y'
            continue
        if 'k-points in reciprocal lattice and weights:' in line:
            break
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

def ReadFermi():
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
    eig_content,info=Readeigval()
    ek = []
    for i in range(6,len(eig_content)):
        if (i-7)%(int(info[2])+2) == band:
            e = []
            for each in eig_content[i].strip('\n').split(' '):
                if each != '':
                    e.append(float(each))
            ek.append(e[1])
    return ek

def Plot3D(fig,kx,ky,kz,E_fermi=0):
    E = SelectBand(band)

    X = np.array(kx).reshape((int(len(E)**0.5),int(len(E)**0.5)))
    Y = np.array(ky).reshape((int(len(E)**0.5),int(len(E)**0.5)))
    Z = np.array(E).reshape((int(len(E)**0.5),int(len(E)**0.5))) - E_fermi

    ax = fig.gca(projection = '3d')
    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap = 'rainbow',linewidth = 0, antialiased = False)
    # Customize the z axis.
    #ax.set_zlim(-0.3, 0.3)
    #ax.zaxis.set_major_locator(LinearLocator(10))
    #ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
     
    # Add a color bar which maps values to colors.
    #fig.colorbar(surf, shrink=0.5, aspect=5)

def main():
    kx,ky,kz = kxkykz()
    E_fermi = ReadFermi()
    eig_content,info = Readeigval()
    print('该体系({0:})有{1:}个价电子,{2:}个k点,{3:}条能带.'.format(eig_content[4].strip('\n').strip(' '),info[0],info[1],info[2]))
    fig,ax= plt.subplots()
    global band
    for band in range(245,248):
        print('绘制第{}条能带'.format(band))
        SelectBand(band)
        Plot3D(fig,kx,ky,kz,E_fermi)
    plt.show()

if __name__ == '__main__':
    main()
