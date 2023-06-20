import numpy as np
def miss_val(df,meth):
    x,y=np.shape(df.iloc[:,1:51].to_numpy())
    if meth != "marginal":
        for i in range(1,x+1):
            if meth == "mean":
                val=df.iloc[i-1:i,1:51].to_numpy()[0][df.iloc[i-1:i,1:51].to_numpy()[0] != 0].mean()#各列の平均値      
            elif meth =="median":
                val=df.iloc[i-1:i,1:51][df.iloc[i-1:i,1:51] != 0].median(axis=1)#各列の中央値
            for j in range(1,y+1):
                if df.iloc[i-1:i,j:j+1].values[0][0] == 0: df.iloc[i-1:i,j:j+1]=int(val)#整数値 
    elif meth == "marginal":
        for i in range(1,x+1):
            for j in range(1,y+1):
                if df.iloc[i-1:i,j:j+1].values[0][0] == 0:
                    if j == y+1:df.iloc[i-1:i,j:j+1]=df.iloc[i-1:i,j-1:j].values#最終行の値は1つ前の値
                    if j == 1:#最初の行の値は左側の0以外の値
                        right=df.iloc[i-1:i,1:51].to_numpy()[0][df.iloc[i-1:i,1:51].to_numpy()[0] != 0].mean()
                        val=0
                        k=j+1
                        while (k < y+1):
                            if df.iloc[i-1:i,k:k+1].values !=0 :
                                left=df.iloc[i-1:i,k:k+1].values
                                break
                            k=k+1
                        else:left=right
                        v=(left+right)/2
                        df.iloc[i-1:i,j:j+1]=int(v)
                    else:
                        right=df.iloc[i-1:i,j-1:j].values#right,右隣
                        #left
                        val=0
                        k=j+1
                        while (k < y+1):
                            if df.iloc[i-1:i,k:k+1].values != 0:
                                left=df.iloc[i-1:i,k:k+1].values
                                break
                            k=k+1
                        else:left=right
                        v=(left+right)/2
                        df.iloc[i-1:i,j:j+1]=int(v)
    else:
        print('The second argument should be "mean" , "median" or "marginal".')
        exit()
    return df
