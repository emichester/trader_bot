"""
https://www.macrotrends.net/stocks/charts/CSV/carriage-services/stock-price-history

https://www.lawebdelprogramador.com/foros/Python/1548513-Derivadas-numericas.html
https://stackoverflow.com/questions/10345278/understanding-lambda-in-python-and-using-it-to-pass-multiple-arguments
https://matplotlib.org/2.1.1/api/_as_gen/matplotlib.pyplot.plot.html
"""
import pandas as pd
from pandas.core.arrays.sparse import dtype
import numpy as np
import matplotlib.pyplot as plt

def diff(x,y) : return np.diff(y)/np.diff(x)

path = "/home/emilio/PaginasWeb/trader_API/data/MacroTrends_Data_Download_GME.csv"

df = pd.read_csv(path, skiprows=14)

# print(df)

res = df['open']
y = res.to_numpy(dtype=np.float32)
x = [i for i in range(len(y))]
x = np.array(x,dtype=np.float32)
dy = diff(x,y)
ddy = diff(x[1:],dy)
dddy = diff(x[2:],ddy)

# plt.plot(x[3:],res[3:], color='r')
# plt.plot(x[3:],dy[2:], color='b')
# plt.plot(x[3:],ddy[1:], color='g')
# plt.plot(x[3:],dddy, color='y')
# plt.show()

path = "/home/emilio/PaginasWeb/trader_API/debug.log"
with open(path,'r') as f:
    text = f.read().splitlines()

STOCK = 'UAVS'

val = []
for line in text:
    if line.find('%s Precio:'%STOCK) >= 0:
        price = line[line.find('%s Precio:'%STOCK):].split(' ')[2]
        val.append(float(price))

res = np.array(val,dtype=np.float32)
y = res#.to_numpy(dtype=np.float32)
x = [i*10 for i in range(len(y))]
x = np.array(x,dtype=np.float32)
dy = diff(x,y)
ddy = diff(x[1:],dy)
dddy = diff(x[2:],ddy)

print(y)

plt.plot(x[3:],res[3:], color='r')
plt.plot(x[3:],dy[2:], color='b')
plt.plot(x[3:],ddy[1:], color='g')
plt.plot(x[3:],dddy, color='y')
plt.show()