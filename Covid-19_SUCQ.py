# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 10:51:57 2020

@author: ravel
"""
import numpy as np
import pandas as pd
from scipy.integrate import odeint
import hydroeval as hy
from scipy import stats
from scipy.optimize import curve_fit

def nstf(ci):
    # Convert to percentile point of the normal distribution.
    pp = (1. + ci) / 2.
    # Convert to number of standard deviations.
    return stats.norm.ppf(pp)

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

#import mensured data
FILE = "COVID-19 Ceará.csv"
t0=0
extrapolação = 5
pop = 9.1

data_covid = pd.read_csv(FILE, header = 0, sep = ";")
data_covid=data_covid[['DateRep','Cases']]
day_0_str=data_covid['DateRep'][0][-4:]+'-'+data_covid['DateRep'][0][3:5]+'-'+data_covid['DateRep'][0][:2]
date = np.array(day_0_str, dtype=np.datetime64)+ np.arange(len(data_covid))
date= date[t0:]

cumdata_covid = data_covid[['Cases']].cumsum()

cumdata_cases = cumdata_covid['Cases'].values[t0:]
days_mens = np.linspace(1,len(cumdata_cases),len(cumdata_cases))

N =.7*pop*10**6
t = days_mens
alfa_0,beta_0,gama1_0= [.5/N,.1,.5] 
So,Uo,Qo,Co = [N,6*cumdata_cases[0],cumdata_cases[0],cumdata_cases[0]]

p0 = [alfa_0,beta_0,gama1_0,So,Uo,Qo,Co] 

bsup = [1/N,1,1,So+100000,Uo*1.5,Qo+10**-9,Co+10**-9]
binf = [0,0,0,So-100000,Uo*.5,Qo-10**-9,Co-10**-9]

popt, pcov = curve_fit(sucq_solve, days_mens, cumdata_cases,
                       bounds = (binf,bsup),
                       p0 = p0,
                       absolute_sigma = True,
                       method = 'trf')

alfa_0,beta_0,gama1_0,So,Uo,Qo,Co = popt 
perr = np.sqrt(np.diag(pcov))
Nstd = nstf(.95)
popt_up = popt + Nstd * perr
popt_dw = popt - Nstd * perr

print("alfa = %f " % (alfa_0*N))
print("beta = %f " % (beta_0))
print("gamma = %f " % (gama1_0))
print("R = %f" %(alfa_0*N/gama1_0))

solution = SUCQ(t,alfa_0,beta_0,gama1_0,So,Uo,Qo,Co)

NSE = hy.nse(cumdata_cases,solution[:,3])

print("NSE = %.5f " % (NSE))

date_future = np.array(date[0], dtype=np.datetime64)+ np.arange(len(date)+extrapolação)
days_future = np.linspace(1,len(cumdata_cases)+extrapolação,len(cumdata_cases)+extrapolação)
Cum_cases_estimated = SUCQ(days_future, *popt)
estimativafutura_saída=pd.DataFrame(Cum_cases_estimated[:,3], columns = ["Cases"])
estimativafutura_saída["I"] = Cum_cases_estimated[:,1]+Cum_cases_estimated[:,2]+Cum_cases_estimated[:,3]
estimativafutura_saída["date"] = date_future
estimativafutura_saída.to_csv("C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/DADOS_estimados/"+FILE,sep=";")

df_SUCQ = pd.DataFrame(data = solution[:,1:], columns = ["U","Q","C"])
df_SUCQ["casos reais"]= cumdata_cases
df_SUCQ.to_csv("saida"+FILE,sep=";")
df_SUCQ.plot(logy=True)

R = alfa_0*N/gama1_0 #reproductive number of the infection
gama1_0 = gama1_0 #quarantine rate for an un-quarantined infected being quarantined
beta_0 = beta_0 #the total confirmation rate.

# importar bibliotecas
import plotly.graph_objects as go
import numpy as np
from plotly.offline import plot

x = pd.to_datetime(date)
y = cumdata_cases

fig = go.Figure()
fig.update_layout(title_text= FILE[:-4],
                  title_font_size=30,
                  yaxis_title="Nº total de casos \n (escala logarítmica)",
                  font=dict(
                          family="Serif",
                          size=16,
                          color="black"
                          ))
fig.update_layout(yaxis_type="log", width=1000, height=800)


fig.add_trace(go.Scatter(
    x=date_future, y=Cum_cases_estimated[:,3],
    name='Casos confirmados estimados'
))
fig.add_trace(go.Scatter(
    x=x, y=y,
    mode='markers',
    name='Casos confirmados medidos',
    marker=dict(color='purple', size=8)
))

fig.add_trace(go.Scatter(
    x=date_future, y=Cum_cases_estimated[:,1]+Cum_cases_estimated[:,2]+Cum_cases_estimated[:,3],
    name='Total de Infectados (incluindo assintomáticos)'
))

fig.add_trace(go.Scatter(
    x=date_future[-1*extrapolação:], y=Cum_cases_estimated[:,3][-1*extrapolação:],
    mode='markers',
    name='Total de casos confirmados nos próximos %d dias'%(extrapolação),
    marker= dict(color='red', size=8)
))

#fig.add_trace(go.Scatter(
#    x=date_future[-1*extrapolação:], y=Cum_cases_estimated_up[-1*extrapolação:],
#    name='Intervalo de confiança (95%)',
#    marker=dict(color='red', size=8)
#))
#fig.add_trace(go.Scatter(
#    x=date_future[-1*extrapolação:], y=Cum_cases_estimated_dw[-1*extrapolação:],
#    name='Intervalo de confiança (95%)',
#    marker=dict(color='red', size=8)
#))

#plot(fig,filename="Previsão Futura " + FILE[:-4]+".html")

