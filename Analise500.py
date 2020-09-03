import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

### IMPORTAR OS DADOS
dados = pd.read_excel('DadosMilho.xlsx',sheet_name='Plan 1')
dia_inicial = 0
distancia_entre_dias = 3000
valores_dolar = list(dados['US$'][dia_inicial:dia_inicial+distancia_entre_dias])#len(dados)//8])
novo_valores = [0]*len(valores_dolar)

num_predic = 5
valores_futuros = list(dados['US$'][dia_inicial:dia_inicial+distancia_entre_dias+num_predic])
novo_valoresf = [0]*len(valores_futuros)

## FAZER A NORMALIZAÇÃO
for i in range(len(valores_dolar)-1):
    novo_valores[i] = (valores_dolar[i+1]-valores_dolar[i])/valores_dolar[i+1]
    
## FAZER A NORMALIZAÇÃO DOS DADOS COM O FUTURO
for i in range(len(valores_futuros)-1):
    novo_valoresf[i] = (valores_futuros[i+1]-valores_futuros[i])/valores_futuros[i+1]


### CALCULO DA FFT
Fs = len(novo_valores)
t = np.arange(0, Fs, 1) ##ANO TEM APROXIMADAMENTE 250 DIAS
n = np.size(t)
fr = (n/2)*np.linspace(0, 1, n//2)

X  = np.fft.fft(novo_valores)
Xm = (2/Fs)*abs(X[0:np.size(fr)])


### PEGAR MENORES FREQUÊNCIAS

n = len(novo_valores)
n_harm = 12               # numero de harmonicos 
t = np.arange(0, n)
p = np.polyfit(t, novo_valores, 1)         # Econtra a tendência
ativo_notrend = novo_valores       # Retira o componente da tendência
ativo_freqdom = np.fft.fft(ativo_notrend)  # Os valores estacionários transformados com Fourier
f = np.fft.fftfreq(n)              # Frequências
indexes = list(range(n))
# organiza da menor pra maior frenquencia
indexes.sort(key = lambda i: np.absolute(f[i]))
 
t = np.arange(0, n + num_predic)
restored_sig = np.zeros(t.size)
for i in indexes[:1 + n_harm * 2]:
    ampli = np.absolute(ativo_freqdom[i]) /n   # amplitude
    fase = np.angle(ativo_freqdom[i])          # angulo
    restored_sig += ampli * np.cos(2 * np.pi * f[i] * t + fase)

extrapolacao = restored_sig 



### PLOTAR OS GRÁFICOS
fig =  make_subplots(rows=3, cols= 1)
fig.append_trace(go.Scatter(x = np.array(range(len(dados))), y = valores_dolar, name= "Variação do preço normalizada"),row= 1, col= 1)
fig.append_trace(go.Scatter(x=fr,y=Xm, name = 'Espectro de frequência'), row=2, col=1)
fig.append_trace(go.Scatter(x=np.array(range(len(valores_futuros))),y=np.array(novo_valoresf)*100,name = "Variação"), row=3, col=1)
fig.show()