import statsmodels.api as sm
import numpy as np
import pandas as pd
import datetime
def pre_temp(temp,day,num):#第1引数=気温(予測したい数値),第２引数=最終日がわかるもの,第３引数=予測したい期間(nヶ月)
    y=day.year
    m=day.month
    d=day.day
    date_list=[]
    c=0
    for _  in range(num):
        m=m+1
        if m > 12:
            c=c+1
            m=1
        date=datetime.date(y+c,m,d)
        date_list.append(date)
    model = sm.tsa.AutoReg(temp,lags=0,seasonal=True,period=12).fit()
    pre=model.predict(end=num-1)
    df_temp=pd.DataFrame(date_list,columns=["date"])
    df_date=pd.DataFrame(pre,columns=["temp"])
    return pd.concat([df_date,df_temp],axis=1)
