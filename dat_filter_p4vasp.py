### p4vasp生成dat文件 改用python作图，需要读取dat数据#######
filepath = 'MnBi.dat'
with open(filepath,'r') as f:
    content = f.readlines()

k = []
E = []

kpoints = 0
for line in content:
    kpoints += 1
    if line == '\n':
        break

for line in content:
    if line != '\n':
        k.append(float(line.strip('\n').strip(' ').split(' ')[0]))
        E.append(float(line.strip('\n').strip(' ').split(' ')[-1]))
print('每条能带有 {} 个k点'.format(kpoints - 1))
print('有 {} 条能带'.format(len(k)/(kpoints - 1)))

for band in range(203,207):
    band_k = np.array(k[(kpoints-1)*band:(kpoints-1)*(band+1)])
    band_E = np.array(E[(kpoints-1)*band:(kpoints-1)*(band+1)])
    plt.plot(band_k,band_E)
plt.show()
