import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from mod.missing_value import miss_val
from mod.convert_to_datetype import conv_date
"""
from mod.predict_sales import pre_sales
from mod.predict_temp import pre_temp
from mod.make_dict import make_dict
from mod.make_json import make_json
from mod.predict_sarima import pre_sarima
#"""
from mod.convert_month import conv_month
import matplotlib.pyplot as plt
import datetime,json,itertools,os
from sklearn.metrics import r2_score

def sarima_r2(df,dic,ids,path="./param/",num=100,day=datetime.date(2022, 4, 1)):
    for id in ids:
        sales=df[id]
        if False not in [type(i) == int for i in dic[id]]:
            df_param=pd.read_csv(f"{path}{id}/SARIMA_id_{id}.csv")
            pdq_ls=[tuple(map(int, i.strip("() ").split(","))) for i in df_param["pdq"][:num] ]
            Spdq_ls=[tuple(map(int, i.strip("() ").split(","))) for i in df_param["Spdq"][:num] ]
            aic_ls=[v for v in df_param["aic"][:num]]
            r2_ls=[]
            for pdq,Spdq in zip(pdq_ls,Spdq_ls):
                try:
                    model = SARIMAX(sales,#学習データ
                              order = pdq, 
                              seasonal_order=Spdq).fit()#param_seasonal
                    pre=model.predict(end=14)
                    r2_ls.append(r2_score(df[id][df["date"]>=day],pre[1:]))
                except:pass
        else:pass
        df_r2=pd.DataFrame(r2_ls,columns=["r2"])
        df_r2=pd.concat([df[:,:num],df_r2],axis=1)
        df_r2.to_csv(f"{path}{id}/r2_id_{id}.csv",index=False)
    print("終了")

#"""
data_path="./data/ssd_12_Data/"
df=conv_date(pd.read_csv(f"{data_path}sales.csv"))
df=miss_val(df,"marginal")#marginal,median,mean
df=conv_month(df,"mean")#1 or mean
ids=[str(i) for i in range(0,50,1)]
with open("./param/seasons.json","r",encoding="utf-8")as f:dic=json.load(f)

p = q =d= range(0,3)
sp = sd = sq =range(0,3)
pdq = [(x[0],x[1],x[2]) for x in list(itertools.product(p,d,q))]
dump=[]
ids=[str(v) for v in [43,45]]#9,11,12,15,25,26,27,42,
for id in ids:
    sales=df[id]
    ls=[]
    if False not in [type(i) == int for i in dic[id]]:
        season=dic[id]
        seasonal_pdq = [(x[0],x[1],x[2],season[0]) for x in list(itertools.product(sp,sd,sq))]
        for c,param in enumerate(pdq):
            for param_seasonal in seasonal_pdq:
                try:
                    mod = SARIMAX(sales,#学習データ
                              order = param, 
                              seasonal_order=param_seasonal)#param_seasonal
                    results = mod.fit()
                    ls.append([param,param_seasonal ,results.aic])
                except:continue
    else:dump.append(id)
    data=pd.DataFrame(ls,columns=["pdq","Spdq","aic"])
    data=data.sort_values("aic")
    path=f"./param/{id}/"
    os.makedirs(path,exist_ok=True)
    data.to_csv(f"{path}SARIMA_id_{id}.csv",index=False)
print(dump)
#"""

if __name__ == "__main__":
    data_path="./data/ssd_12_Data/"
    df=conv_date(pd.read_csv(f"{data_path}sales.csv"))
    df=miss_val(df,"marginal")#marginal,median,mean
    df=conv_month(df,"mean")#1 or mean
    ids=[str(i) for i in range(0,50,1)]
    with open("./param/seasons.json","r",encoding="utf-8")as f:dic=json.load(f)
    sarima_r2(df,dic, ids)