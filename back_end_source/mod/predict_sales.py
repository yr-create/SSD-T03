import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
#第1引数はメインプログラムで作った形のデータフレーム
##学習用に気温(説明変数)と売り上げのデータが必要
#第2引数は予測したい商品のid(第1引数のデータフレームのカラムと対応)
#第3引数は気温(説明変数)
#第4引数は気温に対応した日付
def pre_sales(df,id,temp,date,pool=None):
    #"""
    if type(id) is list:
        s=np.shape(id)
        if len(s) > 1:
            print("The second argument must be a one-dimensional list, int, or str.")
            return None
        id=[str(i) for i in id]
    elif type(id) is not list:
        if type(id) is int or type(id) is str:id=[str(id)]
    else:print("The second argument must be a one-dimensional list, int, or str.")
    for i in id:
        if i not in df.columns:
            print(f"{i} is not in list.Remove {i} from list.")
            id.remove(i)
        elif i in ["平年値からの差(℃)","平均湿度(％)","平年値からの差(％)","日最低気温25℃以上日数(日)","平年値からの差(日)","日最高気温35℃以上日数(日)","平年値からの差(日).1"]:id.remove(i)
    if len(temp) != len(date):print("The lengths of the third and fourth arguments should be equal.")
    #"""
    ls=[]
    data_pool=None
    for i in id:
        x=df["平均気温(℃)"].to_numpy().reshape(-1, 1)
        y=df[i].values.ravel()
        RF = RandomForestRegressor()
        """
        n_estimators=100,
        criterion='mse', 
        max_depth=None, 
        min_samples_split=2, 
        min_samples_leaf=1, 
        min_weight_fraction_leaf=0.0, 
        max_features='auto', 
        max_leaf_nodes=None, 
        min_impurity_decrease=0.0, 
        bootstrap=True, 
        oob_score=False, 
        n_jobs=None, 
        random_state=None, 
        verbose=0, 
        warm_start=False, 
        ccp_alpha=0.0, 
        max_samples=None
        #"""
        RF.fit(x ,y)
        pred=RF.predict(temp.to_numpy().reshape(-1, 1))
        ls.append(pred.astype(np.int64))
        if pool is not None:
            if str(pool) == i:data_pool=pred.astype(np.int64)
    df_id=pd.DataFrame(id,columns=["id"])
    df_return=pd.DataFrame(ls,columns=date)
    df_return=pd.concat([df_id,df_return],axis=1)
    return df_return,data_pool