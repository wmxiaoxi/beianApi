import requests

from common.con_sql import InceptorConnect

def post_mth(url,data,headers):
    try:
        res=requests.post(url=url,json=data,headers=headers)
        result=res.json()
        return result
    except Exception as e:
        raise e

def get_mth(url,par):
    try:
        res=requests.get(url=url,params=par)
        result=res.json()
        return result
    except Exception as e:
        raise e



def sqlcheck(sql):
    # ###连接postgresql
    try:
        newpg=InceptorConnect()
        newpgcoon=newpg.postgconnect()
        sql = sql
        sqlresult=newpg.get_all_data(newpgcoon,sql)
        newpg.mysql_close(newpgcoon)
        return sqlresult
    except Exception as e:
        raise e