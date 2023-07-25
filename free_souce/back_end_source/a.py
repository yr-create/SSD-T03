import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from mod.missing_value import miss_val
from mod.convert_to_datetype import conv_date
from mod.predict_sales import pre_sales
from mod.predict_temp import pre_temp
from mod.make_dict import make_dict
from mod.make_json import make_json
from mod.predict_sarima import pre_sarima
from mod.convert_month import conv_month
from mod.care_0 import care_0
import matplotlib.pyplot as plt
import datetime
import statsmodels.api as sm

def sarimax_forecast(data, forecast_period, last_date, sarimax_params):
    # データの長さを取得
    data_length = len(data)

    # SARIMAXモデルの学習
    model = sm.tsa.SARIMAX(data, order=sarimax_params[0], seasonal_order=sarimax_params[1])
    result = model.fit()

    # 予測期間の日付リストを作成
    date_range = pd.date_range(start=last_date, periods=forecast_period, freq='M')

    # 予測を実行
    forecast_values = result.forecast(steps=forecast_period)

    return forecast_values, date_range


def forecast_sales(data, num_months):
    # 日付列と商品ID列を取得
    dates = data.columns[0]
    ids = data.columns[1:]
    last_date = data[dates].iloc[-1]
    # 予測期間の毎月の日付リスト
    forecast_dates = pd.date_range(last_date, periods=num_months, freq='MS')
    # 各商品の売上をARIMAモデルで予測
    ls=[]
    for id in ids:
        sales = data[id]
        model = ARIMA(sales, order=(1, 0, 0))  # ARIMAの次数は適宜調整してください
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=num_months)#[0]
        ls.append([int(x) for x in forecast])
    sales_list=[]
    for i in range(num_months):
        pool=[]
        for j in ls:pool.append(j[i])    
        sales_list.append(pool)
    df_id = pd.DataFrame(data=[str(x) for x in ids], columns=["id"])
    #forecast_data = pd.DataFrame(data=sales_list,index=forecast_dates, columns=ids)
    forecast_data = pd.DataFrame(data=ls,columns=[d.date() for d in forecast_dates])
    return pd.concat([df_id,forecast_data],axis=1)

if __name__ =="__main__":

    data_path="./data/ssd_12_Data/"
    df=conv_date(pd.read_csv(f"{data_path}sales.csv"))
    df=care_0(df)#marginal,median,mean

    # 売上の予測
    forecast = sarimax_forecast(df, forecast_period=12,)

    # 予測データと学習データの比較グラフの作成
    forecast_dates = forecast.columns[1:]  # 予測期間の日付リスト
    ids = forecast["id"].values  # 商品IDのリスト
    





    for c,id in enumerate(ids):
        if c > 5:break
        # 予測データの取得
        forecast_data = forecast.loc[forecast["id"] == id, forecast_dates].values[0]

        # 学習データの取得
        df_train=df[df["date"] > datetime.date(2021,4,1)]
        train_data = df_train[id].values

        # グラフの作成
        plt.plot(forecast_dates, forecast_data, label="Forecast")
        plt.plot(df_train["date"], train_data, label="Train")
        plt.xlabel("Date")
        plt.ylabel("Sales")
        plt.title(f"Sales Forecast Comparison (ID: {id})")
        plt.legend()
        plt.xticks(rotation=45)
        plt.show()