
import json
def make_json(data,dic):
    for c,i in enumerate(data.columns):
        if i != "id":
            caption=str(i)[0:7]
            df=data[["id",i]].sort_values(i,ascending=False)
            ls=[]
            for j in df["id"].ravel():
                df_id=df[df["id"] == j]
                id=j
                name=dic[str(j)]["name"]
                sales=int(df_id.loc[:,i].iloc[-1])
                d={"id":id,"name":name,"sales":sales}
                ls.append(d)
            di={"caption":caption,"members":ls}  
            with open(f"./json/{caption}.json","w",encoding='utf-8')as f:json.dump(di,f,ensure_ascii=False,indent=4)      
    return None