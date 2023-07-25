# 必要なライブラリのインポート
from statsmodels.tsa import stattools as st
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.arima_model import ARMA,ARIMA
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
# 基本的なライブラリ
import datetime,os
import numpy as np
from dateutil.relativedelta import relativedelta
from mod.convert_to_datetype import conv_date
from mod.convert_month import conv_month
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.metrics import r2_score

path=f"./data/ssd_12_Data/"
df=conv_date(pd.read_csv(f"{path}temp_num_M.csv"))
df.columns=['date', '平均気温(℃)', '日最高気温35℃以上日数(日)', '日最低気温25℃以上日数(日)', '平均湿度(％)']
df_sales=conv_date(pd.read_csv(f"{path}sales.csv"))
df_sales=conv_month(df_sales,"mean")#1 or mean
#df_sales.to_csv("df_sales.csv",index=False)
day=datetime.date(2022, 4, 1)
mid_day=datetime.date(2020, 4, 1)
id="0"
train=df["平均気温(℃)"][df["date"]<day].ravel()
train_sales=df_sales[id][df_sales["date"]<day].ravel()
exogenous=df['平均湿度(％)'][df["date"]<day].ravel()
season=12

"""
plt.rc("figure", figsize = (12,6))
# x 軸がどの程度ずらしているかをあらわし、y軸に相関の強さを表している
sm.graphics.tsa.plot_acf(df["平均気温(℃)"],lags = 35)
sm.tsa.seasonal_decompose(df["平均気温(℃)"].values,period=12).plot()
plt.show()
#"""

"""ARIMA param
import itertools
p = q =d= range(0,10)
# p,q,sp,sqの組み合わせのリストを作成
pdq = [(x[0],x[1],x[2]) for x in list(itertools.product(p,d,q))]
ls=[]
a="-----------------------------------------------"
for c,param in enumerate(pdq):
        print(f"{a}\nstetas:{c/len(pdq)*100}%")
        try:
            mod = ARIMA(train_sales,
                          order = param)
            results = mod.fit()
            pre=results.predict(end=14)
            r2=r2_score(df_sales[id][df_sales["date"]>=day],pre[1:])
            if r2 > 0:
                ls.append([param,  results.aic,r2])
        except:
            continue
data=pd.DataFrame(ls,columns=["pdq","aic","r2"])
data=data.sort_values("r2",ascending=False)
path=f"./param/{id}/"
os.makedirs(path,exist_ok=True)
data.to_csv(f"{path}ARIMA_id_{id}.csv",index=False)
#"""

"""ARIMA param
# モデルの優劣の判定にAICという基準を使う
min_aic = 30000
# 最もAICがよかった（小さかった）p,d,qを格納する
min_pdq = []
for p in range(4,7):
    for d in range(0,3):
        for q in range(1,3):
            model_arima =ARIMA(train_sales,
                               order = [p,d,q])
            try:
                result_arima = model_arima.fit()#method_kwargs={'maxiter':10000}
            except:
                print(p,d,q,"では収束しませんでした")
                continue
            result_arima_aic = result_arima.aic
            print(p,d,q,result_arima_aic)
            if result_arima_aic < min_aic:
                #min_aic = result_arima_aic
                min_pdq.append([p,d,q])
print(min_pdq)#temp[4,0,2], sales_id=0[6, 0, 1],[4, 0, 1], [5, 0, 1]
#"""

"""ARIMA plot temp
model_arima =ARIMA(train,order = [4,0,2]).fit()
prediction_arima=model_arima.predict(end=14)
plt.plot(df["date"][df["date"]>=mid_day], df["平均気温(℃)"][df["date"]>=mid_day])
plt.plot(df["date"][df["date"]>=day],prediction_arima[1:])
plt.show()
print(model_arima.aic)
#"""

"""ARIMA plot sales.id=0
model_arima1 =ARIMA(train_sales,order = [0, 1, 0]).fit()
prediction_arima1=model_arima1.predict(end=14)
plt.plot(df_sales["date"][df_sales["date"]>=mid_day], df_sales[id][df_sales["date"]>=mid_day])
plt.plot(df_sales["date"][df_sales["date"]>=day],prediction_arima1[1:])
r2=r2_score(df_sales[id][df_sales["date"]>=day],prediction_arima1[1:])
plt.title(f"R^2_score={r2}")
plt.show()
print(model_arima1.aic)
#"""

"""SARIMA param
import itertools
# SARIMAのseasonal成分のパラメータを推定するために、各パラメータのパターンを作る
p = range(0, 4)
d = range(0, 4)
q = range(0, 4)
#周期性は12 or 72 or etc
seasonal_pdq = [(x[0], x[1], x[2], season) for x in list(itertools.product(p, d, q))]
pdq = list(itertools.product(p, d, q))
best_param_seasonal = []
best_bic = 100000
best_aic=3000
best_param = (6,0,1)#ARIMAで推定したパラメーター
for param_seasonal in seasonal_pdq:
  try:
    mod = sm.tsa.statespace.SARIMAX(df["平均気温(℃)"][df["date"]<day].ravel(),
                                    order = best_param,
                                    seasonal_order = param_seasonal,
                                    enforce_stationarity = False,
                                    enforce_invertibility = False)
    results = mod.fit()
    if best_aic > results.aic:
        best_param_seasonal.append(param_seasonal)
        aic_pool=results.aic
        #best_aic=results.aic
  except:
    continue
#print('*BEST ARIMA{}x{} - BIC:{}'.format(best_param, best_param_seasonal, best_bic))
print(best_param_seasonal,aic_pool)
#BEST ARIMA(4, 0, 2)x(0, 2, 2, 12)
#"""

#"""SARIMA param
train_sales=df_sales[id][df_sales["date"]<day].ravel()
import itertools
p = q =d= range(0,3)
sp = sd = sq =range(0,3)
# p,q,sp,sqの組み合わせのリストを作成
pdq = [(x[0],x[1],x[2]) for x in list(itertools.product(p,d,q))]
seasonal_pdq = [(x[0],x[1],x[2],season) for x in list(itertools.product(sp,sd,sq))]
best_result = [[0,0,3000]]#3000にしとく
best_score=0
ls=[]
for c,param in enumerate(pdq):
    print("----------------------------------\n",
          c/len(pdq)*100,"%","\n----------------------------------")
    for param_seasonal in seasonal_pdq:
        try:
            mod = SARIMAX(train_sales,#学習データ
                          order = param, 
                          seasonal_order=param_seasonal)#param_seasonal
            results = mod.fit()
            pre=results.predict(end=26)
            r2=r2_score(df_sales[id][df_sales["date"]>=day],pre[1:])
            #if  r2 > 0 :#results.aic < best_result[0][2] and
                                 #param_seasonal
            ls.append([param,param_seasonal ,results.aic,r2])
                #best_result=[param, param_seasonal, results.aic]#.append([param, param_seasonal, results.aic])
        except:continue
#data=pd.DataFrame(ls,columns=["pdq","Spdq","aic","r2"])
data=pd.DataFrame(ls,columns=["pdq","Spdq","aic","r2"])
data=data.sort_values("r2",ascending=False)
path=f"./param/{id}/"
os.makedirs(path,exist_ok=True)
data.to_csv(f"{path}SARIMA_id_{id}.csv",index=False)
#print("AIC最小のモデル:", best_result)
# temp[(1, 1, 2), (0, 1, 1, 12), 301.55020364948075]
#sales,id=0 [(0, 1, 0), (0, 0, 0, 72), 12975.210851587632]
#"""

#"""SARIMA plot sales,id=0
train_sales=df_sales[id][df_sales["date"]<day].ravel()                           #72
model1 = SARIMAX(train_sales,exogenous,order = [1, 0, 0], seasonal_order=[2, 0, 2, 12]).fit()
pre1=model1.predict(end=27)
r2_1=r2_score(df_sales[id][df_sales["date"]>=day],pre1[1:])
model2 = SARIMAX(train_sales,order = [0, 1, 0], seasonal_order=[0, 0, 0, 12]).fit()
pre2=model2.predict(end=27)
r2_2=r2_score(df_sales[id][df_sales["date"]>=day],pre2[1:])

day2=datetime.date(2020, 10, 1)
plt.plot(df_sales["date"][df_sales["date"]>=mid_day], df_sales[id][df_sales["date"]>=mid_day])
plt.plot(df_sales["date"][df_sales["date"]>=day],pre1[1:])
plt.plot(df_sales["date"][df_sales["date"]>=day],pre2[1:])
#plt.title(f"R^2_score:normal={r2_2}\nwith_exogenous={r2_1}")
#plt.savefig("./graph/sarimax_sales_0.jpg")
plt.show()
#"""

"""SARIMA plot temp
model = SARIMAX(df["平均気温(℃)"][df["date"]<day].ravel(),order = [1, 1, 2], seasonal_order=[0, 1, 1, 12]).fit()
pre=model.predict(end=14)
plt.plot(df["date"][df["date"]>=mid_day], df["平均気温(℃)"][df["date"]>=mid_day])
plt.plot(df["date"][df["date"]>=day],pre[1:])
plt.savefig("./graph/sarimax_temp.jpg")
plt.show()
#"""

df_sales=conv_date(pd.read_csv("sales.csv"))
df_sales=conv_month(df_sales,"mean")#1 or mean
