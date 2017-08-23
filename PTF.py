from __future__ import division
import numpy as np
import os
import math
import ImageToolKit
from matplotlib import pyplot as plt
data_dir = 'C:\\Users\\lneat\\Documents\\TestbedData\\PSF_Gen'


ptc_dict = {'FileNames': [],'Raw DN':[],'Offset':[], 'Signal':[], 'Total Noise':[], 'Delta Noise':[], 'Shot Noise':[], 'FPN':''}

x = 100
y = 100
print(ptc_dict['FileNames'])

for file in os.listdir(data_dir):
    if(file.endswith('.fits')):
        ptc_dict['FileNames'].append(file)
        imgs = ImageToolKit.extract_fits_data_cube(data_dir + '\\' + file)
        img1 =  imgs[0][:][:]
        img2 = imgs[1][:][:]
        total = 0
        for i in range(0, x):
            for j in range(0, y):
                total = (img1[i][j]) + total
        ptc_dict['Raw DN'].append(total)
        ptc_dict['Offset'].append(0)

counter = 0
for file in os.listdir(data_dir):
    if(file.endswith('.fits')):
        ptc_dict['Signal'].append((ptc_dict['Raw DN'][counter])/(x*y) - ptc_dict['Offset'][counter])
        counter = counter + 1


counter = 0
for file in os.listdir(data_dir):
        if (file.endswith('.fits')):
            imgs = ImageToolKit.extract_fits_data_cube(data_dir + '\\' + file)
            img1 = imgs[0][:][:]
            img2 = imgs[1][:][:]
            total = 0
            for i in range(0, x):
                for j in range(0, y):
                    total = (img1[i][j] - img2[i][j]) ** 2 + total
            ptc_dict['Total Noise'].append(math.sqrt(total / (x * y)))
            print('\n')
            print(ptc_dict['Signal'][counter])
            print(ptc_dict['Total Noise'][counter])
            print('\n')
            counter = counter + 1

print(ptc_dict)





"""
for file in os.listdir(data_dir):
    if(file.endswith('.fits')):
        print(file)
        imgs = ImageToolKit.extract_fits_data_cube(data_dir + '\\' + file)
        x,y = imgs[0].shape
        x = 50
        y = 50
        img1 =  imgs[0][:][:]
        img2 = imgs[1][:][:]
        mean1 = img1.mean()
        mean2 = img2.mean()
        xaxis.append((mean1+mean2)/2)
        total = 0
        print(mean1)
        for i in range(0, x):
            for j in range(0, y):
                total = ((img1[i][j]-mean1)-(img2[i][j]-mean2)) ** 2 + total
        var.append(math.sqrt(total/(2*x*y)))
"""

w = ptc_dict['Signal'][0:40]
p = ptc_dict['Total Noise'][0:40]
z = np.polyfit(w,p,1)
f = np.poly1d(z)

x_new = np.linspace(0, w[-1], 50)
y_new = f(x_new)
plt.xscale('log')
plt.yscale('log')
plt.plot(w,p,'o', x_new, y_new)
plt.show()



plt.xscale('log')
plt.yscale('log')
plt.xlabel('DN Signal', fontsize=20)
plt.ylabel('DN Noise', fontsize=20)
plt.title('Andor iXon 888 EMCCD PTC', fontsize=25)
plt.plot(ptc_dict['Signal'],ptc_dict['Total Noise'], '.', c='r')
fontsize = 14
ax = plt.gca()

for tick in ax.xaxis.get_major_ticks():
    tick.label1.set_fontsize(fontsize)
    tick.label1.set_fontweight('bold')
for tick in ax.yaxis.get_major_ticks():
    tick.label1.set_fontsize(fontsize)
    tick.label1.set_fontweight('bold')
plt.rc('axes', linewidth=2)
plt.xlabel('DN Signal', fontsize=16, fontweight='bold')
plt.ylabel('DN Noise', fontsize=16, fontweight='bold')
plt.show()