import pandas as pd
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cbook import get_sample_data
from matplotlib.ticker import FuncFormatter

mypath = 'C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/DADOS'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

mort = []
est = []
for i in onlyfiles:
    FILE = i
    data = pd.read_csv(mypath+'/'+FILE, header = 0, sep = ";")
    date_rng = data[["DateRep"]].values
    mortality = data["cum-Deaths"].values[-1:]/data["cum-Cases"].values[-1:]
    mort.append(mortality)
    est.append(FILE[9:-4])
    
mort =np.array(mort)    
est = np.array(est)

df = pd.DataFrame(mort, columns = ["mortalidade"])
df["estado"] = est
df = df.sort_values(by = ["mortalidade"])


fig, ax = plt.subplots(1, 1)

im_ufpe = plt.imread(get_sample_data('C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/imagens/ufpe_logo.png'))

figure = df.plot.bar(ax =ax, x = "estado", y ="mortalidade",figsize = (10,8), legend = None)
figure.set_xlabel(" ")
figure.set_title("Relação entre total de mortos e total de casos confirmados", family = "Serif", fontsize = 18)
figure.tick_params(axis = 'both', labelsize  = 14)

for p in ax.patches:
    b = p.get_bbox()
    val = "{:.1%}".format(b.y1 + b.y0)        
    ax.annotate(val, ((b.x0 + b.x1)/2, b.y1*1.01), fontsize = 14,rotation=90,ha='center', va='bottom')


figure.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y))) 

Now = str(date_rng[-1:][0][0])

newax0 = fig.add_axes([.025,-.15, 1, 1], anchor='NE')
newax0.text(.1, .1,"Fonte dos dados: Ministério da Saúde do Brasil \nAutores: Artur Coutinho, Lucas Ravellys, Lucio Camara e Silva, Maira Pitta, Anderson Almeida\nData da atualização: "+Now, family = "Verdana")
newax0.axis('off')


newax2 = fig.add_axes([.15,.7, 0.15, 0.15], anchor='NW')
newax2.imshow(im_ufpe)
newax2.axis('off')

plt.show()

fig.savefig('C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/imagens/mortality.png', dpi = 300,bbox_inches='tight',transparent = True)

#################################
mypath2 = 'C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/DADOS_estimados'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

mort = []
est = []
mort_total = []
for i in onlyfiles:
    FILE = i
    data = pd.read_csv(mypath+'/'+FILE, header = 0, sep = ";")    
    data2 = pd.read_csv(mypath2+'/'+FILE, header = 0, sep = ";")
    tot_casos = data2["I"].values[-1:]
    
    data2 = data2[:len(data2) - 365]
    mortality = data["cum-Deaths"].values[-1:]/data2["I"].values[-1:]
    mort.append(mortality)
    est.append(FILE[9:-4])
    mort_total.append(tot_casos*mortality)
    
mort =np.array(mort)    
est = np.array(est)
mort_total = np.array(mort_total)

df = pd.DataFrame(mort, columns = ["mortalidade"])
df["estado"] = est
df = df.sort_values(by = ["mortalidade"])

fig, ax = plt.subplots(1, 1)

im_ufpe = plt.imread(get_sample_data('C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/imagens/ufpe_logo.png'))

figure = df.plot.bar(ax =ax, x = "estado", y ="mortalidade",figsize = (10,8), legend = None)
figure.set_xlabel(" ")
figure.set_title("Relação entre total de mortos \ne total de casos estimados\n(incluindo assintomáticos)", family = "Serif", fontsize = 18)
figure.tick_params(axis = 'both', labelsize  = 14)

for p in ax.patches:
    b = p.get_bbox()
    val = "{:.1%}".format(b.y1 + b.y0)        
    ax.annotate(val, ((b.x0 + b.x1)/2, b.y1*1.01), fontsize = 14,rotation=90,ha='center', va='bottom')


figure.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y))) 

Now = str(date_rng[-1:][0][0])

newax0 = fig.add_axes([.025,-.15, 1, 1], anchor='NE')
newax0.text(.1, .1,"Fonte dos dados: Ministério da Saúde do Brasil \nAutores: Artur Coutinho, Lucas Ravellys, Lucio Camara e Silva, Maira Pitta, Anderson Almeida\nData da atualização: "+Now, family = "Verdana")
newax0.axis('off')


newax2 = fig.add_axes([.15,.7, 0.15, 0.15], anchor='NW')
newax2.imshow(im_ufpe)
newax2.axis('off')

plt.show()

fig.savefig('C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/imagens/mortality_real_estimada.png', dpi = 300,bbox_inches='tight',transparent = True)

#######
df = pd.DataFrame(mort_total, columns = ["mortalidade"])
df["estado"] = est
df = df.sort_values(by = ["mortalidade"])

fig, ax = plt.subplots(1, 1)

im_ufpe = plt.imread(get_sample_data('C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/imagens/ufpe_logo.png'))

figure = df.plot.bar(ax =ax, x = "estado", y ="mortalidade",figsize = (10,8), legend = None,logy = True)
figure.set_xlabel(" ")
figure.set_title("Estimativa do total de mortos", family = "Serif", fontsize = 18)
figure.tick_params(axis = 'both', labelsize  = 16)

for p in ax.patches:
    b = p.get_bbox()
    
    val = "{:.0f}".format(b.y1 + b.y0)        
    ax.annotate(val, ((b.x0 + b.x1)/2, b.y1*1.01), fontsize = 14,rotation=90,ha='center', va='bottom')

#figure.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0}'.format(y))) 

Now = str(date_rng[-1:][0][0])

newax0 = fig.add_axes([.025,-.15, 1, 1], anchor='NE')
newax0.text(.1, .1,"Fonte dos dados: Ministério da Saúde do Brasil \nAutores: Artur Coutinho, Lucas Ravellys, Lucio Camara e Silva, Maira Pitta, Anderson Almeida\nData da atualização: "+Now, family = "Verdana")
newax0.axis('off')


newax2 = fig.add_axes([.15,.7, 0.15, 0.15], anchor='NW')
newax2.imshow(im_ufpe)
newax2.axis('off')

plt.show()

fig.savefig('C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/imagens/total de mortes.png', dpi = 300,bbox_inches='tight',transparent = True)
