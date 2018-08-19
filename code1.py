# -*- coding: utf-8 -*-
"""
@author: zan
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 数据表
df = pd.read_csv('CDNOW_master.txt', sep='\s+', header=None)
df.columns = ['id','date','quantity','amount']
df['date'] = pd.to_datetime(df['date'].astype(str))

# 订单金额统计描述
df['amount'].describe().round(2)

# 用户消费金额的统计描述
s = df.groupby('id')['amount'].sum()
s.describe().round(2)

# 后25%用户的贡献率
s = s.sort_values()
s[int(len(s)*0.75):].sum()/s.sum()

# 复购率
df['month'] = df['date'].values.astype('datetime64[M]')
dp = df.pivot_table(index='id', columns='month', values='amount', aggfunc='count')
dp2 = dp.applymap(lambda x : 1 if x>1 else 0 if x==1 else None )
repurchase_rate = dp2.sum()/dp2.count()

# 复购率折线图
plt.figure(figsize=(15,4))
repurchase_rate.plot()

# 用户消费周期的统计描述
s = df.groupby('id')['date'].count()
i = s[s>1].index
s1 = df.set_index(df['id'], drop=True).loc[i,:]['date']
s1.groupby('id').apply(lambda x:x.diff().dt.days).describe().round(2)

