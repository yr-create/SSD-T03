import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

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