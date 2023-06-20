from mod.convert_to_datetype import *
import pandas as pd
import datetime,json
import numpy as np
"""
df=conv_date(pd.read_csv("sales.csv"))
shape_x,shape_y=np.shape(df)
ls=[]
dic={}
for i in df.iloc[:,0]:
    if (i.year,i.month) not in ls:
        ls.append((i.year,i.month))
        d=df[df.iloc[:,0] == i].iloc[:,1:]
        dic[f"{i.year}-{i.month}"]=np.array(d)
    else:dic[f"{i.year}-{i.month}"]=np.append(dic[f"{i.year}-{i.month}"],df[df.iloc[:,0] == i].iloc[:,1:].values,axis=0)
mean_list=np.array([])
for y,m in ls:
            name=f"{y}-{m}"
            if (y,m) == ls[0]:
                mean_num=np.mean(dic[name],axis=0).reshape([1,shape_y-1])
                mean_list=mean_num
            else:
                mean_num=np.mean(dic[name],axis=0).reshape([1,shape_y-1])
                mean_list=np.append(mean_list,mean_num,axis=0)
date_ls=[datetime.date(x[0],x[1],1) for x in ls]
df_date=pd.DataFrame(date_ls)
df_data=pd.DataFrame(mean_list)
df_return=pd.concat([df_date,df_data],axis=1)
df_return.columns=df.columns
print(df_return)
#"""

a=pd.read_csv("ARIMA_param.csv")
#print(a.head())
#print(type(a["pdq"].iloc[-1]))
#ls=[]
#for x in a["pdq"]:ls.append(x)

"""
b=a["pdq"].iloc[0]
print(b,"\n",b[1::3])
c=b.replace("(","").replace(")","").replace(" ","").split(",")
print(c)
for i in c:print(int(i))
d=[int(x) for x in c]
d=tuple(d)
print(d,type(d),type(d[0]))
#"""

ls=[]
for i in a["pdq"]:
    e=i.replace("(","").replace(")","").replace(" ","").split(",")
    f=[int(x) for x in e]
    f=tuple(f)
    ls.append(f)
print(ls)