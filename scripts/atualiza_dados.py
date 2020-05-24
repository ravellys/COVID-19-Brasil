import pandas as pd 
import numpy as np
import requests 

def baixar_arquivo(url, endereco):
    resposta = requests.get(url)
    if resposta.status_code == requests.codes.OK:
        with open(endereco, 'wb') as novo_arquivo:
                novo_arquivo.write(resposta.content)
        print("Download finalizado. Arquivo salvo em: {}".format(endereco))
    else:
        resposta.raise_for_status()

link = 'https://mobileapps.saude.gov.br/esus-vepi/files/unAFkcaNDeXajurGB7LChj8SgQYS2ptm/4320f637fbf33d5a47834ea7c114a995_Download_COVID19_20200419.csv'

baixar_arquivo(link,"C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/att.csv")
 
file ="C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/att.csv"       
df = pd.read_csv(file,header = 0, sep = ";")

nome_data = 'data'
nome_estado = 'estado'

data = df[nome_data]
path_out = "C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/DADOS/"

A=pd.pivot_table(df, values = 'casosNovos', 
                 columns = [nome_estado],
                 aggfunc=np.sum)
estados = A.columns


length = len(df)-1

#day_0_str=df[nome_data][0][:4]+'-'+df[nome_data][0][5:7]+'-'+df[nome_data][0][-2:]
#day_last_str=df[nome_data][length][:4]+'-'+df[nome_data][length][5:7]+'-'+df[nome_data][length][-2:]

day_last_str=df[nome_data][length][-4:]+'-'+df[nome_data][length][3:5]+'-'+df[nome_data][length][:2]

def _day_0(df,nome_data):
    day_0_str=df[nome_data].values[0][-4:]+'-'+df[nome_data].values[0][3:5]+'-'+df[nome_data].values[0][:2]
    return np.array(day_0_str, dtype=np.datetime64)

day_0 = _day_0(df,nome_data)
day_last = np.array(day_last_str, dtype=np.datetime64)

n=0
delta_day = day_last - day_0
delta_day = delta_day.astype(int)+1

for i in range(27):
    df_estado = df[n:n+delta_day]
    n = delta_day*(i+1)
    
    f_case = 0
    while(df_estado["casosAcumulados"].values[f_case]==0):
        f_case = f_case+1
    
    df_estado = df_estado[f_case:]
    s_e = df_estado[nome_estado].values[0]
    
    df_estado.columns = ['regiao','estado',	'DateRep', 'Cases','cum-Cases','Deaths','cum-Deaths']
   
    df_estado["DateRep"] = _day_0(df_estado,'DateRep') +np.arange(len(df_estado))
    df_estado.to_csv(path_out+ "COVID-19 "+ s_e + ".csv", sep = ";",index = False)

Serie = []
for j in range(27):
    for i in range (delta_day):
     Serie.append(i)  

df["ordem"] = Serie

df_brasil = pd.pivot_table(df, values = ["casosNovos","casosAcumulados","obitosNovos","obitosAcumulados"], index = "ordem", aggfunc = np.sum)
df_brasil['DateRep'] = day_0 + np.arange(delta_day)

f_case = 0
while(df_brasil["casosAcumulados"].values[f_case]==0):
    f_case = f_case+1

df_brasil = df_brasil[f_case:] 
df_brasil.columns = ['cum-Cases','Cases','cum-Deaths','Deaths','DateRep']
df_brasil.to_csv(path_out+ "COVID-19 "+ "Brazil" + ".csv", sep = ";",index = False)
   
