import pandas as pd
import numpy as np
#from statsmodels.tsa.arima.model import ARIMA
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
import datetime

def plot_graph(df,ids,path="./param/"):
    for id in ids:
        plt.plot(df["date"], df[id], label=id)
        plt.xlabel("Date")
        plt.ylabel("Sales")
        plt.xticks(rotation=45)
        plt.title(f"{id}")
        plt.savefig(f"{path}{id}/sales.png")
        plt.show()
    print("終了")

if __name__ == "__main__":
    ids=[str(i) for i in range(0,50,1)]
    ids=[str(v) for v in [9,11,12,15,25,26,27,42,43,45]]
    data_path="./data/ssd_12_Data/"
    df=conv_date(pd.read_csv(f"{data_path}sales.csv"))
    #df=miss_val(df,"marginal")#marginal,median,mean
    #df=conv_month(df,"mean")#1 or mean  
    df=pd.read_csv(f"care_0_seasonal.csv")
    #df=pd.read_csv(f"before_care_0.csv")
    plot_graph(df,ids)

"""
id="49"
data_path="./data/ssd_12_Data/"
df=conv_date(pd.read_csv(f"{data_path}sales.csv"))
#df=miss_val(df,"marginal")#marginal,median,mean
df=conv_month(df,"mean")#1 or mean
#"""

"""
# 自己相関の計算
autocorr = np.correlate(df[id].to_numpy(), df[id].to_numpy(), mode='full')
# 自己相関のプロット
ls=[c for c,i in enumerate(autocorr) if i == max(autocorr)]
print(ls)
plt.plot(autocorr)
plt.xlabel('Lag')
plt.ylabel('Autocorrelation')
plt.show()
#"""

"""
day1=datetime.date(2016, 1, 1)
day2=datetime.date(2016, 1, 1)
plt.plot(df["date"][df["date"] > day1][df["date"] < day2], df[id][df["date"] > day1][df["date"] < day2], label=id)
plt.xlabel("Date")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.savefig(f"{id}_{day1}_{day2}")
plt.show()
#"""

"""
plt.plot(df["date"], df[id], label=id)
plt.xlabel("Date")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.show()
#"""
#df[["date",id]].sort_values(id,ascending=False).to_csv(f"sort_{id}.csv",index=False)