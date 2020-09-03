import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


dados = pd.read_excel('DadosMilho.xlsx',sheet_name='Plan 1')
dia_inicial = 1750
distancia_entre_dias = 2000
ativo = list(dados['R$'][dia_inicial:dia_inicial+distancia_entre_dias])


Fs = len(ativo) #Numero de pontos
t = np.arange(0, Fs, 1)

x0 = ativo #- sum(ativo)/Fs
p = np.polyfit(t, ativo, 1)

x1 = ativo - p[0]*t  #### PREÇO SEM A TENDÊNCIA

x2 = x1-p[1] ### PREÇO SEM A TENDÊNCIA OSCILANDO EM TORNO DO 0


fig =  make_subplots(rows=1, cols= 1)

fig.append_trace(go.Scatter(x = t, y = x0, name= "Preço [U$]"),row= 1, col= 1)
fig.append_trace(go.Scatter(x = t, y = x1, name= "Preço sem tendência[U$]"),row= 1, col= 1)
fig.show()