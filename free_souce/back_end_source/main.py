from mod.missing_value import miss_val
from mod.convert_to_datetype import conv_date
from mod.predict_sales import pre_sales
from mod.predict_temp import pre_temp
from mod.make_dict import make_dict
from mod.make_json import make_json
from mod.convert_month import conv_month
import pandas as pd
import os,json,datetime

df=conv_date(pd.read_csv("sales.csv"))#data2.csv
df=miss_val(df,"marginal")#marginal,median,mean
print(df)

#df.to_csv("a.csv")
df_temp=conv_date(pd.read_csv("temp_num_M.csv"))
#df_temp=conv_month(df_temp,"mean")
day=datetime.date(2015, 4, 1)

df_pre=pre_temp(df_temp["平均気温(℃)"],df_temp["年月"].iloc[-1],12)
print(df_pre)

a=pre_sales(df,list(range(0,50,1)),df["平均気温(℃)"][df["date"]>day],df["date"][df["date"]>day])
#a.to_csv("sales.csv",index=False)
dic=make_dict(pd.read_csv("id.csv"))
make_json(a,dic)