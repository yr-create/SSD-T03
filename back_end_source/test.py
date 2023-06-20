from mod.missing_value import miss_val
from mod.convert_to_datetype import conv_date
from mod.predict_sales import pre_sales
from mod.predict_temp import pre_temp
from mod.make_dict import make_dict
from mod.make_json import make_json
from mod.convert_month import conv_month
import pandas as pd
import matplotlib.pyplot as plt
import os,json,datetime

df=conv_date(pd.read_csv("data2.csv"))
df=miss_val(df,"marginal")#marginal,median,mean
#df.to_csv("a.csv")
day=datetime.date(2015, 4, 13)
#df_pre=pre_temp(df["平均気温(℃)"][df["date"]<day],df["date"][df["date"]<day].iloc[-1],12)
df_pre=pre_temp(df["平均気温(℃)"],df["date"].iloc[-1],24)
"""
print(df_pre)#["date"],["temp"]
plt.plot(df["date"],df["平均気温(℃)"])
plt.plot([df["date"].iloc[-1],df_pre["date"].iloc[0]],[df["平均気温(℃)"].iloc[-1],df_pre["temp"].iloc[0]],color="b")
plt.plot(df_pre["date"],df_pre["temp"])
plt.show()
#"""

#"""
a,b=pre_sales(df,list(range(0,2,1)),df_pre["temp"],df_pre["date"],0)
#a.to_csv("sales.csv",index=False)

"""
plt.plot(df["date"],df["0"],color="c")
plt.plot([df["date"].iloc[-1],df_pre["date"].iloc[0]],[df["0"].iloc[-1],b[0]],color="c")
plt.plot(df_pre["date"],b,color="m")
plt.show()

#"""
dic=make_dict(pd.read_csv("id.csv"))
make_json(a,dic)
#"""