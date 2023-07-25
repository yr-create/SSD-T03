import pandas as pd
import numpy as np
#from statsmodels.tsa.arima.model import ARIMA
from mod.missing_value import miss_val
from mod.convert_to_datetype import conv_date
from mod.convert_month import conv_month
"""
from mod.predict_sales import pre_sales
from mod.predict_temp import pre_temp
from mod.make_dict import make_dict
from mod.make_json import make_json
from mod.predict_sarima import pre_sarima
#"""
import matplotlib.pyplot as plt
import datetime,json

def care_0(df,seasons,ids=[str(i) for i in range(0,50,1)]):
    """
    id_0=[]
    for id in ids:
        if (df[id] == 0).any() and False in (df[id] == 0).ravel():id_0.append(id) 
    for id in id_0:
        df_0=df[["date",id]][df[id] != 0]
        date_list=df_0["date"].toarray()
        data={}
        for date in date_list:
            data[str(date.month)]=df_0[df["date"]==date]
        for i in range(len(df[id])):
            df.loc[id].iloc[i]
    """
    id_0=[]
    for id in ids:
        if (df[id] == 0).any() and False in (df[id] == 0).ravel():id_0.append(id) 
    #with open(f"./param/seasons.json","r",encoding='utf-8')as f:seasons=json.load(f)
    for id in id_0:
        """
        df_0=df[["date",id]][df[id] != 0]
        date_list=df_0["date"]
        data={}

        for date in date_list:
            data[str(date.month)]=df[id][df["date"]==date].iloc[-1]
        print(data)
        #"""
        while (df[id] == 0).any() and False in (df[id] == 0).ravel():
            for i in range(len(df[id])):
                if df[id][i] == 0:
                    #df[id][i]=data[str(df["date"].iloc[i].month)]
                    date=df["date"][i]
                    season=seasons[id][0]
                    if datetime.date(date.year+int(int(season)/12),date.month,date.day) in df["date"].values:
                        df[id][i]=df[id][df["date"]==datetime.date(date.year+int(int(season)/12),date.month,date.day)]
    return df

if __name__ == "__main__":
    data_path="./data/ssd_12_Data/"
    df=conv_date(pd.read_csv(f"{data_path}sales.csv"))
    #df=miss_val(df,"marginal")#marginal,median,mean
    df=conv_month(df,"mean")#1 or mean
    ids=[str(i) for i in range(0,50,1)]
    #id_0=care_0(df,ids)
    ids=['4', '9', '12', '15', '25', '26', '27', '42', '43']
    
    print(df)
    df.to_csv("before_care_0.csv",index=False)
    
    with open(f"./param/seasons.json","r",encoding='utf-8')as f:seasons=json.load(f)
    df=care_0(df,seasons,ids)
    print((df!=0).any().any())
    #care_0
    """
    id_0=[]
    for id in ids:
        if (df[id] == 0).any() and False in (df[id] == 0).ravel():id_0.append(id) 
    for id in id_0:
        df_0=df[["date",id]][df[id] != 0]
        date_list=df_0["date"]
        data={}
        for date in date_list:
            data[str(date.month)]=df[id][df["date"]==date].iloc[-1]
        print(data)
        for i in range(len(df[id])):
            if df[id][i] == 0:
                df[id][i]=data[str(df["date"].iloc[i].month)]
                print(df[id][i])
    #"""

    #"""
    id_0=[]
    for id in ids:
        if (df[id] == 0).any() and False in (df[id] == 0).ravel():id_0.append(id) 
    
    with open(f"./param/seasons.json","r",encoding='utf-8')as f:
        seasons=json.load(f)

    for id in id_0:
        df_0=df[["date",id]][df[id] != 0]
        date_list=df_0["date"]
        data={}

        for date in date_list:
            data[str(date.month)]=df[id][df["date"]==date].iloc[-1]
        print(data)
        
        while (df[id] == 0).any() and False in (df[id] == 0).ravel():
            for i in range(len(df[id])):
                if df[id][i] == 0:
                    #df[id][i]=data[str(df["date"].iloc[i].month)]
                    date=df["date"][i]
                    season=seasons[id][0]
                    if datetime.date(date.year+int(int(season)/12),date.month,date.day) in df["date"].values:
                        df[id][i]=df[id][df["date"]==datetime.date(date.year+int(int(season)/12),date.month,date.day)]
    #"""

    print(df)
    df.to_csv("care_0_seasonal.csv",index=False)
    
    exit()