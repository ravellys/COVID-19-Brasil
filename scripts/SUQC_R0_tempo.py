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

def Ajust_SUCQ(data_covid,pop,passo,j):    
        
    data_covid=data_covid[['DateRep','Cases']]
       
    t0 = 0
    tf = j+passo
        
    cumdata_covid = data_covid[['Cases']].cumsum()
    cumdata_cases = cumdata_covid['Cases'].values[t0:tf]
#    data=data_covid[['DateRep']].values[t0:tf]
#    day_last = data[-1:][0][0]
    
    data = data_covid[['DateRep']].values[t0:tf][-1:][0][0]
    day_last_str = data[-4:]+'-'+data[3:5]+'-'+data[:2]
    day_last = day_last_str#np.array(day_last_str, dtype=np.datetime64)
    
    t = np.linspace(1,len(cumdata_cases),len(cumdata_cases))
    N = pop*10**6
    alfa_0,beta_0,gama1_0= [.8/N,.1,.19] 
    So,Uo,Qo,Co = [.8*N,6*cumdata_cases[0],cumdata_cases[0],cumdata_cases[0]]

    p0 = [alfa_0,beta_0,gama1_0,So,Uo,Qo,Co] 
    bsup = [1/N,1,1,N,Uo*1.5,Qo*1.2,Co+10**-9]
    binf = [0,0,0,.5*N,Uo*.5,Qo*0.8,Co-10**-9]
    
    popt = ajust_curvefit(t,cumdata_cases,p0,bsup,binf)
    p0 = popt
    popt = min_minimize(cumdata_cases,sucq_solve,p0,t,bsup,binf)
    alfa_0,beta_0,gama1_0,So,Uo,Qo,Co = popt 
    
    solution = SUCQ(t,alfa_0,beta_0,gama1_0,So,Uo,Qo,Co)
    NSE = hy.nse(np.log10(cumdata_cases),np.log10(solution[:,3]))
    if NSE >= 0.5:
        return [alfa_0*N/gama1_0, day_last]
    else:
        return [ np.nan, day_last]
 
  
população = [["Espanha",46.72],["Itália",60.43],["SP",45.92],["MG",21.17],["RJ",17.26],["BA",14.87],["PR",11.43],["RS",11.37],["PE",9.6],["CE",9.13],["Pará",8.6],["SC",7.16],["MA",7.08],["GO",7.02],["AM", 4.14],["ES",4.02],["PB",4.02],["RN",3.51],["MT",3.49],["AL", 3.4],["PI",3.3],["DF",3.1],["MS",2.8],["SE",2.3],["RO",1.78],["TO",1.6],["AC",0.9],["AM",0.85],["RR",0.61],["Brasil",210.2]]
população = np.array(população)

mypath = 'C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/Dados_site'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

#import mensured data
passo = 10
fig,ax = plt.subplots(1, 1)

for i in onlyfiles:
    FILE = i
    cont = 0
    R = []

    for p in população:
        if p[0] == FILE[9:-4]:
            pop = float(p[1])
    
    data_covid = pd.read_csv("DADOS/"+FILE, header = 0, sep = ";")
    for j in range(len(data_covid)-passo+1):
        ajust = Ajust_SUCQ(data_covid,pop,passo,j)
        if ajust == None:
            print(ajust)
        else:
            R.append(ajust)       
    R = np.array(R)
    df_R = pd.DataFrame(R, columns = [FILE[9:-4],"data"])
    df_R['datetime'] = pd.to_datetime(df_R['data'])
    df_R = df_R.set_index('datetime')
    df_R=df_R[[FILE[9:-4]]].astype(float)

    df_R.to_csv("C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/R0_data/"+FILE,sep=";")
    figure = df_R.plot(ax = ax, kind = "line",style = 'o-',grid = True,rot = 90,figsize= (8,6))

figure.tick_params(axis = 'both', labelsize  = 14)
figure.set_title("Número de Reprodutividade do vírus", family = "Serif", fontsize = 18)
figure.set_xlabel(" ")

im_ufpe = plt.imread(get_sample_data('C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/imagens/ufpe_logo.png'))

dia = df_R.index.values[-1:][0].astype(str)[:10]
newax0 = fig.add_axes([.025,-.15, 1, 1], anchor='NE')
newax0.text(.1, .1,"Fonte dos dados: Ministério da Saúde do Brasil \nAutores: Artur Coutinho, Lucas Ravellys, Lucio Camara e Silva, Maira Pitta, Anderson Almeida\nData da atualização: "+dia, family = "Verdana")
newax0.axis('off')

newax2 = fig.add_axes([.175,.725, 0.15, 0.15], anchor='NW')
newax2.imshow(im_ufpe)
newax2.axis('off')

plt.show()

fig.savefig('C:/Users/ravel/OneDrive/Área de Trabalho/DataScientist/sklearn/COVID-19/CasosPorEstado/imagens/daily_R0.png', dpi = 300,bbox_inches='tight',transparent = True)
    
    
#df_R['datetime'] = pd.to_datetime(df_R['data'])
#
#fig, ax = plt.subplots()
#df_r1 = df_R.groupby('estado')
#
#A=pd.pivot_table(df_R, values = 'R0', 
#                 columns = ['estado'], 
#                 index = ['datetime'])
#
#df_r1.plot(ax = ax,x='datetime', y='R0',rot = 90)
