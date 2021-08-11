%reset -f
import pandas as pd
import numpy as np
import time
import os
from os.path import join

#Raw Data from TEJ
start_ = time.time()
path = os.getcwd()
df = pd.read_csv(join(path,'Raw Data.csv')).drop(columns=['Data Field'])
df['年月日'] = pd.to_datetime(df['年月日'])
df = df.set_index('年月日')

#交易資料
df1 = pd.read_excel(join(path,'TWII.xlsx'))
df1['年月日'] = pd.to_datetime(df1['年月日'])
df1 = df1.set_index('年月日')
df1 = df1.rename(columns = {'開盤價(元)' : 'open', 
            '最高價(元)' : 'high',
            '最低價(元)' : 'low',
            '收盤價(元)' : 'close',
            '成交量(千股)': 'volumn', 
            '成交值(千元)' : 'value'})

import talib
from talib import abstract
#KD判斷多空
K,D = talib.STOCH(high = np.array(df1['high']), 
            low = np.array(df1['low']), 
            close = np.array(df1['close']),
            fastk_period=9,
            slowk_period=3,
            slowk_matype=0,
            slowd_period=3,
            slowd_matype=0)
df1['K'] = K
df1['D'] = D
#k>d:黃金交叉>>>>多頭
#k<d:死亡交叉>>>>空頭
df1['signal'] = 'nan'
for i in range(12,len(df1)):
    k = df1['K'][i]
    d = df1['D'][i]
    if k>d:
        df1['signal'][i] = 1
        df1['signal_buy'] = ((np.roll(df1['signal'].astype(float), 1) - df1['signal'].astype(float)) == -2).replace(True ,1)
    if k<d:
        df1['signal'][i] = -1
        df1['signal_sell'] = ((np.roll(df1['signal'].astype(float), 1) - df1['signal'].astype(float)) == 2).replace(True ,-1)

#df.columns
ticker = '2412 中華電'
df1[[ticker,'0050 元大台灣50', '0051 元大中型100']] = df[[ticker,'0050 元大台灣50', '0051 元大中型100']]
df1 = df1.drop(columns=['證券代碼']).astype(float)
df2 = df1[(df1['signal_buy']==1)|(df1['signal_sell']==-1)]
df2 = df2[[ticker, '0050 元大台灣50', '0051 元大中型100','close','signal']]
df2 = df2.rename(columns = {'close':'台灣加權指數'})
#%%
#計算報酬率
df2['return_'+ticker] = (df2[ticker].shift(-1) - df2[ticker])/df2[ticker]
df2['return_0050 元大台灣50'] = (df2['0050 元大台灣50'].shift(-1) - df2['0050 元大台灣50'])/df2['0050 元大台灣50']
df2['return_0051 元大中型100'] = (df2['0051 元大中型100'].shift(-1) - df2['0051 元大中型100'])/df2['0051 元大中型100']
df2['return_台灣加權指數'] = (df2['台灣加權指數'].shift(-1) - df2['台灣加權指數'])/df2['台灣加權指數']
df3 = df2[df2['signal'] == 1].sum()
df3 = df3[5:]
df3 = pd.DataFrame(df3)
df3 = df3.rename(columns = {0:'Total Return'})
df2.to_csv('buy_sell data.csv',encoding='utf-8-sig')
df3.to_csv('result.csv',encoding = 'utf-8-sig')
