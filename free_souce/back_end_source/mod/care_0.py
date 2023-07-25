import datetime
def care_0(df,seasons,ids=[str(i) for i in range(0,50,1)]):
    id_0=[]
    for id in ids:
        if (df[id] == 0).any() and False in (df[id] == 0).ravel():id_0.append(id) 
    for id in id_0:
        while (df[id] == 0).any() and False in (df[id] == 0).ravel():
            for i in range(len(df[id])):
                if df[id][i] == 0:
                    #df[id][i]=data[str(df["date"].iloc[i].month)]
                    date=df["date"][i]
                    season=seasons[id][0]
                    if datetime.date(date.year+int(int(season)/12),date.month,date.day) in df["date"].values:
                        df[id][i]=df[id][df["date"]==datetime.date(date.year+int(int(season)/12),date.month,date.day)]
    return df