import datetime
def conv_date(df):
    s_format = '%Y/%m/%d'
    x,y=df.shape
    for i in range(0,x):
        df.iloc[i,0]=datetime.datetime.strptime(
                    df.iloc[i,0],s_format).date()
    return df