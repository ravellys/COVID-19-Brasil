# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 10:51:57 2020

@author: ravel
"""
import numpy as np
import pandas as pd
from scipy.integrate import odeint
import hydroeval as hy
from scipy.optimize import curve_fit
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
from matplotlib.cbook import get_sample_data
from matplotlib.ticker import FuncFormatter

from csv import DictWriter
 
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
        
    data_covid = pd.read_csv("CasosPorEstado/DADOS/"+FILE, header = 0, sep = ";")
    data_covid=data_covid[['DateRep','Cases']]
    day_0_str=data_covid['DateRep'][0][-4:]+'-'+data_covid['DateRep'][0][3:5]+'-'+data_covid['DateRep'][0][:2]
    date = np.array(day_0_str, dtype=np.datetime64)+ np.arange(len(data_covid))
    
    if date[0]>=np.array('2020-03-18', dtype=np.datetime64):
        t0 = 0
    else:
        dif_dias =np.array('2020-03-18', dtype=np.datetime64)-date[0]
        t0 = dif_dias.astype(int)
    
    date= date[t0:] 
    
    cumdata_covid = data_covid[['Cases']].cumsum()

    cumdata_cases = cumdata_covid['Cases'].values[t0:]
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
    print(FILE[9:-4])
    print("alfa = %f " % (alfa_0*N))
    print("beta = %f " % (beta_0))
    print("gamma = %f " % (gama1_0))
    print("R = %f" %(alfa_0*N/gama1_0))
    print("NSE = %.5f " % (NSE))
    print("#######################")
    
    date_future = np.array(date[0], dtype=np.datetime64)+ np.arange(len(date)+extrapolação)
    days_future = np.linspace(1,len(cumdata_cases)+extrapolação,len(cumdata_cases)+extrapolação)
    Cum_cases_estimated = SUCQ(days_future, *popt)
    estimativafutura_saída=pd.DataFrame(Cum_cases_estimated[:,3], columns = ["Cases"])
    estimativafutura_saída["S"]=Cum_cases_estimated[:,0]
    estimativafutura_saída["U"]=Cum_cases_estimated[:,1]
    estimativafutura_saída["Q"]=Cum_cases_estimated[:,2]
    estimativafutura_saída["I"] = Cum_cases_estimated[:,1]+Cum_cases_estimated[:,2]+Cum_cases_estimated[:,3]
    estimativafutura_saída["date"] = date_future
    estimativafutura_saída.to_csv("C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/DADOS_estimados/"+FILE,sep=";")
    
    par_SUQC_head = ["estado","população","data inicial","data final", "R","alfa","beta","gamma","So","Uo","Qo","Co","NSE"]
    par_SUQC = {"estado":FILE[9:-4],"população":pop,"data inicial":date[0],"data final": date[-1:][0],"R": alfa_0*N/gama1_0,"alfa":popt[0]*N,"beta":popt[1],"gamma":popt[2],"So":popt[3],"Uo":popt[4],"Qo":popt[5],"Co":popt[6],"NSE":NSE}

    append_dict_as_row("C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/par_SUCQ.csv",par_SUQC,par_SUQC_head)
    
    return alfa_0*N/gama1_0
    
população = [["Espanha",46.72],["Itália",60.43],["SP",45.92],["MG",21.17],["RJ",17.26],["BA",14.87],["PR",11.43],["RS",11.37],["PE",9.6],["CE",9.13],["Pará",8.6],["SC",7.16],["MA",7.08],["GO",7.02],["AM", 4.14],["ES",4.02],["PB",4.02],["RN",3.51],["MT",3.49],["AL", 3.4],["PI",3.3],["DF",3.1],["MS",2.8],["SE",2.3],["RO",1.78],["TO",1.6],["AC",0.9],["AM",0.85],["RR",0.61],["Brasil",210.2]]
população = np.array(população)

mypath = 'C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/DADOS'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

#import mensured data
extrapolação = 365
#onlyfiles =onlyfiles[:2]
R = []
for i in onlyfiles:
    FILE = i
    for i in população:
        if i[0] == FILE[9:-4]:
            pop = float(i[1])
    
    R.append(Ajust_SUCQ(FILE,pop,extrapolação))       
R = np.array(R)

df_R = pd.DataFrame(R, columns = ["R"])

x =[]
for i in onlyfiles:
    x.append(i[9:-4]) 
names = np.array(x)

df_R["Estados"] = names    
df_R = df_R.sort_values(by=["R"])

fig, ax = plt.subplots(1, 1)

im_ufpe = plt.imread(get_sample_data('C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/imagens/ufpe_logo.png'))

figure = df_R.plot.bar(ax =ax, x = "Estados", y ="R",figsize = (10,8), legend = None)
figure.set_xlabel(" ")
figure.set_title("Reprodutividade do vírus (Ro)", family = "Serif", fontsize = 22)
figure.tick_params(axis = 'both', labelsize  = 14)

figure.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.2}'.format(y))) 

data = pd.read_csv(mypath+'/'+onlyfiles[0], header = 0, sep = ";")
date_rng = data[["DateRep"]].values

Now = str(date_rng[-1:][0][0])

newax0 = fig.add_axes([.025,-.15, 1, 1], anchor='NE')
newax0.text(.1, .1,"Fonte dos dados: Ministério da Saúde do Brasil \nAutores: Artur Coutinho, Lucas Ravellys, Lucio Camara e Silva, Maira Pitta, Anderson Almeida\nData da atualização: "+Now, family = "Verdana")
newax0.axis('off')


newax2 = fig.add_axes([.15,.7, 0.15, 0.15], anchor='NW')
newax2.imshow(im_ufpe)
newax2.axis('off')

plt.show()

fig.savefig('C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/imagens/R0.png', dpi = 300,bbox_inches='tight',transparent = True)
