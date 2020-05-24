import pandas as pd
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cbook import get_sample_data
from matplotlib.ticker import FuncFormatter
from math import log10, floor

def format_func(value, tick_number=None):
    num_thousands = 0 if abs(value) < 1000 else floor (log10(abs(value))/3)
    value = round(value / 1000**num_thousands, 0)
    return f'{value:g}'+' KMGTPEZY'[num_thousands]

def desacum(X):
    a = [X[0]]
    for i in range(len(X)-1):
        a.append(X[i+1]-X[i])
    return a

mypath = 'C:/Users/ravellys/Documents/GitHub/COVID-19-Brasil/COVID-19-Brasil/data/DADOS_estimados'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

população = [["Espanha",46.72],["Itália",60.43],["SP",45.92],["MG",21.17],["RJ",17.26],["BA",14.87],["PR",11.43],["RS",11.37],["PE",9.6],["CE",9.13],["PA",8.6],["SC",7.16],["MA",7.08],["GO",7.02],["AM", 4.14],["ES",4.02],["PB",4.02],["RN",3.51],["MT",3.49],["AL", 3.4],["PI",3.3],["DF",3.1],["MS",2.8],["SE",2.3],["RO",1.78],["TO",1.6],["AC",0.9],["AP",0.85],["RR",0.61],["Brazil",210.2]]
população = np.array(população)
estados = ["COVID-19 Brazil.CSV","COVID-19 PE.CSV", "COVID-19 CE.CSV", "COVID-19 AM.CSV", "COVID-19 DF.CSV", "COVID-19 PR.CSV", "COVID-19 SP.CSV", "COVID-19 RJ.CSV"]


fig,ax = plt.subplots(1, 1)
ax.set_xlim(np.array("2020-02-28", dtype=np.datetime64), np.array("2020-04-04", dtype=np.datetime64))

for i in estados:
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
    figure.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y))) 


figure.tick_params(axis = 'both', labelsize  = 14)
#figure.set_title("Predict percent daily cases", family = "Serif", fontsize = 18)
figure.set_title("percentage of the daily cases", family = "Serif", fontsize = 18)
figure.set_xlabel(" ")
figure.legend(loc='center left',bbox_to_anchor=(1.0, 0.5))

plt.show()

file_out = 'C:/Users/ravellys/Documents/GitHub/COVID-19-Brasil/COVID-19-Brasil/imagens/daily_cases.png'
fig.savefig(file_out, dpi = 300,bbox_inches='tight')
###################################### 


inf = []

for i in onlyfiles:
    FILE = i
    for i in população:
        if i[0] == FILE[9:-4]:
            pop = float(i[1])
           
    fig,ax = plt.subplots(1, 1)

    data = pd.read_csv(mypath+'/'+FILE, header = 0, sep = ";")
    data_covid = data[["Cases","S","U","Q","I"]]
    data_covid["date"] = data["date"]
    data_covid[FILE[9:-4]] = desacum(data_covid["Cases"])
    data_covid['datetime'] = pd.to_datetime(data_covid['date'])
    
    max_cases = max(data_covid[FILE[9:-4]])
    for i in range(len(data_covid)):
        if data_covid[FILE[9:-4]][i] == max_cases:
            pos_max = i
    max_day = data_covid["datetime"][pos_max]
    
    if pos_max < i:
        inf.append([FILE[9:-4], max_cases, pos_max, max_day])

    
    figure = data_covid.plot(ax =ax,kind = "line", x = "datetime", y = FILE[9:-4],
                             grid = True,rot = 90,figsize= (8,6))
    figure.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0}'.format(y))) 


    figure.tick_params(axis = 'both', labelsize  = 14)
    figure.set_title("Daily cases - " + FILE[9:-4] , family = "Serif", fontsize = 18)
    figure.set_xlabel(" ")
    figure.yaxis.set_major_formatter(plt.FuncFormatter(format_func)) 
    figure.legend(loc='center left',bbox_to_anchor=(1.0, 0.5))
    plt.show()
    
    file_out = 'C:/Users/ravellys/Documents/GitHub/COVID-19-Brasil/COVID-19-Brasil/imagens/daily_cases/'
    fig.savefig(file_out+ FILE[9:-4]+'.png', dpi = 300,bbox_inches='tight')

inf = np.array(inf)
df_inf = pd.DataFrame(inf, columns = ["Estado","max_cases","diamax","datamax"])
path_out ='C:/Users/ravellys/Documents/GitHub/COVID-19-Brasil/COVID-19-Brasil/'
df_inf.to_csv(path_out+"inf_max_day.csv",sep=";")

def bar_plt(atributo, title_name,df,logscale):
    fig, ax = plt.subplots(1, 1)
    df = df.sort_values(by=[atributo])

    figure = df.plot.bar(ax =ax, x = "Estado", y = atributo, figsize = (15,8), legend = None,width=.75, logy = logscale)
    figure.set_xlabel(" ")
    figure.set_title(title_name, family = "Serif", fontsize = 22)
    figure.tick_params(axis = 'both', labelsize  = 14)
#    figure.yaxis.set_major_formatter(plt.FuncFormatter(format_func)) 
#
#    for p in ax.patches:
#       b = p.get_bbox()
#       val = format_func(b.y1 + b.y0,1)        
#       ax.annotate(val, ((b.x0 + b.x1)/2, b.y1), fontsize = 14,ha='center', va='top',rotation = 90)
#  
    plt.show()
    path_out ="C:/Users/ravellys/Documents/GitHub/COVID-19-Brasil/COVID-19-Brasil/imagens/"
    fig.savefig(path_out+atributo+'_barplot.png', dpi = 300,bbox_inches='tight')

bar_plt(atributo = "diamax", title_name = "Number of days between start of adjustment \nand the peak of the epidemic", df = df_inf, logscale = True)
bar_plt(atributo = "max_cases", title_name = "Maximum number of daily cases", df = df_inf, logscale = True)
