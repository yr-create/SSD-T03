import pandas as pd
import datetime
import numpy as np
def conv_month(df,mode=1):
    if mode == 1 or mode == "1":
        ls=[]
        for i in df.iloc[:,0]:
            if i.day== 1:ls.append(i)
        return df[df.iloc[:,0] == ls]
    if mode == "mean":
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
        return df_return