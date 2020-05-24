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
from csv import DictWriter
from math import log10, floor

def format_func(value, tick_number=None):
    num_thousands = 0 if abs(value) < 1000 else floor (log10(abs(value))/3)
    value = round(value / 1000**num_thousands, 2)
    return f'{value:g}'+' KMGTPEZY'[num_thousands]

 
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
#    
#    if cumdata_cases[-1:] < 1000:
#    return sum( ( np.log10(cumdata_cases)-np.log10(SUCQ[:,3].ravel()) )**2)
#    if cumdata_cases[-1:] >= 1000:
#    return sum((cumdata_cases-SUCQ[:,3].ravel())**2)
    return -1*hy.nse(SUCQ[:,3],cumdata_cases)

def min_minimize(cumdata_cases,sucq_solve,p0,t,bsup,binf):
    bnds = ((binf[0],bsup[0]),(binf[1],bsup[1]),(binf[2],bsup[2]),(binf[3],bsup[3]),(binf[4],bsup[4]),(binf[5],bsup[5]),(binf[6],bsup[6]))
    res = minimize(object_minimize, p0, args = (t,cumdata_cases), bounds = bnds, method='TNC')
    return res.x

def Ajust_SUCQ(FILE,pop,extrapolação):    
    path = 'C:/Users/ravellys/Documents/GitHub/COVID-19-Brasil/COVID-19-Brasil/data/DADOS/'
    data_covid = pd.read_csv(path+FILE, header = 0, sep = ";")
    data_covid=data_covid[['DateRep','Cases']]
    nome_data = 'DateRep'
    df = data_covid[['DateRep','Cases']]
    day_0_str=df[nome_data][0][:4]+'-'+df[nome_data][0][5:7]+'-'+df[nome_data][0][-2:]
    date = np.array(day_0_str, dtype=np.datetime64)+ np.arange(len(data_covid))
    
    
    if date[0]>=np.array('2020-05-09', dtype=np.datetime64):
        t0 = 0
    else:
        dif_dias =np.array('2020-05-09', dtype=np.datetime64)-date[0]
        t0 = dif_dias.astype(int)
    
    date= date[t0:] 
    
    cumdata_covid = df[['Cases']].cumsum()

    cumdata_cases = cumdata_covid['Cases'].values[t0:]
    days_mens = np.linspace(1,len(cumdata_cases),len(cumdata_cases))
    
    
    N = pop*10**6
    t = days_mens
    So,Uo,Qo,Co = [.9*N,6*cumdata_cases[0],cumdata_cases[0],cumdata_cases[0]] # padrão [.8*N,6*cumdata_cases[0],cumdata_cases[0],cumdata_cases[0]]
    alfa_0,beta_0,gama1_0= [.2/So,.3,.1] # padrão [.5/N,.1,.19]

    p0 = [alfa_0,beta_0,gama1_0,So,Uo,Qo,Co] 

    bsup = [0.4/So,.50,.20,   N,Uo*2.,Qo*2.0,Co+10**-9]
    binf = [0.09/So,.05,.01,.7*N,Uo*.5,Qo*0.5,Co-10**-9]
    
    #p0 = ajust_curvefit(days_mens,cumdata_cases,p0,bsup,binf)
    popt = min_minimize(cumdata_cases,sucq_solve,p0,t,bsup,binf)
    alfa_0,beta_0,gama1_0,So,Uo,Qo,Co = popt 

    solution = SUCQ(t,alfa_0,beta_0,gama1_0,So,Uo,Qo,Co)

    NSE = hy.nse(solution[:,3],cumdata_cases)
    RMSE = hy.rmse(solution[:,3],cumdata_cases)
    MARE = hy.mare(solution[:,3],cumdata_cases)
    
    print(FILE[9:-4])
    print("alfa = %f " % (alfa_0*So))
    print("beta = %f " % (beta_0))
    print("gamma = %f " % (gama1_0))
    print("R = %f" %(alfa_0*So/gama1_0))
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
    fileout = 'C:/Users/ravellys/Documents/GitHub/COVID-19-Brasil/COVID-19-Brasil/data/DADOS_estimados/'
    estimativafutura_saída.to_csv(fileout+FILE,sep=";")
    
    #par_SUQC_head = ["estado","população","data inicial","data final", "R","alfa","beta","gamma","So","Uo","Qo","Co","NSE"]
    #par_SUQC = {"estado":FILE[9:-4],"população":pop,"data inicial":date[0],"data final": date[-1:][0],"R": alfa_0*N/gama1_0,"alfa":popt[0]*N,"beta":popt[1],"gamma":popt[2],"So":popt[3],"Uo":popt[4],"Qo":popt[5],"Co":popt[6],"NSE":NSE}

    #append_dict_as_row("C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/par_SUCQ.csv",par_SUQC,par_SUQC_head)
    
    return [alfa_0*So/gama1_0,alfa_0*So, beta_0, gama1_0, So,Uo,Qo,Co, NSE, RMSE, MARE]
    
população = [["Espanha",46.72],["Itália",60.43],["SP",45.92],["MG",21.17],["RJ",17.26],["BA",14.87],["PR",11.43],["RS",11.37],["PE",9.6],["CE",9.13],["PA",8.6],["SC",7.16],["MA",7.08],["GO",7.02],["AM", 4.14],["ES",4.02],["PB",4.02],["RN",3.51],["MT",3.49],["AL", 3.4],["PI",3.3],["DF",3.1],["MS",2.8],["SE",2.3],["RO",1.78],["TO",1.6],["AC",0.9],["AP", 0.85],["RR",0.61],["Brazil",210.2]]
população = np.array(população)

mypath = 'C:/Users/ravellys/Documents/GitHub/COVID-19-Brasil/COVID-19-Brasil/data/DADOS'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

extrapolação = 365

#import mensured data
estados = ['COVID-19 Brazil.csv']

R = []
for i in estados:
    FILE = i
    for i in população:
        if i[0] == FILE[9:-4]:
            pop = float(i[1])
    
    R.append(Ajust_SUCQ(FILE,pop,extrapolação))       
R = np.array(R)

df_R = pd.DataFrame(R, columns = ["R","alfa","beta","gamma1","So","Uo","Qo","Co","NSE","RMSE","MARE"])
path_out = 'C:/Users/ravellys/Documents/GitHub/COVID-19-Brasil/COVID-19-Brasil'

x =[]
for i in estados:
    x.append(i[9:-4]) 
names = np.array(x)

df_R["Estados"] = names  

df_R = pd.read_csv(path_out+'/metrics.csv',header = 0,sep=";")

for i in range(len(estados)):
    a = R[i].tolist()
    a.append(estados[i][9:-4])
    df_R.loc[(df_R["Estados"] == estados[i][9:-4])] = [a]
  
#df_R = pd.DataFrame(R, columns = ["n1","R1","n2","R2","beta","gamma1","gamma2","eta","N","So","Uo","Qo","Co","R1o","R2o","nCo","NSE","RMSE","MARE","NSE_deaths","RMSE_deaths","MARE_deaths"])
#df_R["Estado"] = estados

df_R.to_csv(path_out+'/metrics.csv',sep=";",index = False)
  
def bar_plt(atributo, title_name,df,logscale):
    fig, ax = plt.subplots(1, 1)
    df = df.sort_values(by=[atributo])

    figure = df.plot.bar(ax = ax, x = "Estados", y = atributo, figsize = (15,8), legend = None, width=.75, logy = logscale)
    figure.set_xlabel(" ")
    figure.set_title(title_name, family = "Serif", fontsize = 22)
    figure.tick_params(axis = 'both', labelsize  = 14)
    #figure.yaxis.set_major_formatter(plt.FuncFormatter(format_func)) 

    for p in ax.patches:
       b = p.get_bbox()
       val = format_func(b.y1 + b.y0,1)        
       ax.annotate(val, ((b.x0 + b.x1)/2, b.y1), fontsize = 14,ha='center', va='top',rotation = 90)
  
    plt.show()
    path_out ="C:/Users/ravellys/Documents/GitHub/COVID-19-Brasil/COVID-19-Brasil/imagens/"
    fig.savefig(path_out+atributo+'_barplot.png', dpi = 300,bbox_inches='tight')

bar_plt(atributo = "R", title_name = "Ro", df = df_R, logscale = False)
bar_plt(atributo = "NSE", title_name = "NSE", df = df_R, logscale = False)

