# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from scipy.integrate import odeint
import hydroeval as hy
from scipy.optimize import curve_fit
from os import listdir
from os.path import isfile, join
from csv import DictWriter
import matplotlib.pyplot as plt
from matplotlib.cbook import get_sample_data
from matplotlib.ticker import FuncFormatter
from datetime import datetime
now = datetime.now()
Now = str(now.year)+'-'+ str(now.month)+'-'+str(now.day)
 
def append_dict_as_row(file_name, dict_of_elem, field_names):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        dict_writer = DictWriter(write_obj, fieldnames=field_names)
        # Add dictionary as wor in the csv
        dict_writer.writerow(dict_of_elem)

def desacum(X):
    a = [X[0]]
    for i in range(len(X)-1):
        a.append(X[i+1]-X[i])
    return a

def sucq(x,t,alfa,beta,gama1):
    S=x[0]
    U=x[1]
    Q=x[2]
        
    St = -alfa*U*S
    Ut = alfa*U*S - gama1*U
    Qt = gama1*U - beta*Q
    Ct = beta*Q    
    
    return [St,Ut,Qt,Ct]

def sucq_solve(t,alfa,beta,gama1,So,Uo,Qo,Co):
 
    SUCQ = odeint(sucq, [So,Uo,Qo,Co],t, args=(alfa,beta,gama1))
    return SUCQ[:,3].ravel()



def SUCQ(t,alfa,beta,gama1,So,Uo,Qo,Co):
 
    SUCQ = odeint(sucq, [So,Uo,Qo,Co],t, args=(alfa,beta,gama1))
    return SUCQ


def ajust_curvefit(days_mens,cumdata_cases,p0,bsup,binf):
    popt, pcov = curve_fit(sucq_solve, days_mens, cumdata_cases,
                           bounds = (binf,bsup),
                           p0 = p0,
                           absolute_sigma = True)
    return popt

from scipy.optimize import minimize

def object_minimize(x,t,cumdata_cases):
 
    SUCQ = odeint(sucq, [x[3],x[4],x[5],x[6]],t, args=(x[0],x[1],x[2]))
    return sum((np.log10(cumdata_cases)-np.log10(SUCQ[:,3].ravel()))**2)

def min_minimize(cumdata_cases,sucq_solve,p0,t,bsup,binf):
    bnds = ((binf[0],bsup[0]),(binf[1],bsup[1]),(binf[2],bsup[2]),(binf[3],bsup[3]),(binf[4],bsup[4]),(binf[5],bsup[5]),(binf[6],bsup[6]))
    res = minimize(object_minimize, p0, args = (t,cumdata_cases), bounds = bnds, method='TNC')
    return res.x

def Ajust_SUCQ(FILE,pop,extrapolação):    
        
    data_covid = pd.read_csv("DADOS/"+FILE, header = 0, sep = ";")
    data_covid=data_covid[['DateRep','Cases']]
    day_0_str=data_covid['DateRep'][0][-4:]+'-'+data_covid['DateRep'][0][3:5]+'-'+data_covid['DateRep'][0][:2]
    day_0 = np.array(day_0_str, dtype=np.datetime64)
    date = np.array(day_0_str, dtype=np.datetime64)+ np.arange(len(data_covid))
    
    if date[0]>=np.array('2020-02-26', dtype=np.datetime64):
        t0 = 0
    else:
        dif_dias =np.array('2020-02-26', dtype=np.datetime64)-date[0]
        t0 = dif_dias.astype(int)
    
    day_isol = '2020-03-18'
    dif_dias = date[len(date)-1] - np.array(day_isol, dtype=np.datetime64)
    tf = dif_dias.astype(int)
    
    if (day_0 <= np.array(day_isol, dtype=np.datetime64)):
        
        date = date[t0:-tf] 
        cumdata_covid = data_covid[['Cases']].cumsum()

        cumdata_cases = cumdata_covid['Cases'].values[t0:-tf]
    
        days_mens = np.linspace(1,len(cumdata_cases),len(cumdata_cases))

        N = pop*10**6
        t = days_mens
        alfa_0,beta_0,gama1_0= [.8/N,.1,.19] 
        So,Uo,Qo,Co = [.8*N,6*cumdata_cases[0],cumdata_cases[0],cumdata_cases[0]]

        p0 = [alfa_0,beta_0,gama1_0,So,Uo,Qo,Co] 

        bsup = [1/N,1,1,N,Uo*1.5,Qo*1.2,Co+10**-9]
        binf = [0,0,0,.5*N,Uo*.5,Qo*0.8,Co-10**-9]
    
        popt = ajust_curvefit(days_mens,cumdata_cases,p0,bsup,binf)
        p0 = popt
        popt = min_minimize(cumdata_cases,sucq_solve,p0,t,bsup,binf)
        alfa_0,beta_0,gama1_0,So,Uo,Qo,Co = popt 

        solution = SUCQ(t,alfa_0,beta_0,gama1_0,So,Uo,Qo,Co)

        NSE = hy.nse(cumdata_cases,solution[:,3])
#        print(FILE[9:-4])
#        print("alfa = %f " % (alfa_0*N))
#        print("beta = %f " % (beta_0))
#        print("gamma = %f " % (gama1_0))
#        print("R = %f" %(alfa_0*N/gama1_0))
#        print("NSE = %.5f " % (NSE))
#        print("#######################")
    
        date_future = np.array(date[0], dtype=np.datetime64)+ np.arange(len(date)+extrapolação)
        days_future = np.linspace(1,len(cumdata_cases)+extrapolação,len(cumdata_cases)+extrapolação)
        Cum_cases_estimated = SUCQ(days_future, *popt)
        estimativafutura_saída=pd.DataFrame(Cum_cases_estimated[:,3], columns = ["Cases"])
        estimativafutura_saída["S"]=Cum_cases_estimated[:,0]
        estimativafutura_saída["U"]=Cum_cases_estimated[:,1]
        estimativafutura_saída["Q"]=Cum_cases_estimated[:,2]
        estimativafutura_saída["I"] = Cum_cases_estimated[:,1]+Cum_cases_estimated[:,2]+Cum_cases_estimated[:,3]
        estimativafutura_saída["date"] = date_future
        estimativafutura_saída.to_csv("C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/DADOS_estimados_sem_isolamento/"+FILE,sep=";")
        if NSE >=0.9:
            return [alfa_0*N/gama1_0, FILE[9:-4]]
        
população = [["Espanha",46.72],["Itália",60.43],["SP",45.92],["MG",21.17],["RJ",17.26],["BA",14.87],["PR",11.43],["RS",11.37],["PE",9.6],["CE",9.13],["Pará",8.6],["SC",7.16],["MA",7.08],["GO",7.02],["AM", 4.14],["ES",4.02],["PB",4.02],["RN",3.51],["MT",3.49],["AL", 3.4],["PI",3.3],["DF",3.1],["MS",2.8],["SE",2.3],["RO",1.78],["TO",1.6],["AC",0.9],["AM",0.85],["RR",0.61],["Brasil",210.2]]
população = np.array(população)

mypath = 'C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/DADOS'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

#import mensured data
extrapolação = 24
#onlyfiles =onlyfiles[:2]

R = []
for i in onlyfiles:
    FILE = i
    for i in população:
        if i[0] == FILE[9:-4]:
            pop = float(i[1])
    
    R.append(Ajust_SUCQ(FILE,pop,extrapolação))   

mypath2 = 'C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/Dados_site'
onlyfiles2 = [f for f in listdir(mypath2) if isfile(join(mypath2, f))]
mypath3 = 'C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/DADOS_estimados_sem_isolamento'
mypath4 = 'C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/DADOS_estimados'

fig,ax = plt.subplots(1, 1)
ax.set_xlim(np.array("2020-02-20", dtype=np.datetime64), np.array("2020-04-04", dtype=np.datetime64))

Color = np.array(["r","y","g"])
cont = 0

for i in onlyfiles2:
    FILE = i
    for i in população:
        if i[0] == FILE[9:-4]:
            pop = float(i[1])
    
    data = pd.read_csv(mypath3+'/'+FILE, header = 0, sep = ";")
    data_covid = data[["Cases","S","U","Q","I"]]#/(pop*10**6)
    data_covid["date"] = data["date"]
    data_covid["Tendência Inicial"] = data_covid["Cases"]
    data_covid['datetime'] = pd.to_datetime(data_covid['date'])

    figure = data_covid.plot(ax = ax,kind = "line", x = "datetime", y = "Tendência Inicial",
                             style = '--', color = Color[cont],grid = True,rot = 90,figsize= (8,6), logy = True) 

    data_2 = pd.read_csv(mypath+'/'+FILE, header = 0, sep = ";")
    data_covid2 = data_2[["cum-Cases",'DateRep']]#/(pop*10**6)
    day_0_str=data_covid2['DateRep'][0][-4:]+'-'+data_covid2['DateRep'][0][3:5]+'-'+data_covid2['DateRep'][0][:2]
    date_rng = np.array(day_0_str, dtype=np.datetime64)+ np.arange(len(data_covid2))
    
    date_ = pd.DataFrame(date_rng, columns=['date'])
    data_covid2['datetime'] = date_[['date']]
    data_covid2[FILE[9:-4]] = data_covid2["cum-Cases"]

    figure2 = data_covid2.plot(ax = ax, kind = "line",x = 'datetime', y = FILE[9:-4],
                               style = Color[cont]+'o-', grid = True,rot = 90,figsize= (8,6))   
    cont =cont+1
    data_1 = pd.read_csv(mypath4+'/'+FILE, header = 0, sep = ";")

#    dif_dias = np.array(data_1["date"][len(data_1)-1], dtype=np.datetime64) - date_rng[-1:]
#    tf = dif_dias.astype(int)
    data_covid1 = data_1[["Cases","S","U","Q","I"]][:-365+7]#/(pop*10**6)
    data_covid1["date"] = data_1["date"][:-365+7]
    data_covid1["Tendência Atual"] = data_covid1["Cases"]
    data_covid1['datetime'] = pd.to_datetime(data_covid1['date'])

    figure1 = data_covid1.plot(ax = ax,kind = "line", x = "datetime", y = "Tendência Atual",color = 'black',grid = True,rot = 90,figsize= (8,6), logy = True)
    
    
    
figure.tick_params(axis = 'both', labelsize  = 14)
figure.set_title("Tendência de crescimento do Total de Casos \nantes e depois do isolamento social ", family = "Serif", fontsize = 18)
figure.set_xlabel(" ")

figure.axvline(pd.to_datetime('2020-03-18'), color='gray', linestyle='--', lw=2)
figure.text(pd.to_datetime('2020-03-17'),2*10**3, "ínicio das medidas de \nisolamento social", fontsize=12,
               rotation=90, rotation_mode='anchor')

im_ufpe = plt.imread(get_sample_data('C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/imagens/ufpe_logo.png'))


Now = str(date_rng[-1:][0])

newax0 = fig.add_axes([.025,-.15, 1, 1], anchor='NE')
newax0.text(.1, .1,"Fonte dos dados: Ministério da Saúde do Brasil \nAutores: Artur Coutinho, Lucas Ravellys, Lucio Camara e Silva, Maira Pitta, Anderson Almeida\nData da atualização: "+Now, family = "Verdana")
newax0.axis('off')

newax2 = fig.add_axes([.725,.125, 0.15, 0.15], anchor='NE')
newax2.imshow(im_ufpe)
newax2.axis('off')

plt.show()

fig.savefig('C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/imagens/cum_cases.png', dpi = 300,bbox_inches='tight',transparent = True)

    
