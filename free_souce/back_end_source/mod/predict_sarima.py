from statsmodels.tsa.statespace.sarimax import SARIMAX
import datetime
import pandas as pd

#第1引数=学習データ,第2,3引数=SARIMAXパラメーター(イテレートオブジェクト),第4引数=予測数,第5引数=最終日がわかるもの
def pre_sarima(train,param,qparam,e,day):
    y=day.year
    m=day.month
    d=day.day
    date_list=[]
    c=0
    for _  in range(e):
        m=m+1
        if m > 12:
            c=c+1
            m=1
        date=datetime.date(y+c,m,d)
        date_list.append(date)
    df_date=pd.DataFrame(date_list,columns=["date"])
    mod = SARIMAX(train,#学習データ
                order = param, 
                seasonal_order=qparam).fit()
    pre=mod.predict(end=e)[1:]
    df_pre=pd.DataFrame(pre,columns=["data"])
    return pd.concat([df_date,df_pre],axis=1)
    
    