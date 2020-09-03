import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


num_predic = 500
n_harm = 10
dados = pd.read_excel('DadosMilho.xlsx',sheet_name='Plan 1')
dia_inicial = 2750
distancia_entre_dias = 1000
valores_dolar = list(dados['R$'][dia_inicial:dia_inicial+distancia_entre_dias])

ativo = valores_dolar

Fs = np.float(len(ativo)) #Numero de pontos
t = np.arange(0, Fs, 1)

x0 = ativo #- sum(ativo)/Fs
p = np.polyfit(t, ativo, 1)
x1 = ativo - p[0]*t - p[1]
#varx1 = [0]*len(x1)
#for i in range(1,len(x1)-1):
#    varx1[i] = x1[i]-x1[i-1] 

fig =  make_subplots(rows=3, cols= 1)

fig.append_trace(go.Scatter(x = t, y = x0, name= "Preço [U$]"),row= 1, col= 1)
fig.append_trace(go.Scatter(x = t, y = p[0]*t+p[1], name= "Tendência"),row= 1, col= 1)

fig.append_trace(go.Scatter(x = t, y = x1, name= "Variação sem tendência"),row= 2, col= 1)

#Eixo das frequências

n = np.size(t)
#fr = (Fs/2.0)*np.linspace(0.0,1.0, n/2.0)
fr = np.fft.fftfreq(len(ativo))


#Calcular a fft

X  = np.fft.fft(x1)
Xm = (2/n)*abs(X[0:np.size(fr)])


indexes = list(range(n))
# organiza da menor pra maior frenquencia
indexes.sort(key = lambda i: np.absolute(fr[i]))
t = np.arange(0, n + num_predic)
restored_sig = np.zeros(t.size)

ativo_freqdom = X

for i in indexes[:1 + n_harm * 2]:
    ampli = np.absolute(ativo_freqdom[i]) / n   # amplitude
    fase = np.angle(ativo_freqdom[i])          # angulo
    if ampli > 2:
        restored_sig += ampli * np.cos(2 * np.pi * fr[i] * t + fase)


fig.append_trace(go.Scatter(x = t[:1000], y = restored_sig[:1000], name= "Soma das harmonicas"),row= 2, col= 1)

    
    
fig.append_trace(go.Scatter(x = abs(fr), y = Xm, name= "Espectro de Frequência"),row= 3, col= 1)
fig.append_trace(go.Scatter(x = abs(fr), y = Xm, name= "Espectro de Frequência", mode='markers'),row= 3, col= 1)


fig.show()