from mod.missing_value import miss_val
from mod.convert_to_datetype import conv_date
from mod.predict_sales import pre_sales
from mod.predict_temp import pre_temp
from mod.make_dict import make_dict
from mod.make_json import make_json
from mod.predict_sarima import pre_sarima
from mod.convert_month import conv_month
import pandas as pd
import matplotlib.pyplot as plt
import os,json,datetime
data_path="./data/ssd_12_Data/"
df=conv_date(pd.read_csv(f"{data_path}sales.csv"))
df=miss_val(df,"marginal")#marginal,median,mean
day=datetime.date(2015, 4, 1)
mid_day=datetime.date(2021, 4, 1)
df=conv_month(df,"mean")
df_temp=conv_date(pd.read_csv(f"{data_path}temp_num_M.csv"))
df_pre=pre_temp(df_temp["平均気温(℃)"].ravel(),df_temp["年月"].iloc[-1],12) 
#df_pre=pre_temp(df["平均気温(℃)"][df["date"]<day],df["date"][df["date"]<day].iloc[-1],12)
#df_pre=pre_sarima(df["0"].ravel(),(1,0,0),(2, 0, 2, 12),24,df["date"].iloc[-1])

"""
plt.plot(df["date"][df["date"]>mid_day],df["0"][df["date"]>mid_day])
#plt.plot([df["date"].iloc[-1],df_pre["date"].iloc[0]],[df["平均気温(℃)"].iloc[-1],df_pre["temp"].iloc[0]],color="b")
plt.plot(df_pre["date"],df_pre["temp"])
plt.show()
#"""

data,b=pre_sales(df[[str(i) for i in range(0,50,1)]],df_temp["平均気温(℃)"],df_pre["temp"],df_pre["date"],0)
data.to_csv("data.csv",index=False)

"""
plt.plot(df["date"],df["0"],color="c")
plt.plot([df["date"].iloc[-1],df_pre["date"].iloc[0]],[df["0"].iloc[-1],b[0]],color="c")
plt.plot(df_pre["date"],b,color="m")
plt.show()
#"""
dic=make_dict(pd.read_csv(f"{data_path}id.csv"))
#with open("a.json","w",encoding='utf-8')as f:json.dump(dic,f,indent=4,ensure_ascii=False)
make_json(data,dic)
