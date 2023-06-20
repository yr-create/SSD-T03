def make_dict(id):
    id_cast=id.astype({'販売会社': str})
    id_cast=id.astype({'商品名': str})
    dic={}
    for i in id["ID"].ravel():
        df=id_cast[id['ID'] == i]
        id_num=df.loc[:,"ID"].iloc[-1]
        company=df.loc[:,"販売会社"].iloc[-1]
        name=df.loc[:,"商品名"].iloc[-1]
        dic[str(id_num)]={"company":company,"name":name}
    return dic