import pandas as pd
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cbook import get_sample_data
from matplotlib.ticker import FuncFormatter

def desacum(X):
    a = [X[0]]
    for i in range(len(X)-1):
        a.append(X[i+1]-X[i])
    return a

mypath = 'C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/Dados_estimados'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

mypath2 = 'C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/Dados_site'
onlyfiles2 = [f for f in listdir(mypath2) if isfile(join(mypath, f))]

população = [["Espanha",46.72],["Itália",60.43],["SP",45.92],["MG",21.17],["RJ",17.26],["BA",14.87],["PR",11.43],["RS",11.37],["PE",9.6],["CE",9.13],["Pará",8.6],["SC",7.16],["MA",7.08],["GO",7.02],["AM", 4.14],["ES",4.02],["PB",4.02],["RN",3.51],["MT",3.49],["AL", 3.4],["PI",3.3],["DF",3.1],["MS",2.8],["SE",2.3],["RO",1.78],["TO",1.6],["AC",0.9],["AM",0.85],["RR",0.61],["Brasil",210.2]]
população = np.array(população)


fig,ax = plt.subplots(1, 1)
ax.set_xlim(np.array("2020-02-28", dtype=np.datetime64), np.array("2020-04-04", dtype=np.datetime64))

for i in onlyfiles2:
    FILE = i
    for i in população:
        if i[0] == FILE[9:-4]:
            pop = float(i[1])
    print(FILE)       
    data = pd.read_csv(mypath+'/'+FILE, header = 0, sep = ";")
    data_covid = data[["Cases","S","U","Q","I"]]/(pop*10**6)
    data_covid["date"] = data["date"]
    data_covid[FILE[9:-4]] = desacum(data_covid["Cases"])
    data_covid['datetime'] = pd.to_datetime(data_covid['date'])
    
    
    figure = data_covid.plot(ax =ax,kind = "line", x = "datetime", y = FILE[9:-4],
                             grid = True,rot = 90,figsize= (8,6))
    figure.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.3%}'.format(y))) 


figure.tick_params(axis = 'both', labelsize  = 14)
figure.set_title("Estimativa de Casos Diários \n (em relação ao total populacional)", family = "Serif", fontsize = 18)
figure.set_xlabel(" ")

im_ufpe = plt.imread(get_sample_data('C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/imagens/ufpe_logo.png'))

inicio = str(data["date"][0])
fim = str(data["date"].values[-366:][0])

newax0 = fig.add_axes([.025,-.15, 1, 1], anchor='NE')
newax0.text(.1, .1,"Fonte dos dados: Ministério da Saúde do Brasil \nAutores: Artur Coutinho, Lucas Ravellys, Lucio Camara e Silva, Maira Pitta, Anderson Almeida\nIntervalo de dias ajustados: "+ inicio + " a " + fim, family = "Verdana")
newax0.axis('off')

newax2 = fig.add_axes([.15,.625, 0.15, 0.15], anchor='NW')
newax2.imshow(im_ufpe)
newax2.axis('off')

plt.show()

fig.savefig('C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/imagens/daily_cases.png', dpi = 300,bbox_inches='tight',transparent = True)

####################################### 



for i in onlyfiles2:
    FILE = i
    for i in população:
        if i[0] == FILE[9:-4]:
            pop = float(i[1])
    print(FILE)       
    fig,ax = plt.subplots(1, 1)

    data = pd.read_csv(mypath+'/'+FILE, header = 0, sep = ";")
    data_covid = data[["Cases","S","U","Q","I"]]
    data_covid["date"] = data["date"]
    data_covid[FILE[9:-4]] = desacum(data_covid["Cases"])
    data_covid['datetime'] = pd.to_datetime(data_covid['date'])
    
    
    figure = data_covid.plot(ax =ax,kind = "line", x = "datetime", y = FILE[9:-4],
                             grid = True,rot = 90,figsize= (8,6))
    figure.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0}'.format(y))) 


    figure.tick_params(axis = 'both', labelsize  = 14)
    figure.set_title("Estimativa de Casos Diários -" + FILE[9:-4] , family = "Serif", fontsize = 18)
    figure.set_xlabel(" ")

    im_ufpe = plt.imread(get_sample_data('C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/imagens/ufpe_logo.png'))


    inicio = str(data["date"][0])
    fim = str(data["date"].values[-366:][0])

    newax0 = fig.add_axes([.025,-.15, 1, 1], anchor='NE')
    newax0.text(.1, .1,"Fonte dos dados: Ministério da Saúde do Brasil \nAutores: Artur Coutinho, Lucas Ravellys, Lucio Camara e Silva, Maira Pitta, Anderson Almeida\nIntervalo de dias ajustados: "+ inicio + " a " + fim, family = "Verdana")
    newax0.axis('off')

    newax2 = fig.add_axes([.15,.625, 0.15, 0.15], anchor='NW')
    newax2.imshow(im_ufpe)
    newax2.axis('off')

    plt.show()

    fig.savefig('C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/imagens/daily_cases'+ FILE[9:-4]+'.png', dpi = 300,bbox_inches='tight',transparent = True)
