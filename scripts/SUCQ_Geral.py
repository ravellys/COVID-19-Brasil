# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 10:51:57 2020

@author: ravel
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
from os import listdir
from os.path import isfile, join
from plotly.subplots import make_subplots
from matplotlib.ticker import FuncFormatter
from math import log10, floor

def format_func(value, tick_number=None):
    num_thousands = 0 if abs(value) < 1000 else floor (log10(abs(value))/3)
    value = round(value / 1000**num_thousands, 2)
    return f'{value:g}'+' KMGTPEZY'[num_thousands]

def desacum(X):
    a = [X[0]]
    for i in range(len(X)-1):
        a.append(X[i+1]-X[i])
    return a

def add_plot(path,FILE,fig,row,col,pop):
    data_covid = pd.read_csv(mypath+'/'+FILE, header = 0, sep = ";")
    data_covid=data_covid[['DateRep','Cases',"cum-Deaths"]]
    
    nome_data = 'DateRep'
    df = data_covid[['DateRep','Cases']]
    day_0_str=df[nome_data][0][:4]+'-'+df[nome_data][0][5:7]+'-'+df[nome_data][0][-2:]
    date = np.array(day_0_str, dtype=np.datetime64)+ np.arange(len(data_covid))
    date = np.array(date[0], dtype=np.datetime64)+ np.arange(len(date))
    date=pd.to_datetime(date)
    
    
    cumdata_covid = data_covid[['Cases']].cumsum()
    cumdata_cases = cumdata_covid['Cases'].values
    data_cum_Deaths = data_covid["cum-Deaths"].values
    
    fig.add_trace(go.Scatter(
            x=date, y=cumdata_cases/pop,
            mode='lines+markers',
            name='Nº de Casos Totais - ' + FILE[9:-4],
            marker=dict( size=8)
            ),
            row =1, col=1)
    
    fig.add_trace(go.Scatter(
            x=date, y=desacum(cumdata_cases/pop),
            mode='lines+markers',
            name='Nº de Casos Diários - ' + FILE[9:-4],
            marker=dict( size=8)
            ),
            row =2, col=1)
    
    fig.add_trace(go.Scatter(
            x=date, y=data_cum_Deaths/pop,
            mode='lines+markers',
            name='Nº de Mortes Totais - ' + FILE[9:-4],
            marker=dict( size=8)
            ),
            row =1, col=2)
    
    fig.add_trace(go.Scatter(
            x=date, y=desacum(data_cum_Deaths/pop),
            mode='lines+markers',
            name='Nº de Mortes Diárias - ' + FILE[9:-4],
            marker=dict( size=8)
            ),
            row =2, col=2)  
    
       
def addFuture_plot(path,FILE,fig,row, col,pop):
    data_covid = pd.read_csv(mypath2+'/'+FILE, header = 0, sep = ";")
    data_covid=data_covid[['date','Cases',"I"]]

    x = data_covid.date
    y1 = data_covid.Cases/pop
    #y2 = data_covid.I/pop

    fig.add_trace(go.Scatter(
            x=x, y=y1,
            name='Estimativa - '+FILE[9:-4]
            ),
            row =row, col=col)

#    fig.add_trace(go.Scatter(
#            x=x, y=y2,
#            name='Total de Infectados -'+FILE[:-4]
#            ))

    
def add_daily_plot(path,FILE,fig,row, col, pop):
    data = pd.read_csv(mypath2+'/'+FILE, header = 0, sep = ";")
    data_covid = data[["Cases","U","Q","I","S"]]
    data_covid["date"] = data["date"]
    data_covid['datetime'] = pd.to_datetime(data_covid['date'])

    
    figure = data_covid.plot(x = "datetime",
                    title = FILE[9:-4],
                    figsize = (5,4), 
                    grid = True, 
                    rot = 90)#, ylim = (0,pop*10**6))
    figure.legend(loc='center left',bbox_to_anchor=(1.0, 0.5))
    figure.set_ylabel("Individual number", family = "Serif", fontsize = 14)
    figure.set_xlabel("date", family = "Serif", fontsize = 14)
    figure.yaxis.set_major_formatter(plt.FuncFormatter(format_func))
    #ax.yaxis.set_major_formatter(plt.FuncFormatter(format_func))
    plt.show()
    plt.savefig("C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/COVID-19-Brasil/plot_sucq/"+FILE[:-4]+".png", dpi = 300,bbox_inches='tight')
    
    x = data_covid.date[1:]
    y1 = desacum(data_covid.Cases)[1:]
    
    fig.add_trace(go.Scatter(
            x=x, y=y1,
            name='Estimativa - diária - '+FILE[:-4]
            ),
        row =row, col=col)
    
mypath2 = 'C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/DADOS_estimados'
onlyfiles2 = [f for f in listdir(mypath2) if isfile(join(mypath2, f))]
    
mypath = 'C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/DADOS'
onlyfiles = [f for f in listdir(mypath2) if isfile(join(mypath, f))]

população = [["Espanha",46.72],["Itália",60.43],["SP",45.92],["MG",21.17],["RJ",17.26],["BA",14.87],["PR",11.43],["RS",11.37],["PE",9.6],["CE",9.13],["PA",8.6],["SC",7.16],["MA",7.08],["GO",7.02],["AM", 4.14],["ES",4.02],["PB",4.02],["RN",3.51],["MT",3.49],["AL", 3.4],["PI",3.3],["DF",3.1],["MS",2.8],["SE",2.3],["RO",1.78],["TO",1.6],["AC",0.9],["AP",0.85],["RR",0.61],["Brazil",210.2]]
população = np.array(população)

fig =  make_subplots(rows=2, cols=2,shared_xaxes=True, vertical_spacing=0.02, horizontal_spacing = 0.05)
estados = ["COVID-19 Brazil.CSV","COVID-19 PE.CSV", "COVID-19 CE.CSV"]


for i in estados:
    FILE = i
    for i in população:
        if i[0] == FILE[9:-4]:
            pop = float(i[1])
            
    #add_plot(path = mypath,FILE = FILE,fig=fig,row=1, col=1,pop=pop)
    
for i in onlyfiles:
    FILE = i
    for i in população:
        if i[0] == FILE[9:-4]:
            pop = float(i[1])
            
    #addFuture_plot(path = mypath2, FILE=FILE,fig=fig,row=1,col=1,pop=pop)
    add_daily_plot(path = mypath, FILE=FILE,fig=fig,row=2,col=1,pop=pop)

fig.update_layout(title_text= "Autores: Artur Coutinho, Lucas Ravellys, Lucio Camara e Silva, Maira Pitta, Anderson Franca",
                  title_font_size=12,
                  yaxis_title="Nº de casos por milhão",
                  font=dict(
                          family="Serif",
                          size=16,
                          color="black"
                          ))

fig.update_layout( yaxis_type="log", width=1400, height=800)
fig.update_yaxes(title_text="Nº de casos por milhão", row=2, col=1)

#plot(fig,filename="Predict.html")








