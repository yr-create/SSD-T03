import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from mod.missing_value import miss_val
from mod.convert_to_datetype import conv_date
#"""
from mod.predict_sales import pre_sales
from mod.predict_temp import pre_temp
from mod.make_dict import make_dict
from mod.make_json import make_json
from mod.predict_sarima import pre_sarima
from mod.care_0 import care_0
#"""
from mod.convert_month import conv_month
import matplotlib.pyplot as plt
import datetime,json,itertools,os
from sklearn.metrics import r2_score
def sarimax_forecast(data, forecast_period, last_date, sarimax_params, id):
    # データの長さを取得
    data_length = len(data)
    # SARIMAXモデルの学習
    model = SARIMAX(data, order=sarimax_params[0], seasonal_order=sarimax_params[1])
    result = model.fit()
    # 予測期間の日付リストを作成
    date_range = pd.date_range(start=last_date, periods=forecast_period, freq='M')
    # 予測を実行
    forecast_values = result.forecast(steps=forecast_period)
    # 予測結果をDataFrameに格納
    forecast_df = pd.DataFrame({"date":date_range,id: forecast_values}, index=date_range)
    return forecast_df

data_path="./data/ssd_12_Data/"
ids=[str(i) for i in range(5,50,1)]
#ids=[str(i) for i in range(0,6,1)]
df=conv_date(pd.read_csv(f"{data_path}sales.csv"))
with open("./param/seasons.json","r",encoding="utf-8")as f:seasons=json.load(f)
#df=miss_val(df,"marginal")#marginal,median,mean
df=conv_month(df,"mean")#1 or mean
df=care_0(df,seasons,ids)

for id in ids:
    season=seasons[id][0]
    data=pd.read_csv(f"./param/{id}/SARIMA_id_{id}.csv")
    data=data[data["aic"] < 3000]#[data["aic"] > 50]
    pdq_list=[tuple(int(x) for x in s.strip('()').split(', ')) for s in data["pdq"]]
    spdq_list=[tuple(int(x) for x in s.strip('()').split(', ')) for s in data["Spdq"]]
    print(pdq_list,spdq_list)
    c=0
    #data=pd.DataFrame({"pdq":pdq_list,"Spdq":spdq_list,"aic":data["aic"]})
    for pdq,Spdq,aic in zip(pdq_list,spdq_list,data["aic"].values):
        c=c+1
        if c > 50:break
        print(pdq,Spdq,season,type(pdq))
        #予測する関数
        precidt=sarimax_forecast(df[id].values,
                                 forecast_period=season,
                                 last_date=df["date"].iloc[-1],
                                 sarimax_params=[pdq,Spdq],
                                 id=id)
        #結果をプロットして保存
        path=f"./param/{id}/graph/"
        os.makedirs(path,exist_ok=True)
        plt.plot(df["date"],df[id])
        plt.plot(precidt["date"],precidt[id])
        plt.plot( [ df["date"].iloc[-1], precidt["date"].iloc[0] ],[ df[id].iloc[-1],precidt[id].iloc[0]])
        plt.savefig(f"{path}{aic}_{pdq}_{Spdq}.jpg")
        plt.close()

exit()